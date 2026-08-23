"""Render the pipeline architecture diagram from the actual control flow.

Kept as a script rather than a hand-drawn image so the figure and the code can
be checked against each other. Every box below corresponds to a named function
in `neuro_symbolic.py`; the mapping is in NODE_SOURCE and is printed when this
script runs, so a drifted diagram is visible rather than silent.

The colour axis is the one that matters for a neuro-symbolic system: blue =
a stage that calls the language model, teal = a stage that is fully
deterministic. The point of the architecture is how little of it is blue.

Writes Charts/Architecture.png and Charts/Architecture.svg (vector, for LaTeX).

Usage: python utils/make_architecture_diagram.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.patches as mpatches  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from chart_style import apply  # noqa: E402

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Charts")

apply()

# Where each box lives in the source. Printed on every run as a drift check.
NODE_SOURCE = {
    "fast path": "neuro_symbolic.is_simple_math / solve_simple_math",
    "semantic parse": "neuro_symbolic.step1_semantic_parser",
    "retrieval": "neuro_symbolic.get_rag_hint",
    "vector store": "rules_base.find_hints (ChromaDB, local disk, cosine)",
    "type classifier": "neuro_symbolic.extract_problem_type (token-capped)",
    "web search": "web_search.get_web_hint (DuckDuckGo)",
    "program-of-thought": "neuro_symbolic.step2_pot_generator",
    "validate": "neuro_symbolic.step3_code_validator",
    "execute": "neuro_symbolic._SandboxWorker.execute / sandbox_runner",
    "self-correction": "run_neuro_symbolic_pipeline retry loop (max_retries = 3)",
    "fallback": "run_neuro_symbolic_pipeline tail + neuro_symbolic.extract_boxed",
}

# Palette: the neural/symbolic split is the message.
NEURAL = ("#e3f2fd", "#1565c0")        # calls the LLM
SYMBOLIC = ("#d7f0ec", "#00695c")      # deterministic, no LLM
IO = ("#ffe9d6", "#e65100")            # problem in, answer out
NETWORK = ("#fff4d6", "#ef6c00")       # leaves the machine

FLOW = "#455a64"
ERR = "#c62828"
FAST = "#00695c"

_HEAD = {"arrowstyle": "-|>,head_width=0.17,head_length=0.32"}


def box(ax, x, y, w, h, title, body="", palette=SYMBOLIC, dashed=False, fontsize=9.5):
    fill, edge = palette
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor=fill, edgecolor=edge, linewidth=1.7,
        linestyle="--" if dashed else "-", zorder=3,
    ))
    cx = x + w / 2
    if body:
        ax.text(cx, y + h * 0.70, title, ha="center", va="center",
                fontsize=fontsize, fontweight="bold", color=edge, zorder=4)
        ax.text(cx, y + h * 0.30, body, ha="center", va="center",
                fontsize=fontsize - 1.4, color="#37474f", zorder=4, linespacing=1.35)
    else:
        ax.text(cx, y + h / 2, title, ha="center", va="center",
                fontsize=fontsize, fontweight="bold", color=edge, zorder=4)
    return {"x": x, "y": y, "w": w, "h": h,
            "cx": cx, "cy": y + h / 2,
            "l": (x, y + h / 2), "r": (x + w, y + h / 2),
            "t": (cx, y + h), "b": (cx, y)}


def route(ax, points, colour=FLOW, dashed=False, head=True, width=1.6):
    """Draw an orthogonal poly-line through ``points``, arrowhead at the end.

    Every connector in this diagram is axis-aligned. Diagonals across a dense
    figure read as crossings even when nothing crosses, so the router only ever
    emits horizontal and vertical segments and the caller supplies the corners.
    """
    style = "--" if dashed else "-"
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs[:-1] + [xs[-1]], ys[:-1] + [ys[-1]], color=colour, linewidth=width,
            linestyle=style, solid_capstyle="round", zorder=1)
    if head:
        ax.add_patch(mpatches.FancyArrowPatch(
            points[-2], points[-1], color=colour, linewidth=width,
            linestyle=style, zorder=2, **_HEAD))


def label(ax, x, y, text, colour=FLOW, fontsize=8.4, weight="normal", ha="center"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=fontsize, color=colour,
            fontweight=weight, zorder=5,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.6})


def build():
    fig, ax = plt.subplots(figsize=(15.6, 9.9))
    ax.set_xlim(0, 15.6)
    ax.set_ylim(0, 9.9)
    ax.axis("off")

    # ---- main row ------------------------------------------------------------
    my, mh = 5.85, 1.25
    prob = box(ax, 0.25, my, 1.75, mh, "Problem", "natural language", IO)
    parse = box(ax, 3.05, my, 2.25, mh, "1. Semantic parse",
                "LLM $\\rightarrow$ JSON:\nvariables, constraints, goal", NEURAL)
    pot = box(ax, 6.10, my, 2.35, mh, "2. Program-of-Thought",
              "LLM $\\rightarrow$ SymPy program,\nprompted with P $\\oplus$ H", NEURAL)
    val = box(ax, 9.25, my, 1.85, mh, "3. Validate",
              "extract code block,\nrequire final_result", SYMBOLIC)
    ex = box(ax, 11.90, my, 2.05, mh, "4. Execute",
             "persistent SymPy worker,\nseparate process, 120 s", SYMBOLIC)
    ans = box(ax, 14.75 - 0.35, my, 1.15, mh, "Answer", "", IO)

    for a, b in ((prob, parse), (parse, pot), (pot, val), (val, ex), (ex, ans)):
        route(ax, [a["r"], b["l"]])

    # ---- parallel retrieval branch --------------------------------------------
    ry = 3.95
    rag = box(ax, 3.05, ry, 2.25, mh, "1'. Retrieval (Eq. 1)",
              "embed the problem text,\nquery the vector store", SYMBOLIC)
    fork_x = 2.52
    # Stage 1 and stage 1' are submitted to one ThreadPoolExecutor and joined
    # before stage 2, so the flow forks here and re-joins under the generator.
    route(ax, [(fork_x, my + mh / 2), (fork_x, rag["cy"]), rag["l"]])
    label(ax, fork_x - 0.12, 5.05, "run in\nparallel", fontsize=8.2, ha="right")
    join_x = pot["cx"]
    route(ax, [rag["r"], (join_x, rag["cy"]), (join_x, my)])
    label(ax, join_x + 0.62, rag["cy"] + 0.30, "hints H")

    # ---- retrieval cascade ------------------------------------------------------
    cy, ch = 1.75, 1.05
    db = box(ax, 0.25, cy, 2.30, ch, "Vector store",
             "271 rules, ChromaDB\non local disk (cosine)", SYMBOLIC, fontsize=9)
    cls = box(ax, 3.30, cy, 2.30, ch, "Type classifier",
              "LLM, 2048-token cap\n(only after a miss)", NEURAL, fontsize=9)
    web = box(ax, 6.35, cy, 2.30, ch, "Web search",
              "DuckDuckGo\n(last resort)", NETWORK, fontsize=9)

    route(ax, [rag["b"], (rag["cx"], cy + ch + 0.45), (db["cx"], cy + ch + 0.45), db["t"]])
    route(ax, [db["r"], cls["l"]])
    route(ax, [cls["r"], web["l"]])
    label(ax, (db["r"][0] + cls["l"][0]) / 2, cy + ch / 2 + 0.26, "miss")
    label(ax, (cls["r"][0] + web["l"][0]) / 2, cy + ch / 2 + 0.26, "miss")
    label(ax, db["x"], cy + ch + 0.72, "cascade - the first hit wins", ha="left",
          fontsize=8.4)

    # ---- self-correction loop -----------------------------------------------------
    loop_y = 7.85
    route(ax, [val["t"], (val["cx"], loop_y), (pot["cx"] + 0.55, loop_y),
               (pot["cx"] + 0.55, my + mh)], colour=ERR)
    route(ax, [ex["t"], (ex["cx"], loop_y - 0.55), (pot["cx"] - 0.55, loop_y - 0.55),
               (pot["cx"] - 0.55, my + mh)], colour=ERR)
    label(ax, (pot["cx"] + val["cx"]) / 2 + 0.4, loop_y + 0.26,
          "self-correction - regenerate from the error, keeping the same "
          "P $\\oplus$ H context (3 attempts total)",
          colour=ERR, fontsize=8.8, weight="bold")
    label(ax, val["cx"] + 0.62, my + mh + 0.52, "invalid", colour=ERR, fontsize=8.2)
    label(ax, ex["cx"] + 0.72, my + mh + 0.30, "error / timeout", colour=ERR, fontsize=8.2)

    # ---- final fallback -------------------------------------------------------------
    fb = box(ax, 9.55, ry, 3.20, mh, "Fallback: direct reasoning",
             "same model, no program;\nanswer read from \\boxed{}", NEURAL)
    # Enter from above (the retry loop gave up), leave to the right (into the
    # same answer node the main path reaches) — never back across the box.
    drop_y = my - 0.42
    route(ax, [ex["b"], (ex["cx"], drop_y), (fb["cx"], drop_y), fb["t"]], colour=ERR)
    label(ax, (ex["cx"] + fb["cx"]) / 2, drop_y + 0.02, "all 3 attempts failed",
          colour=ERR, fontsize=8.2)
    route(ax, [fb["r"], (ans["cx"], fb["cy"]), (ans["cx"], my)], colour=ERR)

    # ---- fast path ---------------------------------------------------------------------
    fast_y = 9.05
    fast = box(ax, 5.20, fast_y - 0.40, 5.20, 0.80,
               "Fast path: pure arithmetic / basic algebra",
               "solved by SymPy directly - no LLM, no retrieval",
               SYMBOLIC, dashed=True, fontsize=9)
    route(ax, [prob["t"], (prob["cx"], fast_y), (fast["x"], fast_y)], colour=FAST)
    route(ax, [(fast["x"] + fast["w"], fast_y), (ans["cx"], fast_y),
               (ans["cx"], my + mh)], colour=FAST)

    # ---- legend -------------------------------------------------------------------------
    legend = [
        (NEURAL, "calls the language model"),
        (SYMBOLIC, "deterministic - no language model"),
        (IO, "problem in / answer out"),
        (NETWORK, "leaves the machine"),
    ]
    for i, ((fill, edge), text) in enumerate(legend):
        lx = 0.30 + i * 3.85
        ax.add_patch(mpatches.FancyBboxPatch(
            (lx, 0.62), 0.36, 0.28, boxstyle="round,pad=0.01,rounding_size=0.07",
            facecolor=fill, edgecolor=edge, linewidth=1.5, zorder=3))
        ax.text(lx + 0.52, 0.76, text, ha="left", va="center", fontsize=9.2,
                color="#37474f")

    ax.text(7.8, 9.80,
            "Neuro-symbolic pipeline: control flow as implemented in neuro_symbolic.py",
            ha="center", va="top", fontsize=13.5, fontweight="bold", color="#212121")
    ax.text(0.30, 0.20,
            "Everything runs on one machine by default (Ollama and ChromaDB on local "
            "disk). The provider layer is Bring-Your-Own-Key: selecting a cloud model "
            "routes every LLM call there for the whole run - there is no separate cloud "
            "fallback stage.",
            ha="left", va="center", fontsize=8.6, color="#616161")

    fig.tight_layout(pad=0.2)
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT_DIR, f"Architecture.{ext}"))
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    build()
    print("Diagram nodes and their implementation:")
    for node, source in NODE_SOURCE.items():
        print(f"  {node:20} {source}")
    print(f"\nWritten to {OUT_DIR}/Architecture.png and .svg")
