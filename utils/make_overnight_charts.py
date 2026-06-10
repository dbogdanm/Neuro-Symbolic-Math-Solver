"""Charts for the overnight benchmark run (regenerated after every problem).

Reads tests/results/overnight_results.jsonl and writes to Charts/:
  - Chart_overnight_results.png   (per-benchmark outcome breakdown + accuracy)
  - Chart_overnight_progress.png  (cumulative correct answers per benchmark)
  - Chart_overnight_times.png     (per-benchmark solve-time statistics)

Usage: python utils/make_overnight_charts.py   (or import generate())
"""

import json
import os
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(_ROOT, "Charts")
DEFAULT_RESULTS = os.path.join(_ROOT, "tests", "results", "overnight_results.jsonl")

BENCH_LABELS = {
    "gsm8k": "GSM8K\n(first 50)",
    "math500": "MATH500\n(first 50)",
    "aime25": "AIME 2025\n(all 30)",
}
BENCH_TOTALS = {"gsm8k": 50, "math500": 50, "aime25": 30}
STATUS_ORDER = ["correct", "wrong", "timeout", "error"]
STATUS_COLORS = {
    "correct": "#2e7d32", "wrong": "#c62828",
    "timeout": "#f9a825", "error": "#8d6e63",
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
})


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


def _stamp(done: int, total: int) -> str:
    state = "FINAL" if done >= total else f"in progress — {done}/{total} problems"
    return f"{state} · {time.strftime('%Y-%m-%d %H:%M')}"


def generate(model: str = "deepseek-r1:8b", results_path: str = DEFAULT_RESULTS) -> None:
    by_bench = _load(results_path, model)
    benches = list(BENCH_TOTALS)  # always show all benchmarks, even before they start
    done = sum(len(v) for v in by_bench.values())
    total = sum(BENCH_TOTALS.values())
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- outcomes + accuracy ------------------------------------------------
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    bottoms = [0] * len(benches)
    for status in STATUS_ORDER:
        vals = [sum(1 for r in by_bench.get(b, []) if r["status"] == status)
                for b in benches]
        ax.bar([BENCH_LABELS.get(b, b) for b in benches], vals, bottom=bottoms,
               color=STATUS_COLORS[status], width=0.55, label=status)
        bottoms = [b + v for b, v in zip(bottoms, vals, strict=True)]

    for i, b in enumerate(benches):
        recs = by_bench.get(b, [])
        n = len(recs)
        n_total = BENCH_TOTALS.get(b, n)
        correct = sum(1 for r in recs if r["status"] == "correct")
        if n:
            acc = 100.0 * correct / n
            ax.annotate(
                f"{acc:.0f}%\n({correct}/{n} graded)",
                (i, bottoms[i]), ha="center", va="bottom",
                fontsize=11, fontweight="bold", color="#1b5e20",
            )
        if n < n_total:
            ax.annotate(f"{n}/{n_total} run", (i, 0), ha="center", va="bottom",
                        fontsize=9, color="#555555")
    ax.set_ylabel("problems")
    ax.set_title(
        f"{model} + neuro-symbolic pipeline (v3.2) — overnight benchmark\n"
        f"{_stamp(done, total)}",
        fontsize=12, fontweight="bold",
    )
    ax.legend(loc="upper right", frameon=False)
    ax.margins(y=0.35)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "Chart_overnight_results.png"), bbox_inches="tight")
    plt.close(fig)

    # ---- cumulative correct-answer progress per benchmark --------------------
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    line_colors = {"gsm8k": "#5c6bc0", "math500": "#00897b", "aime25": "#e65100"}
    for b in benches:
        recs = by_bench.get(b, [])
        cum = [0]
        for r in recs:
            cum.append(cum[-1] + (1 if r["status"] == "correct" else 0))
        label = BENCH_LABELS.get(b, b).replace("\n", " ")
        ax.plot(range(len(cum)), cum, linewidth=2.5,
                color=line_colors.get(b, "#777777"),
                marker="o", markersize=3,
                label=f"{label}: {cum[-1]} correct / {len(recs)} run "
                      f"(of {BENCH_TOTALS.get(b, '?')})")
    ax.set_xlabel("problems attempted (in benchmark order)")
    ax.set_ylabel("cumulative correct answers")
    ax.set_xlim(0, max(BENCH_TOTALS.values()))
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.25)
    ax.set_title(f"Correct answers as the run progresses — {_stamp(done, total)}",
                 fontsize=12, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "Chart_overnight_progress.png"), bbox_inches="tight")
    plt.close(fig)

    # ---- times ---------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    labels, avgs, medians, maxima = [], [], [], []
    for b in benches:
        times = sorted(r["elapsed"] for r in by_bench.get(b, []))
        if not times:
            continue
        labels.append(BENCH_LABELS.get(b, b))
        avgs.append(sum(times) / len(times))
        medians.append(times[len(times) // 2])
        maxima.append(times[-1])
    if labels:
        xpos = range(len(labels))
        width = 0.27
        ax.bar([p - width for p in xpos], avgs, width, label="mean", color="#5c6bc0")
        ax.bar(list(xpos), medians, width, label="median", color="#00897b")
        ax.bar([p + width for p in xpos], maxima, width, label="max", color="#b0bec5")
        for bars in ax.containers:
            ax.bar_label(bars, fmt="%.0fs", fontsize=9, fontweight="bold")
        ax.set_xticks(list(xpos))
        ax.set_xticklabels(labels)
    ax.set_ylabel("seconds per problem")
    ax.set_title(f"Solve time per problem — {_stamp(done, total)}",
                 fontsize=12, fontweight="bold")
    ax.legend(loc="upper left", frameon=False)
    ax.margins(y=0.2)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "Chart_overnight_times.png"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    import sys
    model = sys.argv[1] if len(sys.argv) > 1 else "deepseek-r1:8b"
    generate(model=model)
    print(f"Charts written to {OUT_DIR}")
