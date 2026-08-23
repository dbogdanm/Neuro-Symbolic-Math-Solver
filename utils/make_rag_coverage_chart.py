"""Measure and plot what the knowledge base actually covers, per benchmark.

This is the honest version of "does the RAG stage contribute?". It runs Eq. 1 —
the direct-embedding retrieval — over every problem of every benchmark and
records whether the closest rule falls inside the acceptance threshold. No LLM
is involved, so the measurement is deterministic and takes seconds.

The result is not uniformly flattering, which is the point: the knowledge base
fires on almost every AIME problem, on about half of MATH500, and on *none* of
GSM8K. Grade-school word problems are prose about shopping and ages; they are
mutually similar as text and far from any statement of a mathematical rule. So
GSM8K accuracy is attributable to the Program-of-Thought + SymPy execution path
alone, and the retrieval stage is what carries the competition-level problems.

Writes Charts/Chart_rag_coverage.png and tests/results/rag_coverage.json.

Usage: python utils/make_rag_coverage_chart.py
"""

import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(_ROOT)  # rules_base resolves ./chroma_db_reguli relative to CWD

import matplotlib.pyplot as plt  # noqa: E402
from chart_style import MUTED, SYSTEM, apply, footnote  # noqa: E402

OUT_DIR = os.path.join(_ROOT, "Charts")
DATA_OUT = os.path.join(_ROOT, "tests", "results", "rag_coverage.json")

BENCHMARKS = [
    ("gsm8k", "gsm8k_50.jsonl", "GSM8K\n(first 50)"),
    ("math500", "math500_50.jsonl", "MATH500\n(first 50)"),
    ("aime25", "aime25_30.jsonl", "AIME 2025\n(all 30)"),
]

apply()


def measure() -> dict:
    """Query the vector store once per problem; return per-benchmark stats."""
    import contextlib
    import io

    from rules_base import DIRECT_MAX_DISTANCE, _get_collection

    collection = _get_collection()
    out = {"threshold": DIRECT_MAX_DISTANCE, "space": "cosine", "benchmarks": {}}
    for key, fname, _label in BENCHMARKS:
        path = os.path.join(_ROOT, "tests", "datasets", fname)
        with open(path, encoding="utf-8") as f:
            items = [json.loads(line) for line in f if line.strip()]
        with contextlib.redirect_stdout(io.StringIO()):  # silence per-query logging
            distances = [
                collection.query(query_texts=[it["problem"]], n_results=1)["distances"][0][0]
                for it in items
            ]
        hits = sum(1 for d in distances if d < DIRECT_MAX_DISTANCE)
        ordered = sorted(distances)
        out.setdefault("distances", {})[key] = [round(d, 4) for d in distances]
        out["benchmarks"][key] = {
            "n": len(distances),
            "hits": hits,
            "hit_rate": 100.0 * hits / len(distances),
            "min_distance": round(min(distances), 3),
            "median_distance": round(ordered[len(ordered) // 2], 3),
        }
    return out


def chart(stats: dict) -> None:
    fig, (ax_rate, ax_dist) = plt.subplots(
        1, 2, figsize=(12.0, 4.8), gridspec_kw={"width_ratios": [1, 1.15]}
    )
    keys = [k for k, _f, _l in BENCHMARKS]
    labels = [label for _k, _f, label in BENCHMARKS]
    rates = [stats["benchmarks"][k]["hit_rate"] for k in keys]

    bars = ax_rate.bar(labels, rates, width=0.55,
                       color=[SYSTEM["ours"] if r else SYSTEM["baseline"] for r in rates])
    ax_rate.set_ylim(0, 118)
    ax_rate.set_yticks([0, 20, 40, 60, 80, 100])
    for bar, key in zip(bars, keys, strict=True):
        s = stats["benchmarks"][key]
        ax_rate.annotate(f"{s['hit_rate']:.0f}%\n{s['hits']}/{s['n']}",
                         (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                         ha="center", va="bottom", fontsize=11, fontweight="bold",
                         color=SYSTEM["ours"] if s["hits"] else MUTED)
    ax_rate.set_ylabel("problems with a knowledge-base hit (%)")
    ax_rate.set_title("Retrieval coverage (Eq. 1, direct embedding)", fontweight="bold")

    # Distance distribution: shows *how far* the misses are, not just that they missed.
    threshold = stats["threshold"]
    for key, label, colour in zip(
        keys, labels, [SYSTEM["previous"], SYSTEM["ours"], SYSTEM["external"]], strict=True
    ):
        values = sorted(stats["distances"][key])
        ys = [100.0 * (i + 1) / len(values) for i in range(len(values))]
        ax_dist.plot(values, ys, linewidth=2.5, color=colour,
                     label=label.replace("\n", " "))
    ax_dist.axvline(threshold, color="#c62828", linestyle="--", linewidth=1.5)
    # Set vertically against the rule itself: every horizontal position in this
    # panel is crossed by one of the three curves.
    ax_dist.annotate(f"acceptance threshold {threshold}", (threshold, 50),
                     xytext=(-5, 0), textcoords="offset points", rotation=90,
                     ha="right", va="center", fontsize=9, color="#c62828",
                     bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5})
    ax_dist.set_xlabel("cosine distance to the closest rule")
    ax_dist.set_ylabel("problems within that distance (%)")
    ax_dist.set_ylim(0, 100)
    ax_dist.grid(alpha=0.6)
    ax_dist.legend(loc="lower right")
    ax_dist.set_title("How far the misses actually are", fontweight="bold")

    fig.suptitle(
        "What the 271-rule knowledge base covers: everything on AIME, half of MATH500, "
        "none of GSM8K",
        fontsize=12.5, fontweight="bold",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    footnote(fig, "Deterministic: one vector query per problem, no LLM in the loop. "
                  "GSM8K word problems sit far from every rule statement, so their "
                  "accuracy comes from the PoT + SymPy path, not from retrieval.")
    fig.savefig(os.path.join(OUT_DIR, "Chart_rag_coverage.png"))
    plt.close(fig)


def main() -> None:
    from rules_base import DIRECT_MAX_DISTANCE

    stats = measure()
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DATA_OUT), exist_ok=True)
    with open(DATA_OUT, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    chart(stats)

    print(f"threshold: cosine distance < {DIRECT_MAX_DISTANCE}")
    for key, _fname, label in BENCHMARKS:
        s_ = stats["benchmarks"][key]
        print(f"  {label.splitlines()[0]:10} {s_['hits']:3}/{s_['n']:<3} "
              f"= {s_['hit_rate']:5.1f}%   median distance {s_['median_distance']}")
    print(f"Chart written to {OUT_DIR}; raw distances in {DATA_OUT}")


if __name__ == "__main__":
    main()
