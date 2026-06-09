"""Run a single problem through the neuro-symbolic pipeline from the CLI.

Usage:
    python tests/run_one.py "<problem text>" [model]

Defaults to ollama:deepseek-r1:8b (the paper's edge model).
"""
import os
import sys
import time

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
os.chdir(_ROOT)  # rules_base resolves ./chroma_db_reguli relative to CWD

from llm import LLMConfig
from neuro_symbolic import run_neuro_symbolic_pipeline


def main():
    problem = sys.argv[1] if len(sys.argv) > 1 else "how much is 2+6"
    model = sys.argv[2] if len(sys.argv) > 2 else "deepseek-r1:8b"

    cfg = LLMConfig(provider="ollama", model=model)
    print(f"MODEL:   {cfg.label}")
    print(f"PROBLEM: {problem}\n")

    t0 = time.time()
    result = run_neuro_symbolic_pipeline(problem, cfg)
    elapsed = time.time() - t0

    print("\n" + "=" * 60)
    print(f"FINAL ANSWER: {result}")
    print(f"TOTAL TIME:   {elapsed:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
