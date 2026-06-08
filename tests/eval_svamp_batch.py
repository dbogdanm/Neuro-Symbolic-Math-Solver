"""Batch evaluation of the neuro-symbolic pipeline on the SVAMP dataset.

Runs every problem through :func:`run_neuro_symbolic_pipeline` and compares the
numeric answer against the gold label, reporting accuracy and timing.

Usage
-----
    python tests/eval_svamp_batch.py --limit 20 --provider ollama --model deepseek-r1:8b

The pipeline talks to whatever provider you configure (Ollama by default, or any
BYOK cloud provider via ``--provider``/``--model``/``--api-key``).
"""

import argparse
import json
import math
import os
import sys
import time

# Make the project root importable when run as a script.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from llm import LLMConfig  # noqa: E402
from neuro_symbolic import run_neuro_symbolic_pipeline  # noqa: E402


def parse_numeric(result: str):
    """Extract a float from a pipeline answer string, or None if impossible."""
    cleaned = "".join(c for c in str(result) if c.isdigit() or c in ".-")
    try:
        return float(cleaned)
    except ValueError:
        return None


def evaluate_svamp(filepath: str, llm: LLMConfig, limit: int = 20, tol: float = 1e-6):
    with open(filepath, "r", encoding="utf-8") as f:
        problems = json.load(f)[:limit]

    total = len(problems)
    correct = 0
    print(f"=== Evaluating {total} SVAMP problems with {llm.label} ===")

    start = time.time()
    for i, item in enumerate(problems, 1):
        problem_text = f"{item['Body']} {item['Question']}"
        expected = float(item["Answer"])

        print(f"\n[{i}/{total}] Problem ID: {item['ID']}")
        print(f"Text: {problem_text}")
        print(f"Expected: {expected}")

        try:
            result_str = run_neuro_symbolic_pipeline(
                problem_text, llm=llm, ui_callback=lambda _msg: None
            )
            predicted = parse_numeric(result_str)
            is_correct = predicted is not None and math.isclose(
                predicted, expected, rel_tol=0, abs_tol=tol
            )
            if is_correct:
                correct += 1
                print(f"[OK]    answer={result_str}")
            else:
                print(f"[WRONG] predicted={result_str}, expected={expected}")
        except Exception as exc:  # noqa: BLE001 - keep the batch running
            print(f"[ERROR] {exc}")

    duration = time.time() - start
    accuracy = (correct / total * 100) if total else 0.0
    print("\n" + "=" * 50)
    print("EVALUATION COMPLETE")
    print(f"Total time: {duration:.2f}s  ({duration / total:.2f}s per problem)")
    print(f"Accuracy: {correct}/{total} ({accuracy:.2f}%)")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Evaluate the pipeline on SVAMP.")
    parser.add_argument("--file", default=os.path.join(os.path.dirname(__file__), "svamp.json"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--provider", default="ollama")
    parser.add_argument("--model", default="deepseek-r1:8b")
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--base-url", default=None)
    args = parser.parse_args()

    llm = LLMConfig(
        provider=args.provider,
        model=args.model,
        api_key=args.api_key,
        base_url=args.base_url,
    )
    evaluate_svamp(args.file, llm=llm, limit=args.limit)


if __name__ == "__main__":
    main()
