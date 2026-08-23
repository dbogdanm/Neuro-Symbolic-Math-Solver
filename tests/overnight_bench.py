"""Overnight benchmark orchestrator: GSM8K(50) + MATH500(50) + AIME25(30).

Each problem runs in its own subprocess (tests/bench_one_json.py) with a hard
wall-clock budget; on overrun the whole process tree is killed and the problem
is recorded as a timeout. Results append to tests/results/overnight_results.jsonl
after every problem, so the run is fully resumable: already-recorded
(benchmark, id) pairs are skipped on restart. Charts in Charts/ are regenerated
after every problem, so partial results are always visible.

Usage: python tests/overnight_bench.py [model] [benchmark ...]
"""

import json
import os
import re
import subprocess
import sys
import time

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grading import grade  # noqa: E402 - needs the sys.path setup above

DATA_DIR = os.path.join(_ROOT, "tests", "datasets")
RESULTS_DIR = os.path.join(_ROOT, "tests", "results")
LOGS_DIR = os.path.join(RESULTS_DIR, "logs")
RESULTS_PATH = os.path.join(RESULTS_DIR, "overnight_results.jsonl")

# (name, dataset file, per-problem wall-clock budget in seconds)
#
# The default set is what the paper reports. SVAMP is available under the same
# harness and the same grader — pass it explicitly rather than adding a fourth
# 300-problem benchmark to every run:
#     python tests/overnight_bench.py deepseek-r1:8b svamp
ALL_BENCHMARKS = {
    "gsm8k": ("gsm8k_50.jsonl", 600),
    "math500": ("math500_50.jsonl", 900),
    "aime25": ("aime25_30.jsonl", 1200),
    "svamp": ("svamp_300.jsonl", 600),
}
DEFAULT_BENCHMARKS = ["gsm8k", "math500", "aime25"]


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
    selected = sys.argv[2:] or DEFAULT_BENCHMARKS
    unknown = [b for b in selected if b not in ALL_BENCHMARKS]
    if unknown:
        print(f"[bench] unknown benchmark(s): {', '.join(unknown)}; "
              f"known: {', '.join(ALL_BENCHMARKS)}")
        return
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    done = load_done(model)
    print(f"[bench] starting; {len(done)} results already recorded for {model}", flush=True)

    for bench in selected:
        fname, budget = ALL_BENCHMARKS[bench]
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
