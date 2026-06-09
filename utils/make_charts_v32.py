"""Generate the v3.2.0 progress charts for the README.

All numbers are wall-clock measurements taken on the reference workstation
(RTX 5070 Ti, Ryzen 5 7600X, 32 GB RAM, Ollama deepseek-r1:8b Q4_K_M) during
the v3.2.0 optimization session. Re-run after updating the DATA block.

Requires matplotlib (dev-only dependency, not needed by the app):
    pip install matplotlib

Usage (from the project root):
    python utils/make_charts_v32.py
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Charts")

# --------------------------------------------------------------------------- #
# DATA (measured)
# --------------------------------------------------------------------------- #

# Head-to-head on the two-problem "hard suite":
#   P1 = infinite power tower x^x^x^... = 4  (semantic-trap, KB hit)
#   P2 = count n <= 10^6 with S(n) = S(2n)   (requires real computation, KB miss)
# Each entry: (seconds, outcome, note) with outcome in {"correct", "wrong", "dnf"}.
# Single-run LLM timings carry high variance (thinking length, retry luck);
# outcomes are the hard signal, the notes give the run context.
HEAD_TO_HEAD = {
    "Raw DeepSeek-R1 8B\n(no pipeline)": {
        "P1": (580.0, "dnf", "still thinking\nwhen killed"),
        "P2": (None, None, None),  # not run: cannot brute-force 10^6 mentally
    },
    "v3.1.0 pipeline\n(previous code)": {
        "P1": (None, None, None),  # run interrupted, no result recorded
        "P2": (48.3, "correct", "1 PoT attempt"),
    },
    "v3.2.0 pipeline\n(this release)": {
        "P1": (55.2, "correct", "direct RAG hit,\n1 PoT attempt"),
        "P2": (133.4, "correct", "incl. 1 self-\ncorrection round"),
    },
}

# Sandbox executor: per-execution overhead (smoke-test measurements).
SANDBOX = {
    "v3.1.0: spawn a fresh\nprocess per execution": 0.36,
    "v3.2.0: persistent\nwarm worker": 0.001,
}

# Retrieval stage: LLM round-trips required before the vector query.
#   v3.1.0 always runs an LLM problem-type classification first (observed
#   stalling >600 s on a hard problem when the reasoning model rabbit-holed);
#   v3.2.0 embeds the raw problem text directly (Eq. 1) — measured 0.12 s on
#   a KB hit — and only falls back to a 2048-token-capped classifier on miss.
RETRIEVAL_CALLS = {
    "v3.1.0: classify with LLM,\nthen query vector DB": 1,
    "v3.2.0: embed problem text\ndirectly (Eq. 1)": 0,
}

OUTCOME_STYLE = {
    "correct": ("#2e7d32", "correct"),
    "wrong": ("#c62828", "wrong answer"),
    "dnf": ("#8d6e63", "no answer (DNF)"),
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
})


def chart_head_to_head():
    systems = list(HEAD_TO_HEAD.keys())
    problems = [
        ("P1", "P1 — power tower trap\n$x^{x^{x^{\\cdots}}} = 4$"),
        ("P2", "P2 — digit-sum count\n$S(n) = S(2n),\\ n \\leq 10^6$"),
    ]
    colors = ["#9e9e9e", "#5c6bc0", "#00897b"]

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.0), sharey=True)
    for ax, (key, title) in zip(axes, problems, strict=True):
        xs, heights, bar_colors, outcomes, notes = [], [], [], [], []
        for i, sys_name in enumerate(systems):
            secs, outcome, note = HEAD_TO_HEAD[sys_name][key]
            if secs is None:
                continue
            xs.append(i)
            heights.append(secs)
            bar_colors.append(colors[i])
            outcomes.append(outcome)
            notes.append(note or "")
        bars = ax.bar([systems[i] for i in xs], heights, color=bar_colors, width=0.55)
        for bar, outcome, note in zip(bars, outcomes, notes, strict=True):
            color, text = OUTCOME_STYLE[outcome]
            suffix = "+" if outcome == "dnf" else ""
            ax.annotate(
                f"{bar.get_height():.0f}s{suffix} — {text}\n{note}",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=color,
            )
        ax.set_title(title, fontsize=11)
        ax.set_ylabel("wall-clock time (s)")
        ax.margins(y=0.32)
        ax.tick_params(axis="x", labelsize=9)
    fig.suptitle(
        "Hard-problem suite: total time to answer (single runs — outcomes are the hard signal,\n"
        "wall-clock varies with reasoning length and self-correction rounds)",
        fontsize=11.5, fontweight="bold",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(os.path.join(OUT_DIR, "Chart_v32_head_to_head.png"), bbox_inches="tight")
    plt.close(fig)


def chart_sandbox():
    fig, ax = plt.subplots(figsize=(8, 3.2))
    names = list(SANDBOX.keys())
    vals = [SANDBOX[n] for n in names]
    bars = ax.barh(names, vals, color=["#5c6bc0", "#00897b"], height=0.5)
    ax.set_xscale("log")
    ax.set_xlabel("overhead per PoT execution (s, log scale)")
    for bar, v in zip(bars, vals, strict=True):
        ax.annotate(f" {v*1000:.0f} ms" if v < 0.01 else f" {v:.2f} s",
                    (v, bar.get_y() + bar.get_height() / 2),
                    va="center", fontsize=10, fontweight="bold")
    speedup = vals[0] / vals[1]
    ax.set_title(
        f"SymPy sandbox: persistent warm worker — ~{speedup:,.0f}× less overhead per execution\n"
        "(paid on every attempt of the self-correction loop)",
        fontsize=11, fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "Chart_v32_sandbox.png"), bbox_inches="tight")
    plt.close(fig)


def chart_retrieval():
    fig, ax = plt.subplots(figsize=(8.5, 3.4))
    names = list(RETRIEVAL_CALLS.keys())
    vals = [RETRIEVAL_CALLS[n] for n in names]
    bars = ax.barh(names, vals, color=["#5c6bc0", "#00897b"], height=0.5)
    ax.set_xlabel("LLM round-trips required before the vector query (KB-hit problem)")
    ax.set_xticks([0, 1])
    ax.set_xlim(0, 1.35)
    ax.annotate("  measured: 0.12 s retrieval, zero LLM calls",
                (0.02, bars[1].get_y() + bars[1].get_height() / 2),
                va="center", fontsize=10, fontweight="bold", color="#00695c")
    ax.annotate("  observed stalling >600 s when the reasoning\n"
                "  model rabbit-holed on the classification",
                (1.02, bars[0].get_y() + bars[0].get_height() / 2),
                va="center", fontsize=9, color="#3949ab")
    ax.set_title(
        "Semantic RAG: querying ChromaDB directly with the problem embedding (Eq. 1)\n"
        "removes the LLM classification round-trip from the retrieval hot path",
        fontsize=11, fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "Chart_v32_rag_retrieval.png"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    chart_head_to_head()
    chart_sandbox()
    chart_retrieval()
    print(f"Charts written to {OUT_DIR}")
