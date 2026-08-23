"""Charts for the overnight benchmark run (regenerated after every problem).

Reads tests/results/overnight_results.jsonl and writes to Charts/:
  - Chart_overnight_results.png   (per-benchmark outcome breakdown + accuracy)
  - Chart_overnight_progress.png  (accuracy as a share of each benchmark)
  - Chart_overnight_times.png     (solve time over *completed* problems)

Usage: python utils/make_overnight_charts.py   (or import generate())
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt  # noqa: E402
from chart_style import STATUS, SYSTEM, apply, footnote, headroom  # noqa: E402

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(_ROOT, "Charts")
DEFAULT_RESULTS = os.path.join(_ROOT, "tests", "results", "overnight_results.jsonl")

BENCH_LABELS = {
    "gsm8k": "GSM8K\n(first 50)",
    "math500": "MATH500\n(first 50)",
    "aime25": "AIME 2025\n(all 30)",
}
BENCH_TOTALS = {"gsm8k": 50, "math500": 50, "aime25": 30}
# Per-problem wall-clock budget, mirroring BENCHMARKS in tests/overnight_bench.py.
# The budgets differ per benchmark, so a "max time" bar compares budgets rather
# than performance unless timeouts are excluded — see chart_times().
BENCH_BUDGETS = {"gsm8k": 600, "math500": 900, "aime25": 1200}
STATUS_ORDER = ["correct", "wrong", "timeout", "error"]
LINE_COLORS = {
    "gsm8k": SYSTEM["previous"],
    "math500": SYSTEM["ours"],
    "aime25": SYSTEM["external"],
}

apply()


def _load(results_path: str, model: str) -> dict:
    by_bench: dict = {}
    if not os.path.exists(results_path):
        return by_bench
    with open(results_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:  # the orchestrator may be mid-write on the last line
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("model", "deepseek-r1:8b") == model:
                by_bench.setdefault(rec["benchmark"], []).append(rec)
    return by_bench


def _stamp(by_bench: dict, done: int, total: int) -> str:
    """Describe the run using the data's own timestamps, never the wall clock.

    Stamping "now" would silently re-date the experiment every time the charts
    are regenerated from unchanged results.
    """
    stamps = [r["ts"] for recs in by_bench.values() for r in recs if r.get("ts")]
    when = max(stamps)[:16] if stamps else "no data"
    state = "complete" if done >= total else f"in progress - {done}/{total} problems"
    return f"{state} - run of {when}"


def _accuracy_note() -> str:
    return ("Accuracy = correct / attempted; timeouts and errors count as failures. "
            "Answers graded by tests/grading.py (symbolic equivalence, not string match).")


def generate(model: str = "deepseek-r1:8b", results_path: str = DEFAULT_RESULTS) -> None:
    by_bench = _load(results_path, model)
    benches = list(BENCH_TOTALS)  # always show all benchmarks, even before they start
    done = sum(len(v) for v in by_bench.values())
    total = sum(BENCH_TOTALS.values())
    stamp = _stamp(by_bench, done, total)
    os.makedirs(OUT_DIR, exist_ok=True)

    _chart_results(by_bench, benches, model, stamp)
    _chart_progress(by_bench, benches, stamp)
    _chart_times(by_bench, benches, stamp)


def _chart_results(by_bench, benches, model, stamp):
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    bottoms = [0] * len(benches)
    for status in STATUS_ORDER:
        vals = [sum(1 for r in by_bench.get(b, []) if r["status"] == status)
                for b in benches]
        if not any(vals):
            continue  # do not put an all-zero series in the legend
        ax.bar([BENCH_LABELS.get(b, b) for b in benches], vals, bottom=bottoms,
               color=STATUS[status], width=0.55, label=status)
        bottoms = [b + v for b, v in zip(bottoms, vals, strict=True)]

    headroom(ax, max(bottoms) if bottoms else 0)
    for i, b in enumerate(benches):
        recs = by_bench.get(b, [])
        n = len(recs)
        n_total = BENCH_TOTALS.get(b, n)
        correct = sum(1 for r in recs if r["status"] == "correct")
        if n:
            ax.annotate(
                f"{100.0 * correct / n:.0f}%\n{correct}/{n} correct",
                (i, bottoms[i]), ha="center", va="bottom",
                fontsize=11, fontweight="bold", color=STATUS["correct"],
            )
        if n < n_total:
            ax.annotate(f"{n}/{n_total} run", (i, 0), ha="center", va="bottom",
                        fontsize=9, color="#555555")
    ax.set_ylabel("problems")
    ax.set_title(f"{model} + neuro-symbolic pipeline (v3.2.0)\n{stamp}",
                 fontweight="bold")
    ax.legend(loc="upper right")
    footnote(fig, _accuracy_note())
    fig.savefig(os.path.join(OUT_DIR, "Chart_overnight_results.png"))
    plt.close(fig)


def _chart_progress(by_bench, benches, stamp):
    """Accuracy against progress through each benchmark.

    Plotted as a *share* of each benchmark rather than a raw cumulative count:
    the benchmarks have different lengths (30 vs 50), so on a shared count axis
    the shorter one simply stops early and reads as a system that stalled.
    """
    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    for b in benches:
        recs = by_bench.get(b, [])
        if not recs:
            continue
        n_total = BENCH_TOTALS.get(b, len(recs))
        xs, ys, correct = [0.0], [0.0], 0
        for k, r in enumerate(recs, 1):
            correct += 1 if r["status"] == "correct" else 0
            xs.append(100.0 * k / n_total)
            ys.append(100.0 * correct / k)
        label = BENCH_LABELS.get(b, b).replace("\n", " ")
        ax.plot(xs[1:], ys[1:], linewidth=2.5, color=LINE_COLORS.get(b, "#777777"),
                label=f"{label}: {ys[-1]:.0f}% ({correct}/{len(recs)})")
    ax.set_xlabel("progress through the benchmark (% of problems attempted)")
    ax.set_ylabel("running accuracy (%)")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.6)
    ax.set_title(f"Running accuracy as each benchmark progresses\n{stamp}",
                 fontweight="bold")
    ax.legend(loc="lower right")
    footnote(fig, "The first few points are noisy by construction: with k problems "
                  "attempted, one answer moves the running accuracy by 1/k.")
    fig.savefig(os.path.join(OUT_DIR, "Chart_overnight_progress.png"))
    plt.close(fig)


def _chart_times(by_bench, benches, stamp):
    """Solve time over problems that actually finished.

    A timed-out problem contributes its *budget*, not a solve time. Including
    those turns the statistic into a description of the harness: with 17 of 30
    AIME problems hitting the 1200 s cap, the median "solve time" would be
    exactly 1200 s. They are reported separately, as a count.
    """
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    labels, medians, p90s, maxima = [], [], [], []
    for b in benches:
        recs = by_bench.get(b, [])
        times = sorted(r["elapsed"] for r in recs if r["status"] in ("correct", "wrong"))
        if not times:
            continue
        n_cut = sum(1 for r in recs if r["status"] in ("timeout", "error"))
        cut_note = (f", {n_cut} hit the {BENCH_BUDGETS.get(b, '?')}s cap" if n_cut else "")
        labels.append(f"{BENCH_LABELS.get(b, b)}\n{len(times)} completed{cut_note}")
        medians.append(_median(times))
        p90s.append(times[min(len(times) - 1, int(0.9 * len(times)))])
        maxima.append(times[-1])

    if labels:
        xpos = range(len(labels))
        width = 0.27
        ax.bar([p - width for p in xpos], medians, width, label="median",
               color=SYSTEM["ours"])
        ax.bar(list(xpos), p90s, width, label="90th percentile", color=SYSTEM["previous"])
        ax.bar([p + width for p in xpos], maxima, width, label="slowest",
               color="#b0bec5")
        for bars in ax.containers:
            ax.bar_label(bars, fmt="%.0fs", fontsize=9, fontweight="bold", padding=2)
        headroom(ax, max(maxima), factor=1.34)
        ax.set_xticks(list(xpos))
        ax.set_xticklabels(labels, fontsize=9.5)
    ax.set_ylabel("seconds per problem")
    ax.set_title(f"Solve time over completed problems\n{stamp}", fontweight="bold")
    ax.legend(loc="upper left")
    footnote(fig, "Timed-out problems are excluded: they contribute the per-benchmark "
                  "budget (600 / 900 / 1200 s), not a solve time. Counts shown under "
                  "each group.")
    fig.savefig(os.path.join(OUT_DIR, "Chart_overnight_times.png"))
    plt.close(fig)


def _median(sorted_values: list) -> float:
    n = len(sorted_values)
    mid = n // 2
    if n % 2:
        return sorted_values[mid]
    return (sorted_values[mid - 1] + sorted_values[mid]) / 2


if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else "deepseek-r1:8b"
    generate(model=model)
    print(f"Charts written to {OUT_DIR}")
