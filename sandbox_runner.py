"""Child-process loop for the persistent SymPy sandbox.

Kept in its own import-light module on purpose: on Windows, multiprocessing
uses the *spawn* start method, so the child re-imports the module that holds
the target function. Keeping this file free of heavy imports (Flask, ChromaDB,
the LLM layer) means the worker boots with only the SymPy import cost — and
that cost is paid once per worker, not once per execution.
"""

import pickle


def sandbox_loop(in_q, out_q):
    """Run PoT scripts received on ``in_q`` forever; reply on ``out_q``.

    Protocol: receives a code string (or ``None`` to shut down), replies with
    ``("SUCCESS", final_result)`` or ``("ERROR", message)``.
    """
    import sympy as sp  # paid once per worker lifetime

    while True:
        code = in_q.get()
        if code is None:
            break

        namespace = {"sp": sp, "sympy": sp}
        try:
            exec(code, namespace)  # noqa: S102 - isolated worker subprocess
            result = namespace.get("final_result")
            try:
                pickle.dumps(result)
            except Exception:  # noqa: BLE001 - unpicklable SymPy/lambda objects
                result = str(result)
            out_q.put(("SUCCESS", result))
        except BaseException as e:  # noqa: BLE001 - report, keep worker alive
            out_q.put(("ERROR", f"{type(e).__name__}: {e}"))
