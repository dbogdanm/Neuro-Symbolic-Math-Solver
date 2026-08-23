"""Generate the v3.2.0 engineering charts for the README.

All numbers are wall-clock measurements taken on the reference workstation
(RTX 5070 Ti, Ryzen 5 7600X, 32 GB RAM, Ollama deepseek-r1:8b Q4_K_M) during
the v3.2.0 optimization session. Re-run after updating the DATA block.

These figures describe *engineering* changes to the pipeline, on a two-problem
diagnostic suite. They are single runs and are labelled as such: they show that
a failure mode was removed, not that accuracy improved by a measurable margin.
The accuracy claims live in the overnight benchmark figures
(utils/make_overnight_charts.py), which cover 130 problems.

Requires matplotlib (dev-only dependency, not needed by the app):
    pip install matplotlib

Usage (from the project root):
    python utils/make_charts_v32.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt  # noqa: E402
from chart_style import MUTED, STATUS, SYSTEM, apply, footnote, headroom  # noqa: E402

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Charts")

apply()

# --------------------------------------------------------------------------- #
# DATA (measured)
# --------------------------------------------------------------------------- #

# Head-to-head on the two-problem "hard suite":
#   P1 = infinite power tower x^x^x^... = 4  (semantic trap, KB hit)
#   P2 = count n <= 10^6 with S(n) = S(2n)   (requires real computation, KB miss)
# Each entry: (seconds, outcome, note) with outcome in {"correct", "wrong", "dnf"}
# or None for a configuration that was not run.
SYSTEMS = [
    ("Raw DeepSeek-R1 8B\n(no pipeline)", "baseline"),
    ("v3.1.0 pipeline\n(previous code)", "previous"),
    ("v3.2.0 pipeline\n(this release)", "ours"),
]

HEAD_TO_HEAD = {
    "P1": {
        "Raw DeepSeek-R1 8B\n(no pipeline)": (580.0, "dnf", "still thinking\nwhen killed"),
        "v3.1.0 pipeline\n(previous code)": None,   # run interrupted, no result recorded
        "v3.2.0 pipeline\n(this release)": (55.2, "correct", "direct RAG hit,\n1 PoT attempt"),
    },
    "P2": {
        # Not run: a raw model cannot brute-force 10^6 candidates in its head,
        # so there is no baseline number to report rather than a missing one.
        "Raw DeepSeek-R1 8B\n(no pipeline)": None,
        "v3.1.0 pipeline\n(previous code)": (48.3, "correct", "1 PoT attempt"),
        "v3.2.0 pipeline\n(this release)": (133.4, "correct", "incl. 1 self-\ncorrection round"),
    },
}

PROBLEMS = [
    # Rendered as a tower-of-exponents *notation* rather than a literal nested
    # superscript: at three levels of nesting matplotlib's mathtext shrinks the
    # innermost term below legible size in a figure this wide.
    ("P1", "P1 - power tower trap\n$x^{x^{x^{\\ldots}}} = 4$  (no real solution)"),
    ("P2", "P2 - digit-sum count\n$S(n) = S(2n),\\ n \\leq 10^6$  (answer 65,063)"),
]

# Sandbox executor: per-execution overhead (smoke-test measurements, mean of 20
# executions after warm-up). The v3.1.0 figure is dominated by re-importing
# SymPy in a fresh interpreter; the v3.2.0 figure is queue round-trip only.
SANDBOX = {
    "v3.1.0: fresh process\nper execution": 0.36,
    "v3.2.0: persistent\nwarm worker": 0.0011,
}
# Self-correction attempts per problem, worst case (see max_retries in
# neuro_symbolic.run_neuro_symbolic_pipeline). The sandbox overhead is paid once
# per attempt, which is what makes it worth removing at all.
MAX_ATTEMPTS = 3

OUTCOME_STYLE = {
    "correct": (STATUS["correct"], "correct"),
    "wrong": (STATUS["wrong"], "wrong answer"),
    "dnf": (STATUS["error"], "no answer (DNF)"),
}


def chart_head_to_head():
    """One panel per problem, with every system on the x axis of both.

    Keeping all three categories on both panels — with an explicit "not run"
    marker where a cell is empty — means a given x position denotes the same
    system in both panels. Dropping the empty cells instead would silently
    shift the categories and invite a left-to-right misreading.
    """
    names = [n for n, _ in SYSTEMS]
    colours = [SYSTEM[role] for _, role in SYSTEMS]

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6))
    for ax, (key, title) in zip(axes, PROBLEMS, strict=True):
        cells = HEAD_TO_HEAD[key]
        heights = [cells[n][0] if cells[n] else 0.0 for n in names]
        bars = ax.bar(range(len(names)), heights, width=0.55, color=colours)
        headroom(ax, max(heights), factor=1.42)

        for i, (bar, name) in enumerate(zip(bars, names, strict=True)):
            cell = cells[name]
            if cell is None:
                ax.annotate("not run", (i, 0), xytext=(0, 8),
                            textcoords="offset points", ha="center",
                            fontsize=9.5, style="italic", color=MUTED)
                continue
            secs, outcome, note = cell
            colour, text = OUTCOME_STYLE[outcome]
            suffix = "+" if outcome == "dnf" else ""
            ax.annotate(
                f"{secs:.0f}s{suffix} - {text}\n{note}",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=colour,
            )
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, fontsize=9)
        ax.set_title(title, fontsize=11)
        ax.set_ylabel("wall-clock time (s)")

    fig.suptitle(
        "Diagnostic suite: does the pipeline reach an answer at all?\n"
        "Single runs - the outcome is the signal; the times are context, not a benchmark",
        fontsize=12, fontweight="bold",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    footnote(fig, "P1 is a trap with no real solution; P2 needs a value no language model "
                  "can recall (65,063). On P2 v3.2.0 is slower than v3.1.0 because it spent "
                  "a self-correction round - both reach the exact count.")
    fig.savefig(os.path.join(OUT_DIR, "Chart_v32_head_to_head.png"))
    plt.close(fig)


def chart_sandbox():
    """Per-execution overhead, on a linear axis, in context.

    Deliberately not a log-scale bar chart: on a log axis a bar's length is set
    by the lower limit of the axis rather than by the value, so the ratio being
    claimed is not the ratio the reader sees.
    """
    names = list(SANDBOX)
    vals = [SANDBOX[n] for n in names]
    worst = [v * MAX_ATTEMPTS for v in vals]
    speedup = vals[0] / vals[1]

    fig, ax = plt.subplots(figsize=(9.0, 3.8))
    ypos = range(len(names))
    ax.barh([p + 0.19 for p in ypos], vals, height=0.34,
            color=[SYSTEM["previous"], SYSTEM["ours"]], label="one execution")
    ax.barh([p - 0.19 for p in ypos], worst, height=0.34, alpha=0.42,
            color=[SYSTEM["previous"], SYSTEM["ours"]],
            label=f"worst case ({MAX_ATTEMPTS} self-correction attempts)")
    for p, v, w in zip(ypos, vals, worst, strict=True):
        ax.annotate(f"  {v * 1000:.0f} ms" if v < 0.01 else f"  {v:.2f} s",
                    (v, p + 0.19), va="center", fontsize=10, fontweight="bold")
        ax.annotate(f"  {w * 1000:.0f} ms" if w < 0.01 else f"  {w:.2f} s",
                    (w, p - 0.19), va="center", fontsize=9.5, color=MUTED)
    ax.set_yticks(list(ypos))
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlim(0, max(worst) * 1.22)
    ax.set_xlabel("overhead per PoT execution (s)")
    ax.legend(loc="upper right")
    # Rounded to one significant figure on purpose: the warm-worker measurement
    # is ~1 ms, so quoting "327x" would claim three digits of precision that the
    # input does not carry.
    rounded = round(speedup, -2)
    ax.set_title(
        f"SymPy sandbox: a warm worker removes ~{rounded:.0f}x of the execution overhead",
        fontweight="bold",
    )
    footnote(fig, "Latency only, and a small share of it: a problem takes 39-93 s at the "
                  "median, so this removes well under 1% of end-to-end time. It matters "
                  "because it made the executor's cost independent of retry count.")
    fig.savefig(os.path.join(OUT_DIR, "Chart_v32_sandbox.png"))
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    chart_head_to_head()
    chart_sandbox()
    print(f"Charts written to {OUT_DIR}")
