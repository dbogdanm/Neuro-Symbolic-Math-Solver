import requests
import json
import re
import hashlib
import multiprocessing
import queue
import sympy as sp
from typing import Callable, Optional
from web_search import get_web_hint

try:
    from rules_base import find_hint
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("[WARNING] rules_base not found — RAG disabled.")

OLLAMA_URL = "http://localhost:11434/api/generate"

_pot_cache: dict = {}

def _log(msg: str, ui_callback: Optional[Callable[[str], None]] = None, **kwargs):
    print(msg, **kwargs)
    if ui_callback:
        ui_callback(msg)

def is_simple_math(problem: str) -> bool:
    """Detects simple arithmetic or basic algebraic expressions (e.g., '2+6', 'x^2=4')."""
    # Clean the problem string
    clean = problem.replace(" ", "").lower()
    # Remove common conversational noise
    clean = clean.replace("howmuchis", "").replace("whatis", "").replace("calculate", "")
    # Simple arithmetic: digits and basic operators only
    if re.match(r'^[0-9+\-*/().^]+$', clean):
        return True
    # Basic algebraic patterns like x+5=10 or 2*x=8 (up to 15 chars)
    if re.match(r'^[a-z0-9+\-*/().^=]+$', clean) and len(clean) < 15:
        return True
    return False

def solve_simple_math(problem: str) -> str:
    """Solves trivial math using SymPy directly, bypassing LLM/RAG."""
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
        else:
            # Evaluate as a numeric expression
            result = sp.sympify(clean_problem).evalf()
            # If it's an integer, show it clearly
            if result == int(result):
                return str(int(result))
            return str(round(result, 6))
    except Exception as e:
        print(f"  [FastPath Error]: {e}")
        return ""

def extract_problem_type(problem: str, model: str, ui_callback: Optional[Callable[[str], None]] = None) -> str:
    _log("  [RAG] Extracting problem type...", ui_callback)
    prompt = (
        "You are a math problem classifier. Describe the MATHEMATICAL TYPE in 1-2 VERY SHORT sentences.\n"
        "Focus on structures (sequences, subsets), techniques (recurrence, combinatorics), and domain.\n"
        "Output ONLY the type description. No explanations.\n\n"
        f"Problem: {problem}"
    )
    # Use a smaller context (2048) for extraction to save memory
    tip = call_llm(prompt, model=model, num_ctx=2048, ui_callback=ui_callback)
    tip = re.sub(r'<think>.*?</think>', '', tip, flags=re.DOTALL).strip()
    _log(f"  [RAG] Detected type: {tip}", ui_callback)
    return tip

def get_rag_hint(problem: str, model: str, ui_callback: Optional[Callable[[str], None]] = None) -> str:
    if not RAG_AVAILABLE:
        return ""

    tip = extract_problem_type(problem, model=model, ui_callback=ui_callback)
    if not tip:
        return ""

    # 1. Internal RAG
    hint = find_hint(tip)
    if hint:
        _log(f"LOG: [RAG] Internal hint found.", ui_callback)
        _log(f"PROMPT: {hint}", ui_callback)
        return hint
    
    # 2. Web Search Fallback
    _log("LOG: [RAG] No internal hint. Searching Web...", ui_callback)
    web_hint = get_web_hint(tip)
    if web_hint:
        _log(f"LOG: [RAG] Web search results incorporated.", ui_callback)
        _log(f"PROMPT: {web_hint}", ui_callback)
        return web_hint
        
    return ""

def call_llm(prompt: str, model: str, num_ctx: int = 4096, ui_callback: Optional[Callable[[str], None]] = None) -> str:
    _log(f"LOG: [LLM] Calling model {model}...", ui_callback)
    _log(f"PROMPT: {prompt}", ui_callback)
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, "num_ctx": num_ctx}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=600)
        response.raise_for_status()
        resp_json = response.json()
        full_response = resp_json.get("response", "")
        
        # Log thinking block if present
        think_match = re.search(r'<think>(.*?)</think>', full_response, re.DOTALL)
        if think_match:
            _log(f"THINK: {think_match.group(1)}", ui_callback)
            
        return full_response
    except Exception as e:
        _log(f"LOG: [LLM Error]: {e}", ui_callback)
        return ""

def call_llm_json(prompt: str, model: str, ui_callback: Optional[Callable[[str], None]] = None) -> Optional[dict]:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1, "num_ctx": 4096}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=600)
        response.raise_for_status()
        raw = response.json().get("response", "")
        clean_raw = re.sub(r'<think>.*?(?:</think>|$)', '', raw, flags=re.DOTALL).strip()
        return json.loads(clean_raw)
    except Exception:
        return None

def step1_semantic_parser(problem: str, model: str, ui_callback: Optional[Callable[[str], None]] = None) -> str:
    _log("  [NS] Stage 1: Semantic Parsing...", ui_callback)
    prompt = (
        "Respond ONLY with a valid JSON object extracting: variables, known_values, constraints, and goal.\n"
        f"Problem: {problem}"
    )
    parsed_dict = call_llm_json(prompt, model=model, ui_callback=ui_callback)
    if parsed_dict:
        result_str = json.dumps(parsed_dict, indent=2)
        return result_str
    return "No structure detected."

def step2_pot_generator(parsed_structure: str, model: str, hint: str = "", ui_callback: Optional[Callable[[str], None]] = None) -> str:
    cache_key = hashlib.md5(f"{parsed_structure}||{hint}".encode()).hexdigest()
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
    # Larger context for complex PoT
    result = call_llm(prompt, model=model, num_ctx=16384, ui_callback=ui_callback)
    result = re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL).strip()
    _pot_cache[cache_key] = result
    return result

def step3_code_validator(code_response: str, ui_callback: Optional[Callable[[str], None]] = None) -> str:
    if not code_response: raise ValueError("Empty LLM output.")
    blocks = re.findall(r'```python\s*(.*?)```', code_response, re.DOTALL | re.IGNORECASE)
    if not blocks: blocks = re.findall(r'```(?:python)?\s*(.*?)```', code_response, re.DOTALL | re.IGNORECASE)
    if not blocks: raise ValueError("No python block found.")
    python_code = blocks[-1].strip()
    if 'final_result' not in python_code: raise ValueError("'final_result' not defined.")
    return python_code

def _worker_exec(code, q):
    namespace = {"sp": sp, "sympy": sp}
    try:
        exec(code, namespace)
        q.put(("SUCCESS", namespace.get('final_result')))
    except Exception as e:
        q.put(("ERROR", str(e)))

def execute_code_with_timeout(python_code: str, timeout: int = 120) -> any:
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
        if status == "ERROR": raise Exception(result)
        return result
    except queue.Empty:
        raise Exception("Code failed to produce a result.")

def run_neuro_symbolic_pipeline(problem: str, model: str, hint: str = "", ui_callback: Optional[Callable[[str], None]] = None) -> str:
    _log("\n[NS] Starting Optimized Pipeline...", ui_callback)

    if is_simple_math(problem):
        _log("  [NS] Fast Path: Simple math detected. Solving with SymPy...", ui_callback)
        result = solve_simple_math(problem)
        if result:
            _log(f"  [NS] Solved via Fast Path: {result}", ui_callback)
            return result

    if not hint:
        _log("  [NS] Stage 0: Retrieval (RAG + Web)...", ui_callback)
        hint = get_rag_hint(problem, model=model, ui_callback=ui_callback)

    try:
        parsed_structure = step1_semantic_parser(problem, model=model, ui_callback=ui_callback)
        raw_pot = step2_pot_generator(parsed_structure, model=model, hint=hint, ui_callback=ui_callback)
        python_code = step3_code_validator(raw_pot, ui_callback=ui_callback)
        final_result = execute_code_with_timeout(python_code)
        
        if final_result is None:
            raise ValueError("Execution returned None.")
            
        _log(f"  [NS] Pipeline finished successfully: {final_result}", ui_callback)
        return str(final_result)
    except Exception as e:
        _log(f"  [NS] Pipeline failed: {e}. Retrying with direct reasoning...", ui_callback)
        # Fallback to direct reasoning if PoT fails
        prompt = f"Solve this math problem. Show final answer in \\boxed{{}}:\n{problem}\nHint: {hint}"
        final_attempt = call_llm(prompt, model=model, num_ctx=8192, ui_callback=ui_callback)
        match = re.search(r'\\boxed\{(.*?)\}', final_attempt)
        return match.group(1) if match else "Extraction Failed"

if __name__ == "__main__":
    print(run_neuro_symbolic_pipeline("$\",(2,", "deepseek-r1:8b"))
