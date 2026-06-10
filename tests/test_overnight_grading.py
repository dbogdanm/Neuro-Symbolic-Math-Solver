"""Unit tests for the overnight benchmark grader (no LLM required)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tests.overnight_bench import grade, normalize_answer  # noqa: E402


def test_plain_numbers():
    assert grade("8.0", "8")
    assert grade("70", "70")
    assert not grade("11", "12")


def test_latex_fractions():
    assert grade("1/2", "\\frac{1}{2}")
    assert grade("0.5", "\\frac{1}{2}")
    assert grade("(3)/(2)", "\\dfrac{3}{2}")


def test_sqrt_and_pi():
    assert grade("sqrt(2)", "\\sqrt{2}")
    assert grade("2*pi", "2\\pi")


def test_tuples_normalize_to_same_string():
    assert grade("(3, pi/2)", "\\left( 3, \\frac{\\pi}{2} \\right)")


def test_thousands_separator():
    assert grade("1234", "1,234")


def test_gsm8k_style():
    assert grade("18", "18")
    assert grade("18.0", "18")


def test_no_false_positive_on_empty():
    assert not grade("", "")
    assert not grade("Extraction Failed", "42")


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"[OK] {name}")
            except AssertionError:
                failures += 1
                print(f"[FAIL] {name}")
    print("normalize sample:", normalize_answer("\\left( 3, \\frac{\\pi}{2} \\right)"))
    sys.exit(1 if failures else 0)
