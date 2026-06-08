"""Unit tests for the pure pipeline helpers. No LLM / network required.

These cover the deterministic parts of the neuro-symbolic pipeline: the
fast-path detector, the direct SymPy solver, code-block validation, and the
sandboxed executor (including its timeout guard).
"""

import pytest

import neuro_symbolic as ns


def test_is_simple_math_detects_arithmetic_and_basic_algebra():
    assert ns.is_simple_math("2+6")
    assert ns.is_simple_math("how much is 2+6")
    assert ns.is_simple_math("x^2=4")


def test_is_simple_math_rejects_word_problems():
    assert not ns.is_simple_math("Mary has 5 apples and buys 3 more; how many now?")


def test_solve_simple_math_arithmetic():
    assert ns.solve_simple_math("2+6") == "8"
    assert ns.solve_simple_math("how much is 10*10") == "100"


def test_solve_simple_math_equation_lists_solutions():
    out = ns.solve_simple_math("x^2=4")
    assert "2" in out  # solutions are ±2


def test_code_validator_extracts_python_block():
    response = "Sure:\n```python\nfinal_result = 2 + 2\n```\n"
    assert "final_result" in ns.step3_code_validator(response)


def test_code_validator_requires_final_result():
    with pytest.raises(ValueError):
        ns.step3_code_validator("```python\nx = 1\n```")


def test_code_validator_requires_a_code_block():
    with pytest.raises(ValueError):
        ns.step3_code_validator("there is no code here")


def test_execute_code_returns_value():
    assert ns.execute_code_with_timeout("final_result = 6 * 7") == 42


def test_execute_code_propagates_errors():
    with pytest.raises(ns.SandboxError):
        ns.execute_code_with_timeout("final_result = 1 / 0")


def test_execute_code_enforces_timeout():
    with pytest.raises(TimeoutError):
        ns.execute_code_with_timeout("while True:\n    pass", timeout=3)
