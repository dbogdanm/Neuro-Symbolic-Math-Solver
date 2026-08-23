"""Answer grading for the benchmark harness (no LLM, no I/O).

The pipeline answers with whatever SymPy prints, while the benchmark labels are
written in LaTeX by hand. Comparing them requires normalizing both sides onto a
common syntax before any numeric comparison:

* ``\\frac``/``\\sqrt`` are expanded to plain arithmetic, innermost group first,
  so nested LaTeX such as ``\\frac{\\sqrt{3}}{3}`` collapses correctly;
* SymPy's imaginary unit ``I`` and explicit ``*`` are folded onto the bare ``i``
  the labels use, so ``6 - 5*I`` matches ``6 - 5i``;
* list/set wrappers are stripped and solution sets are compared without order,
  so ``[3, 5, 7]`` matches ``3, 5, 7`` and ``[-2, 1]`` matches ``1,-2``;
* an answer-shell prefix (``x =``, ``The answer is``, ``\\boxed``) is removed.

Kept in its own module so both the live harness and ``tests/regrade.py`` share
exactly one implementation — a benchmark whose grader drifts between the run
and the re-analysis is not reproducible.
"""

import re
from fractions import Fraction

# Matches one LaTeX command whose arguments contain no further braces, i.e. the
# innermost one. Applied repeatedly, this peels nesting from the inside out.
_LATEX_PATTERNS = (
    (re.compile(r"\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}"), r"((\1)/(\2))"),
    (re.compile(r"\\[dt]?frac\s*(\d)\s*(\d)"), r"((\1)/(\2))"),
    (re.compile(r"\\sqrt\s*\[([^\[\]]*)\]\s*\{([^{}]*)\}"), r"((\2)**(1/(\1)))"),
    (re.compile(r"\\sqrt\s*\{([^{}]*)\}"), r"sqrt(\1)"),
    (re.compile(r"\\sqrt\s*(\d+)"), r"sqrt(\1)"),
)

_TEXT_CMD = re.compile(r"\\(?:text|mbox|textbf|textrm|mathrm|operatorname)\s*\{([^{}]*)\}")
_ANSWER_PREFIX = re.compile(
    r"^\s*(?:the\s+)?(?:answers?|solutions?|results?|values?)\s*(?:is|are|:|=)\s*",
    re.IGNORECASE,
)
# A leading binding such as "x =" or "f(x) =", but never "==" or "<=".
_BINDING_PREFIX = re.compile(r"^\s*[a-zA-Z][a-zA-Z0-9_]*\s*(?:\([^()]*\))?\s*=\s*(?=[^=])")
_THOUSANDS = re.compile(r"(?<=\d),(?=\d{3}\b)")
_BARE_I = re.compile(r"(?<![A-Za-z])I(?![A-Za-z])")
_IMPLICIT_MUL = re.compile(r"(?<=[\d)])(?=[a-z(])")

_TOLERANCE = 1e-4


def _expand_latex(s: str) -> str:
    """Rewrite ``\\frac``/``\\sqrt`` into plain syntax, innermost group first.

    A single pass cannot handle nesting: in ``\\frac{\\sqrt{3}}{3}`` the first
    argument itself contains braces, which a ``[^{}]*`` group can never match.
    Looping until the text stops changing rewrites one nesting level per pass.
    """
    for _ in range(12):  # bounded; each pass removes at least one command
        before = s
        for pattern, replacement in _LATEX_PATTERNS:
            s = pattern.sub(replacement, s)
        if s == before:
            break
    return s


def _strip_shell(s: str) -> str:
    """Remove answer-shell decoration from around the value itself."""
    s = re.sub(r"\\boxed\s*\{", "{", s)
    s = _ANSWER_PREFIX.sub("", s)
    s = _BINDING_PREFIX.sub("", s)
    return s.strip()


def _wraps_whole(s: str) -> bool:
    """True when the leading bracket's partner is the very last character.

    Distinguishes a wrapper — ``[5]`` — from an expression that merely starts
    and ends with brackets, such as ``(3)/(2)``, which must not be unwrapped.
    """
    if len(s) < 2 or (s[0], s[-1]) not in (("(", ")"), ("[", "]")):
        return False
    depth = 0
    for k, ch in enumerate(s):
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
            if depth == 0:
                return k == len(s) - 1
    return False


def normalize_answer(s: str) -> str:
    """Best-effort normalization of a LaTeX/SymPy answer string."""
    s = str(s).strip()
    s = s.replace("$", "").replace("\\!", "").replace("\\,", " ").replace("\\;", " ")
    s = s.replace("\\left", "").replace("\\right", "")
    s = _TEXT_CMD.sub(r"\1", s)
    s = _strip_shell(s)
    s = _expand_latex(s)
    s = s.replace("\\pi", "pi").replace("\\cdot", "*").replace("\\times", "*")
    s = s.replace("\\div", "/").replace("\\infty", "oo")
    s = s.replace("^\\circ", "").replace("\\circ", "").replace("\u00b0", "")
    s = s.replace("\\%", "").replace("%", "")
    s = s.replace("\\dots", "").replace("\\ldots", "").replace("\\cdots", "")
    s = _THOUSANDS.sub("", s)
    s = s.replace("{", "(").replace("}", ")")
    # SymPy prints the imaginary unit as "I"; the labels write a bare "i".
    # Fold before lowercasing, so a variable named "i" is left alone.
    s = _BARE_I.sub("i", s)
    s = s.replace(" ", "").rstrip(".").lower()
    s = re.sub(r"(?<=\d)\*(?=i(?![a-z]))", "", s)  # "5*i" -> "5i"
    s = _strip_shell(s)
    # A one-element solution set is just the element: SymPy's solve() returns
    # "[5]" where the label writes "5". Only unwrap when there is no comma, so
    # tuples and intervals keep their brackets for split_list() to handle.
    while "," not in s and _wraps_whole(s):
        s = _strip_shell(s[1:-1])
    return s


def to_number(s: str):
    """Parse a real-valued answer to a float, or None if it is not one."""
    if not s or len(s) > 200:
        return None
    try:
        return float(Fraction(s))
    except (ValueError, ZeroDivisionError, OverflowError):
        pass
    try:
        import sympy as sp
        value = sp.sympify(_IMPLICIT_MUL.sub("*", s))
        if not value.is_number or value.is_real is False:
            return None  # complex values are compared by to_complex()
        return float(value.evalf())
    except Exception:  # noqa: BLE001 - sympify raises a wide range of errors
        return None


def to_complex(s: str):
    """Parse a complex-valued answer to a Python complex, or None."""
    if not s or len(s) > 200:
        return None
    try:
        import sympy as sp
        value = sp.sympify(_IMPLICIT_MUL.sub("*", s), locals={"i": sp.I, "j": sp.I})
        if not value.is_number:
            return None
        return complex(value.evalf())
    except Exception:  # noqa: BLE001 - sympify raises a wide range of errors
        return None


def split_list(s: str):
    """Split a comma-separated answer at depth-0 commas, or None if scalar.

    An optional ``()``/``[]`` wrapper is stripped first, so SymPy's
    ``[3, 5, 7]`` and the label's ``3, 5, 7`` yield the same element list.
    """
    inner = s[1:-1] if len(s) >= 2 and (s[0], s[-1]) in (("(", ")"), ("[", "]")) else s
    if "," not in inner:
        return None
    parts, depth, cur = [], 0, ""
    for ch in inner:
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
    if depth != 0 or any(not part.strip() for part in parts):
        return None
    return parts if len(parts) > 1 else None


def equal_scalar(p: str, g: str) -> bool:
    """Compare two scalar answers numerically, falling back to complex."""
    if p and p == g:
        return True
    pn, gn = to_number(p), to_number(g)
    if pn is not None and gn is not None:
        return abs(pn - gn) <= _TOLERANCE * max(1.0, abs(gn))
    pc, gc = to_complex(p), to_complex(g)
    if pc is not None and gc is not None:
        return abs(pc - gc) <= _TOLERANCE * max(1.0, abs(gc))
    return False


def _equal_as_set(predicted: list, gold: list) -> bool:
    """Match two element lists ignoring order; each label is consumed once."""
    remaining = list(gold)
    for a in predicted:
        for k, b in enumerate(remaining):
            if equal_scalar(a, b):
                del remaining[k]
                break
        else:
            return False
    return True


def grade(predicted: str, gold: str) -> bool:
    """True when ``predicted`` is the same mathematical answer as ``gold``."""
    p, g = normalize_answer(predicted), normalize_answer(gold)
    if p and p == g:
        return True
    pt, gt = split_list(p), split_list(g)
    if pt is not None and gt is not None:
        if len(pt) != len(gt):
            return False
        # Ordered first (covers coordinate pairs, where order is meaningful),
        # then unordered (covers solution sets, where it is not).
        return all(equal_scalar(a, b) for a, b in zip(pt, gt, strict=True)) or \
            _equal_as_set(pt, gt)
    if (pt is None) != (gt is None):
        return False  # a list is never equal to a scalar
    return equal_scalar(p, g)
