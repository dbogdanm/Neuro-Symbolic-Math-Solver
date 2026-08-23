"""Re-grade a finished benchmark run with the current grader.

The overnight harness stores the model's raw answer alongside the label, so a
run can be re-scored without spending GPU time again. This matters when the
grader is fixed after the fact: the v1 grader compared normalized strings only,
and marked six MATH500 answers wrong that were mathematically correct but
formatted differently (SymPy's ``6 - 5*I`` against the label's ``6 - 5i``,
``[3, 5, 7]`` against ``3, 5, 7``, an unordered solution set against an ordered
one). Re-grading fixes the score without touching the recorded model output.

Only ``status`` fields recorded as ``correct``/``wrong`` are revisited —
``timeout`` and ``error`` describe the run, not the answer, and are preserved.

Usage:
    python tests/regrade.py            # report what would change
    python tests/regrade.py --write    # rewrite the results file in place
"""

import argparse
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grading import grade  # noqa: E402 - needs the sys.path setup above

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_PATH = os.path.join(_ROOT, "tests", "results", "overnight_results.jsonl")

GRADED_STATUSES = ("correct", "wrong")


def regrade(records: list) -> list:
    """Return (record, old_status, new_status) for every graded record."""
    changes = []
    for rec in records:
        old = rec.get("status")
        if old not in GRADED_STATUSES:
            continue
        new = "correct" if grade(rec.get("predicted", ""), rec.get("gold", "")) else "wrong"
        changes.append((rec, old, new))
    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true",
                        help="rewrite the results file (a .bak copy is kept)")
    parser.add_argument("--results", default=RESULTS_PATH)
    args = parser.parse_args()

    if not os.path.exists(args.results):
        print(f"No results file at {args.results}")
        return 1

    with open(args.results, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    flipped = [(r, o, n) for r, o, n in regrade(records) if o != n]

    for rec, old, new in flipped:
        print(f"{rec['benchmark']:8} {rec['id']:40} {old} -> {new}\n"
              f"         predicted={rec['predicted'][:60]!r} gold={rec['gold'][:40]!r}")

    print(f"\n{len(flipped)} of {len(records)} records change status.")
    for bench in dict.fromkeys(r["benchmark"] for r in records):
        rows = [r for r in records if r["benchmark"] == bench]
        correct = sum(1 for r in rows if r["status"] == "correct")
        print(f"  {bench:8} {correct}/{len(rows)} = {100 * correct / len(rows):.0f}%"
              f"  (before re-grading)")

    if not args.write:
        print("\nDry run - pass --write to apply.")
        return 0

    shutil.copyfile(args.results, args.results + ".bak")
    for rec, _old, new in flipped:
        rec["status"] = new
        rec["regraded"] = True
    with open(args.results, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"\nWritten. Previous file kept at {os.path.basename(args.results)}.bak")
    for bench in dict.fromkeys(r["benchmark"] for r in records):
        rows = [r for r in records if r["benchmark"] == bench]
        correct = sum(1 for r in rows if r["status"] == "correct")
        print(f"  {bench:8} {correct}/{len(rows)} = {100 * correct / len(rows):.0f}%"
              f"  (after re-grading)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
