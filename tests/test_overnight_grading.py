"""Unit tests for the benchmark answer grader (no LLM required)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grading import grade, normalize_answer  # noqa: E402


def test_plain_numbers():
    assert grade("8.0", "8")
    assert grade("70", "70")
    assert not grade("11", "12")


def test_latex_fractions():
    assert grade("1/2", "\\frac{1}{2}")
    assert grade("0.5", "\\frac{1}{2}")
    assert grade("(3)/(2)", "\\dfrac{3}{2}")


def test_nested_latex_is_expanded():
    """A single regex pass cannot see into a braced argument."""
    assert grade("\\frac{\\sqrt{3}}{3}", "\\sqrt{3}/3")
    assert grade("\\frac{\\sqrt{2}}{2}", "0.7071067811865476")
    assert grade("\\frac{1}{\\sqrt{2}}", "\\frac{\\sqrt{2}}{2}")


def test_sqrt_and_pi():
    assert grade("sqrt(2)", "\\sqrt{2}")
    assert grade("2*pi", "2\\pi")
    assert grade("\\sqrt[3]{8}", "2")


def test_tuples_normalize_to_same_string():
    assert grade("(3, pi/2)", "\\left( 3, \\frac{\\pi}{2} \\right)")


def test_complex_numbers_match_sympy_output():
    """SymPy prints the imaginary unit as ``I``; the labels write ``i``."""
    assert grade("6 - 5*I", "6 - 5i")
    assert grade("6 + 9*I", "6+9i")
    assert grade("-2 + 7*I", "-2 + 7i")
    assert not grade("6 - 5*I", "6 + 5i")


def test_list_wrappers_are_stripped():
    """``solve()`` returns a list where the label writes bare values."""
    assert grade("[3, 5, 7]", "3, 5, 7")
    assert grade("[5]", "x=5")
    assert grade("[18]", "18")
    assert not grade("[1, 2]", "1")
    assert not grade("1", "[1, 2]")


def test_solution_sets_ignore_order():
    assert grade("-2.00000000000000, 1.00000000000000", "1,-2")
    assert grade("[7, 3, 5]", "3, 5, 7")
    assert not grade("1,2", "1,3")


def test_ordered_pairs_still_respect_order():
    """Coordinates are ordered even though solution sets are not."""
    assert not grade("(1, 2)", "(2, 3)")


def test_answer_shell_is_stripped():
    assert grade("The answer is 42", "42")
    assert grade("\\boxed{42}", "42")
    assert grade("x = 5", "5")


def test_thousands_separator():
    assert grade("1234", "1,234")


def test_gsm8k_style():
    assert grade("18", "18")
    assert grade("18.0", "18")


def test_no_false_positive_on_empty():
    assert not grade("", "")
    assert not grade("Extraction Failed", "42")


def test_genuinely_wrong_answers_stay_wrong():
    """Guards the fix against over-permissiveness: these are real misses."""
    assert not grade("336", "225")
    assert not grade("239", "821")
    assert not grade("52", "52_8")  # base-8 label, bare decimal prediction
    assert not grade("60671", "237")


def test_normalize_is_idempotent():
    for raw in ("\\frac{\\sqrt{3}}{3}", "[3, 5, 7]", "6 - 5*I", "x = 5"):
        once = normalize_answer(raw)
        assert normalize_answer(once) == once
