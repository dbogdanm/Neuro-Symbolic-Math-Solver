"""Neuro-symbolic reasoning pipeline.

Natural-language problem  ->  semantic parse (+ parallel RAG)  ->  SymPy
Program-of-Thought  ->  sandboxed execution (+ self-correction)  ->  answer.

All LLM access goes through the provider-agnostic :mod:`llm` layer, so the same
pipeline runs on a local Ollama model or any OpenRouter model the user brings a
key for (BYOK).
"""

import concurrent.futures
import hashlib
import multiprocessing
import queue
import re
from typing import Callable, Optional

import sympy as sp

import llm as llm_layer
from llm import LLMConfig

# rules_base (ChromaDB) and web_search (DuckDuckGo) are imported lazily inside
# get_rag_hint(). This keeps the module's import cost low so the sandboxed
# execution subprocess — re-imported per PoT run under the "spawn" start method
# on Windows/macOS — does not pull in the vector store and search stack each
# time, and so importing this module has no I/O side effects.

# Bounded in-process cache of generated PoT code, keyed by (model, structure,
# hint). Capped so a long-running server cannot grow it without limit.
_pot_cache: dict = {}
_POT_CACHE_MAX = 256


def _log(msg: str, ui_callback: Optional[Callable[[str], None]] = None, **kwargs):
    print(msg, **kwargs)
    if ui_callback:
        ui_callback(msg)


# --------------------------------------------------------------------------- #
# Fast path: trivial arithmetic / basic algebra (no LLM, no RAG)
# --------------------------------------------------------------------------- #

def is_simple_math(problem: str) -> bool:
    """Detect simple arithmetic or basic algebra (e.g. '2+6', 'x^2=4')."""
    clean = problem.replace(" ", "").lower()
    clean = clean.replace("howmuchis", "").replace("whatis", "").replace("calculate", "")
    if re.match(r'^[0-9+\-*/().^]+$', clean):
        return True
    if re.match(r'^[a-z0-9+\-*/().^=]+$', clean) and len(clean) < 15:
        return True
    return False


def solve_simple_math(problem: str) -> str:
    """Solve trivial math with SymPy directly, bypassing the LLM."""
    try:
        clean_problem = problem.lower()
        for phrase in ["how much is", "what is", "calculate"]:
            clean_problem = clean_problem.replace(phrase, "")
        clean_problem = clean_problem.strip().strip("?")

        if "=" in clean_problem:
            left, right = clean_problem.split("=")
            expr = sp.sympify(f"({left}) - ({right})")
            sol = sp.solve(expr)
            return f"The solutions are: {sol}"
        # Note: a sympy Float never compares == to a Python int, so convert to a
        # native float to detect whole numbers and render them cleanly.
        value = float(sp.sympify(clean_problem).evalf())
        if value.is_integer():
            return str(int(value))
        return str(round(value, 6))
    except Exception as e:
        print(f"  [FastPath Error]: {e}")
        return ""


# --------------------------------------------------------------------------- #
# LLM helpers (provider-agnostic)
# --------------------------------------------------------------------------- #

def call_llm(prompt: str, llm: LLMConfig, num_ctx: int = 4096,
             ui_callback: Optional[Callable[[str], None]] = None) -> str:
    _log(f"LOG: [LLM] Calling {llm.label}...", ui_callback)
    _log(f"PROMPT: {prompt}", ui_callback)
    try:
        full_response = llm_layer.complete(llm, prompt, num_ctx=num_ctx)
        think_match = re.search(r'<think>(.*?)</think>', full_response, re.DOTALL)
        if think_match:
            _log(f"THINK: {think_match.group(1)}", ui_callback)
        return full_response
    except Exception as e:
        _log(f"LOG: [LLM Error]: {e}", ui_callback)
        return ""


def call_llm_json(prompt: str, llm: LLMConfig,
                  ui_callback: Optional[Callable[[str], None]] = None) -> Optional[dict]:
    import json
    try:
        raw = llm_layer.complete(llm, prompt, temperature=0.1, num_ctx=4096, json_mode=True)
        clean_raw = re.sub(r'<think>.*?(?:</think>|$)', '', raw, flags=re.DOTALL).strip()
        # Some models wrap JSON in code fences even in json mode.
        clean_raw = re.sub(r'^```(?:json)?|```$', '', clean_raw.strip(), flags=re.MULTILINE).strip()
        return json.loads(clean_raw)
    except Exception:
        return None


# --------------------------------------------------------------------------- #
# RAG retrieval
# --------------------------------------------------------------------------- #

def extract_problem_type(problem: str, llm: LLMConfig,
                         ui_callback: Optional[Callable[[str], None]] = None) -> str:
    _log("  [RAG] Extracting problem type...", ui_callback)
    prompt = (
        "You are a math problem classifier. Describe the MATHEMATICAL TYPE in "
        "1-2 VERY SHORT sentences.\n"
        "Focus on structures (sequences, subsets), techniques (recurrence, "
        "combinatorics), and domain.\n"
        "Output ONLY the type description. No explanations.\n\n"
        f"Problem: {problem}"
    )
    tip = call_llm(prompt, llm=llm, num_ctx=2048, ui_callback=ui_callback)
    tip = re.sub(r'<think>.*?</think>', '', tip, flags=re.DOTALL).strip()
    _log(f"  [RAG] Detected type: {tip}", ui_callback)
    return tip


def get_rag_hint(problem: str, llm: LLMConfig,
                 ui_callback: Optional[Callable[[str], None]] = None) -> str:
    try:
        from rules_base import find_hint
    except Exception as exc:  # noqa: BLE001 - RAG is an optional dependency
        _log(f"LOG: [RAG] Disabled ({exc}).", ui_callback)
        return ""

    tip = extract_problem_type(problem, llm=llm, ui_callback=ui_callback)
    if not tip:
        return ""

    # 1. Internal RAG (ChromaDB)
    hint = find_hint(tip)
    if hint:
        _log("LOG: [RAG] Internal hint found.", ui_callback)
        _log(f"PROMPT: {hint}", ui_callback)
        return hint

    # 2. Web search fallback
    _log("LOG: [RAG] No internal hint. Searching Web...", ui_callback)
    from web_search import get_web_hint
    web_hint = get_web_hint(tip)
    if web_hint:
        _log("LOG: [RAG] Web search results incorporated.", ui_callback)
        _log(f"PROMPT: {web_hint}", ui_callback)
        return web_hint

    return ""


# --------------------------------------------------------------------------- #
# Pipeline stages
# --------------------------------------------------------------------------- #

def step1_semantic_parser(problem: str, llm: LLMConfig,
                          ui_callback: Optional[Callable[[str], None]] = None) -> str:
    _log("  [NS] Stage 1: Semantic Parsing...", ui_callback)
    prompt = (
        "Respond ONLY with a valid JSON object extracting: variables, "
        "known_values, constraints, and goal.\n"
        f"Problem: {problem}"
    )
    parsed_dict = call_llm_json(prompt, llm=llm, ui_callback=ui_callback)
    if parsed_dict:
        import json
        return json.dumps(parsed_dict, indent=2)
    return "No structure detected."


def step2_pot_generator(parsed_structure: str, llm: LLMConfig, hint: str = "",
                        ui_callback: Optional[Callable[[str], None]] = None) -> str:
    cache_key = hashlib.md5(
        f"{llm.label}||{parsed_structure}||{hint}".encode()
    ).hexdigest()
    if cache_key in _pot_cache:
        _log("  [NS] Stage 2: Cache hit.", ui_callback)
        return _pot_cache[cache_key]

    bloc_hint = f"\nHINTS/SEARCH RESULTS:\n{hint}\n" if hint else ""
    prompt = (
        "You are an expert Python SymPy programmer. Think step by step in <think></think>.\n"
        "Then output ONLY one python code block using SymPy.\n"
        "The code MUST contain: final_result = <value>\n"
        f"{bloc_hint}\nStructure:\n{parsed_structure}"
    )
    _log("  [NS] Stage 2: Generating Program-of-Thought...", ui_callback)
    result = call_llm(prompt, llm=llm, num_ctx=16384, ui_callback=ui_callback)
    result = re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL).strip()
    if len(_pot_cache) >= _POT_CACHE_MAX:
        _pot_cache.pop(next(iter(_pot_cache)))  # evict oldest (FIFO)
    _pot_cache[cache_key] = result
    return result


def step3_code_validator(code_response: str,
                         ui_callback: Optional[Callable[[str], None]] = None) -> str:
    if not code_response:
        raise ValueError("Empty LLM output.")
    blocks = re.findall(r'```python\s*(.*?)```', code_response, re.DOTALL | re.IGNORECASE)
    if not blocks:
        blocks = re.findall(r'```(?:python)?\s*(.*?)```', code_response, re.DOTALL | re.IGNORECASE)
    if not blocks:
        raise ValueError("No python block found.")
    python_code = blocks[-1].strip()
    if 'final_result' not in python_code:
        raise ValueError("'final_result' not defined.")
    return python_code


# --------------------------------------------------------------------------- #
# Sandboxed execution
#
# SECURITY MODEL: the Program-of-Thought code is generated by an LLM and is
# therefore untrusted. It runs in a separate process with a hard wall-clock
# timeout, so a hang or crash can never take down the server. This is process
# *isolation*, NOT a security sandbox — the code runs with full Python builtins
# and may import modules or touch the filesystem/network. That is acceptable for
# the intended use (a local, single-user research tool driving a local model).
# Do NOT expose this endpoint to untrusted users without first restricting
# builtins/imports and adding OS-level isolation (e.g. a locked-down container
# with no network and a read-only filesystem).
# --------------------------------------------------------------------------- #

class SandboxError(RuntimeError):
    """Raised when sandboxed PoT code fails to execute or yields no result."""


def _worker_exec(code, q):
    """Execute generated code in a child process and report final_result back."""
    import itertools
    import math

    # Pre-bind common libraries so generated code can use them without imports.
    namespace = {"sp": sp, "sympy": sp, "math": math, "itertools": itertools}
    try:
        exec(code, namespace)  # noqa: S102 - intentional; see SECURITY MODEL above
        q.put(("SUCCESS", namespace.get("final_result")))
    except Exception as e:  # noqa: BLE001 - report any failure back to the parent
        q.put(("ERROR", str(e)))


def execute_code_with_timeout(python_code: str, timeout: int = 120):
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=_worker_exec, args=(python_code, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        raise TimeoutError("Execution timed out.")
    try:
        status, result = q.get_nowait()
    except queue.Empty:
        raise SandboxError("Code failed to produce a result.") from None
    if status == "ERROR":
        raise SandboxError(result)
    return result


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #

def run_neuro_symbolic_pipeline(problem: str, llm: LLMConfig, hint: str = "",
                                ui_callback: Optional[Callable[[str], None]] = None) -> str:
    _log("\n[NS] Starting Optimized Pipeline...", ui_callback)

    if is_simple_math(problem):
        _log("  [NS] Fast Path: Simple math detected. Solving with SymPy...", ui_callback)
        result = solve_simple_math(problem)
        if result:
            _log(f"  [NS] Solved via Fast Path: {result}", ui_callback)
            return result

    # Stage 0 & 1: RAG retrieval runs in parallel with semantic parsing.
    parsed_structure = ""
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_hint = executor.submit(get_rag_hint, problem, llm, ui_callback) if not hint else None
        future_parse = executor.submit(step1_semantic_parser, problem, llm, ui_callback)

        if not hint and future_hint is not None:
            _log(
                "  [NS] Stage 0: Retrieval (RAG + Web) running in parallel with "
                "Stage 1 (Parsing)...",
                ui_callback,
            )
            hint = future_hint.result()

        parsed_structure = future_parse.result()

    # Stage 2 & 3: Program-of-Thought generation with a self-correction loop.
    max_retries = 3
    last_error = ""
    raw_pot = ""

    for attempt in range(1, max_retries + 1):
        try:
            if attempt == 1:
                raw_pot = step2_pot_generator(
                    parsed_structure, llm=llm, hint=hint, ui_callback=ui_callback
                )
            else:
                _log(
                    f"  [NS] Stage 2: Self-Correction Attempt {attempt}/{max_retries}...",
                    ui_callback,
                )
                error_prompt = (
                    "Your previous Python SymPy code failed with the following error:\n"
                    f"{last_error}\n\n"
                    "Please analyze the error and provide a CORRECTED Python SymPy code block.\n"
                    "Remember, the code MUST contain exactly: final_result = <value>\n"
                    "Do NOT repeat the same mistake. Output ONLY the fixed python code block."
                )
                raw_pot = call_llm(error_prompt + "\n\nOriginal Code:\n" + raw_pot,
                                   llm=llm, num_ctx=8192, ui_callback=ui_callback)

            python_code = step3_code_validator(raw_pot, ui_callback=ui_callback)
            final_result = execute_code_with_timeout(python_code)

            if final_result is None:
                raise ValueError("Execution returned None.")

            _log(f"  [NS] Pipeline finished successfully: {final_result}", ui_callback)
            return str(final_result)

        except Exception as e:
            last_error = str(e)
            _log(f"  [NS] Execution failed (Attempt {attempt}): {last_error}", ui_callback)

    # Fallback: direct natural-language reasoning if every PoT attempt failed.
    _log("  [NS] All PoT attempts failed. Retrying with direct reasoning...", ui_callback)
    prompt = f"Solve this math problem. Show final answer in \\boxed{{}}:\n{problem}\nHint: {hint}"
    final_attempt = call_llm(prompt, llm=llm, num_ctx=8192, ui_callback=ui_callback)
    match = re.search(r'\\boxed\{(.*?)\}', final_attempt)
    return match.group(1) if match else "Extraction Failed"


if __name__ == "__main__":
    cfg = LLMConfig(provider="ollama", model="deepseek-r1:8b")
    print(run_neuro_symbolic_pipeline("how much is 2+6", cfg))
