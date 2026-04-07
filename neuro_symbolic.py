import requests
import json
import re
import sys
import io

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:8b"


def extract_after_think(text):
    match = re.search(r'</think>\s*(.*)', text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()


def call_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 8192}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=600)
        response.raise_for_status()
        return extract_after_think(response.json().get("response", ""))
    except Exception as e:
        print(f"  [LLM Error]: {e}")
        return ""


def step1_semantic_parser(problem):
    prompt = f"Extract the mathematical entities, variables, operations, and the ultimate goal from the following problem. Return ONLY a concise structured summary.\n\nProblem: {problem}"
    return call_llm(prompt)


def step2_pot_generator(parsed_structure, hint=""):
    bloc_hint = f"\nUSE THESE MATHEMATICAL RULES/HINTS:\n{hint}\n" if hint else ""

    prompt = (
        "Based on the following mathematical structure, write a Python script using the `sympy` library to solve the problem."
        f"{bloc_hint}"
        "\n- Put the final numerical or symbolic answer in a variable named `final_result`."
        "\n- ONLY output valid Python code inside a ```python ... ``` block. Do NOT add any explanations."
        f"\n\nStructure: {parsed_structure}"
    )
    return call_llm(prompt)


def step3_code_validator(code_response):
    match = re.search(r'```python(.*?)```', code_response, re.DOTALL)
    code = match.group(1).strip() if match else code_response.strip()
    code = re.sub(r'<think>.*?</think>', '', code, flags=re.DOTALL).strip()

    forbidden = ['import os', 'import sys', 'subprocess', 'open(', 'exec(', 'eval(', '__import__']
    for word in forbidden:
        if word in code:
            raise ValueError(f"Cod periculos detectat: {word}")
    return code


def step4_symbolic_executor(safe_code):
    local_env = {}
    captured_output = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured_output

    try:
        exec(safe_code, {}, local_env)
        printed_text = captured_output.getvalue().strip()
        result = local_env.get('final_result')

        if result is not None:
            return str(result)
        elif printed_text:
            return printed_text
        else:
            return "Eroare: 'final_result' nedefinit."
    except Exception as e:
        return f"Eroare executie: {e}"
    finally:
        sys.stdout = old_stdout


def step5_post_processing(problem, result):
    prompt = (
        f"The user asked: '{problem}'.\n"
        f"A symbolic engine calculated the exact answer as: '{result}'.\n"
        "You MUST end your response EXACTLY with the following format:\n"
        "RASPUNS_FINAL: <only_the_final_value>\n"
        "Do not include anything after this line."
    )
    return call_llm(prompt)


def run_neuro_symbolic_pipeline(problem, hint=""):
    print("  [NS] Pas 1: Semantic Parsing....")
    parsed = step1_semantic_parser(problem)

    print("  [NS] Pas 2: Generare Program-of-Thought (cu RAG)....")
    pot_code = step2_pot_generator(parsed, hint)

    try:
        print("  [NS] Pas 3 & 4: Validare si Executie Simbolica (SymPy)....")
        safe_code = step3_code_validator(pot_code)
        raw_result = step4_symbolic_executor(safe_code)
    except Exception as e:
        raw_result = str(e)

    print("  [NS] Pas 5: Formatare Raspuns.....")
    final_answer = step5_post_processing(problem, raw_result)
    return final_answer