"""Internal RAG over a small library of math rules, backed by ChromaDB.

The vector store is built lazily on first query from ``MATH_RULES`` (the source
of truth in ``math_rules.py``), so importing this module performs no I/O. If the
persistent store under ``chroma_db_reguli/`` is missing or empty it is rebuilt
automatically on first use.
"""

import chromadb

_DB_PATH = "./chroma_db_reguli"
_COLLECTION_NAME = "reguli_matematice"

_collection = None


def _get_collection():
    """Return the ChromaDB collection, building/populating it on first use."""
    global _collection
    if _collection is not None:
        return _collection

    client = chromadb.PersistentClient(path=_DB_PATH)
    collection = client.get_or_create_collection(name=_COLLECTION_NAME)

    if collection.count() == 0:
        from math_rules import MATH_RULES

        print("[ChromaDB] Empty store — generating rule embeddings...")
        collection.add(
            documents=[rule["description"] for rule in MATH_RULES],
            metadatas=[{"hint": rule["hint"], "rule_id": rule["id"]} for rule in MATH_RULES],
            ids=[rule["id"] for rule in MATH_RULES],
        )
        print(f"[ChromaDB] Indexed {collection.count()} math rules.")

    _collection = collection
    return _collection


def find_hint(problem_type: str, max_distance: float = 1.2) -> str:
    """Return the best-matching rule hint, or ``""`` if none is close enough.

    ``max_distance`` is the semantic-distance threshold above which the closest
    match is rejected as irrelevant.
    """
    if not problem_type or not problem_type.strip():
        return ""

    try:
        results = _get_collection().query(query_texts=[problem_type], n_results=1)
        distance = results["distances"][0][0]
        metadata = results["metadatas"][0][0]
        rule_id = metadata.get("rule_id", "UNKNOWN_ID")
        hint = metadata.get("hint", "")

        if distance < max_distance:
            print(f"    [Chroma Match] Rule {rule_id} (distance {distance:.2f})")
            return hint

        print(
            f"    [Chroma Miss] Closest rule {rule_id} rejected "
            f"(distance {distance:.2f} >= {max_distance})."
        )
        return ""
    except Exception as exc:  # noqa: BLE001 - never let RAG break the pipeline
        print(f"[ChromaDB Error] Query failed: {exc}")
        return ""
