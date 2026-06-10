"""Solve one benchmark problem in an isolated process (overnight harness worker).

Usage: python tests/bench_one_json.py <problem_file> <out_file> [model]

Reads the problem text (UTF-8) from <problem_file>, runs the neuro-symbolic
pipeline, and writes ``{"answer", "elapsed", "status"}`` JSON to <out_file>.
Pipeline logs go to stdout (the orchestrator redirects them to a log file).
"""

import json
import os
import sys
import time

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
os.chdir(_ROOT)  # rules_base resolves ./chroma_db_reguli relative to CWD


def main():
    problem_file, out_file = sys.argv[1], sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else "deepseek-r1:8b"

    with open(problem_file, encoding="utf-8") as f:
        problem = f.read()

    from llm import LLMConfig
    from neuro_symbolic import run_neuro_symbolic_pipeline

    t0 = time.time()
    try:
        answer = run_neuro_symbolic_pipeline(
            problem, LLMConfig(provider="ollama", model=model)
        )
        status = "ok"
    except Exception as exc:  # noqa: BLE001 - report, don't crash the harness
        answer = f"PIPELINE_ERROR: {exc}"
        status = "error"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"answer": str(answer), "elapsed": round(time.time() - t0, 1),
                   "status": status}, f)


if __name__ == "__main__":
    main()
