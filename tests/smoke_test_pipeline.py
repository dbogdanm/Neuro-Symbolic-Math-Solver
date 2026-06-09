"""Quick smoke test for the pipeline internals (no LLM/Ollama needed).

Run from anywhere: ``python tests/smoke_test_pipeline.py``
"""
import os
import sys
import time

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
os.chdir(_ROOT)  # rules_base resolves ./chroma_db_reguli relative to CWD


def main():
    import neuro_symbolic as ns

    # --- fast path ---------------------------------------------------------
    assert ns.is_simple_math("how much is 2+6")
    assert ns.solve_simple_math("how much is 2+6") == "8"
    print("[OK] fast path")

    # --- validator ---------------------------------------------------------
    code = ns.step3_code_validator("bla\n```python\nfinal_result = 1+1\n```\n")
    assert "final_result" in code
    print("[OK] validator")

    # --- persistent sandbox: cold vs warm ----------------------------------
    t0 = time.time()
    r1 = ns.execute_code_with_timeout("import sympy\nfinal_result = sympy.Integer(2) + 3")
    cold = time.time() - t0

    t0 = time.time()
    r2 = ns.execute_code_with_timeout("final_result = sp.sqrt(16)")
    warm = time.time() - t0
    assert str(r1) == "5" and str(r2) == "4", (r1, r2)
    print(f"[OK] sandbox exec: cold={cold:.2f}s warm={warm:.3f}s")

    # --- error path keeps worker alive --------------------------------------
    try:
        ns.execute_code_with_timeout("final_result = 1/0")
        raise AssertionError("expected error")
    except Exception as e:
        assert "ZeroDivision" in str(e), e
    r3 = ns.execute_code_with_timeout("final_result = 7*6")
    assert str(r3) == "42"
    print("[OK] error path + worker survives")

    # --- timeout kills and respawns -----------------------------------------
    t0 = time.time()
    try:
        ns.execute_code_with_timeout("while True:\n    pass", timeout=3)
        raise AssertionError("expected timeout")
    except TimeoutError:
        pass
    print(f"[OK] timeout path ({time.time()-t0:.1f}s)")
    r4 = ns.execute_code_with_timeout("final_result = 10**3")
    assert str(r4) == "1000"
    print("[OK] respawn after timeout")

    # --- direct embedding RAG (no LLM call) ----------------------------------
    try:
        from rules_base import find_hints
    except Exception:
        find_hints = None
    if find_hints is not None:
        t0 = time.time()
        h1 = find_hints("Converting a point from Cartesian coordinates to polar coordinates.")
        assert h1, "expected a direct match on a near-exact description"
        print(f"[OK] direct RAG hit in {time.time()-t0:.2f}s -> {h1[:60]!r}")

        h2 = find_hints("Convert the point (0,3) in rectangular coordinates to polar coordinates.")
        print(f"[OK] wordy query (miss allowed, no crash) -> {h2[:60]!r}")

        # hint with Romanian diacritics must not crash the console print
        h3 = find_hints("infinite tower of powers x^x^x... convergence")
        print(f"[OK] diacritics-safe print -> {h3[:60]!r}")
    else:
        print("[SKIP] RAG not available")

    print("\nALL SMOKE TESTS PASSED")


if __name__ == "__main__":
    main()
