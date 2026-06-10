"""Overnight benchmark orchestrator: GSM8K(50) + MATH500(50) + AIME25(30).

Each problem runs in its own subprocess (tests/bench_one_json.py) with a hard
wall-clock budget; on overrun the whole process tree is killed and the problem
is recorded as a timeout. Results append to tests/results/overnight_results.jsonl
after every problem, so the run is fully resumable: already-recorded
(benchmark, id) pairs are skipped on restart. Charts in Charts/ are regenerated
after every problem, so partial results are always visible.

Usage: python tests/overnight_bench.py [model]
"""

import json
import os
import re
import subprocess
import sys
import time
from fractions import Fraction

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)

DATA_DIR = os.path.join(_ROOT, "tests", "datasets")
RESULTS_DIR = os.path.join(_ROOT, "tests", "results")
LOGS_DIR = os.path.join(RESULTS_DIR, "logs")
RESULTS_PATH = os.path.join(RESULTS_DIR, "overnight_results.jsonl")

# (name, dataset file, per-problem wall-clock budget in seconds)
BENCHMARKS = [
    ("gsm8k", "gsm8k_50.jsonl", 600),
    ("math500", "math500_50.jsonl", 900),
    ("aime25", "aime25_30.jsonl", 1200),
]


# --------------------------------------------------------------------------- #
# Grading
# --------------------------------------------------------------------------- #

def normalize_answer(s: str) -> str:
    """Best-effort normalization of LaTeX/SymPy answer strings for comparison."""
    s = str(s).strip()
    s = s.replace("$", "").replace("\\!", "").replace("\\,", " ").replace("\\;", " ")
    s = re.sub(r"\\text\s*\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\mbox\s*\{([^}]*)\}", r"\1", s)
    s = s.replace("\\left", "").replace("\\right", "")
    s = re.sub(r"\\[dt]?frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)", s)
    s = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r"sqrt(\1)", s)
    s = re.sub(r"\\sqrt\s*(\d+)", r"sqrt(\1)", s)
    s = s.replace("\\pi", "pi").replace("\\cdot", "*").replace("\\times", "*")
    s = s.replace("^\\circ", "").replace("\\circ", "").replace("°", "")
    s = s.replace("\\%", "").replace("%", "")
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)  # thousands separators
    s = s.replace("{", "(").replace("}", ")")
    s = s.replace(" ", "").rstrip(".").lower()
    return s


def to_number(s: str):
    if not s or len(s) > 200:
        return None
    try:
        return float(Fraction(s))
    except Exception:  # noqa: BLE001
        pass
    try:
        import sympy as sp
        # implicit multiplication: "2pi" -> "2*pi", "3sqrt(2)" -> "3*sqrt(2)"
        s = re.sub(r"(?<=[\d)])(?=[a-z(])", "*", s)
        return float(sp.sympify(s).evalf())
    except Exception:  # noqa: BLE001
        return None


def _split_tuple(s: str):
    """Split "(a,b,...)" at depth-0 commas; None if not tuple-shaped."""
    if not (s.startswith("(") and s.endswith(")") and "," in s):
        return None
    parts, depth, cur = [], 0, ""
    for ch in s[1:-1]:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return parts if len(parts) > 1 else None


def _equal_scalar(p: str, g: str) -> bool:
    if p and p == g:
        return True
    pn, gn = to_number(p), to_number(g)
    if pn is not None and gn is not None:
        return abs(pn - gn) <= 1e-4 * max(1.0, abs(gn))
    return False


def grade(predicted: str, gold: str) -> bool:
    p, g = normalize_answer(predicted), normalize_answer(gold)
    if p and p == g:
        return True
    pt, gt = _split_tuple(p), _split_tuple(g)
    if pt and gt and len(pt) == len(gt):
        return all(_equal_scalar(a, b) for a, b in zip(pt, gt, strict=True))
    return _equal_scalar(p, g)


# --------------------------------------------------------------------------- #
# Harness
# --------------------------------------------------------------------------- #

def load_done(model: str) -> set:
    done = set()
    if os.path.exists(RESULTS_PATH):
        with open(RESULTS_PATH, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:  # tolerate a partial line from an interrupted write
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("model", "deepseek-r1:8b") == model:
                    done.add((rec["benchmark"], rec["id"]))
    return done


def append_result(rec: dict) -> None:
    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def run_one(bench: str, item: dict, budget: int, model: str) -> dict:
    safe_id = re.sub(r"[^\w.-]", "_", str(item["id"]))
    problem_file = os.path.join(RESULTS_DIR, "tmp_problem.txt")
    out_file = os.path.join(RESULTS_DIR, "tmp_result.json")
    log_file = os.path.join(LOGS_DIR, f"{bench}_{safe_id}.log")
    with open(problem_file, "w", encoding="utf-8") as f:
        f.write(item["problem"])
    if os.path.exists(out_file):
        os.remove(out_file)

    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    t0 = time.time()
    with open(log_file, "w", encoding="utf-8") as log:
        proc = subprocess.Popen(
            [sys.executable, os.path.join(_ROOT, "tests", "bench_one_json.py"),
             problem_file, out_file, model],
            cwd=_ROOT, env=env, stdout=log, stderr=subprocess.STDOUT,
        )
        try:
            proc.wait(timeout=budget)
            timed_out = False
        except subprocess.TimeoutExpired:
            timed_out = True
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                           capture_output=True, check=False)
            proc.wait()
    elapsed = round(time.time() - t0, 1)

    if timed_out:
        return {"answer": "", "elapsed": elapsed, "status": "timeout"}
    if not os.path.exists(out_file):
        return {"answer": "", "elapsed": elapsed, "status": "error"}
    try:
        with open(out_file, encoding="utf-8") as f:
            result = json.load(f)
        result["elapsed"] = elapsed
        return result
    except Exception:  # noqa: BLE001
        return {"answer": "", "elapsed": elapsed, "status": "error"}


def regenerate_charts(model: str) -> None:
    # Run as a subprocess so chart-script edits take effect mid-run and a
    # chart bug can never kill the benchmark.
    try:
        subprocess.run(
            [sys.executable, os.path.join(_ROOT, "utils", "make_overnight_charts.py"), model],
            cwd=_ROOT, capture_output=True, timeout=120, check=False,
        )
    except Exception as exc:  # noqa: BLE001 - charts must never kill the run
        print(f"[charts] regeneration failed: {exc}", flush=True)


def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "deepseek-r1:8b"
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    done = load_done(model)
    print(f"[bench] starting; {len(done)} results already recorded for {model}", flush=True)

    for bench, fname, budget in BENCHMARKS:
        path = os.path.join(DATA_DIR, fname)
        with open(path, encoding="utf-8") as f:
            items = [json.loads(line) for line in f if line.strip()]

        for i, item in enumerate(items, 1):
            if (bench, item["id"]) in done:
                continue
            print(f"[bench] {bench} {i}/{len(items)} (id={item['id']}) ...", flush=True)
            result = run_one(bench, item, budget, model)
            correct = result["status"] == "ok" and grade(result["answer"], item["gold"])
            status = "correct" if correct else (
                result["status"] if result["status"] != "ok" else "wrong"
            )
            rec = {
                "benchmark": bench, "id": item["id"], "model": model, "status": status,
                "predicted": result["answer"], "gold": item["gold"],
                "elapsed": result["elapsed"], "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            append_result(rec)
            print(f"[bench]   -> {status} in {result['elapsed']}s "
                  f"(pred={result['answer'][:60]!r} gold={item['gold'][:40]!r})", flush=True)
            regenerate_charts(model)

    print("[bench] ALL BENCHMARKS COMPLETE", flush=True)


if __name__ == "__main__":
    main()
