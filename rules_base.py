"""Internal RAG over a small library of math rules, backed by ChromaDB.

The vector store is built lazily on first query from ``MATH_RULES`` (the source
of truth in ``math_rules.py``), so importing this module performs no I/O. If the
persistent store under ``chroma_db_reguli/`` is missing or empty it is rebuilt
automatically on first use.

The active collection is ``reguli_matematice_en_cosine``: ``math_rules.py`` is
written in English to match the language of the evaluation benchmarks (GSM8K,
MATH500, AIME, SVAMP), and the index is built in **cosine** space so that the
distances printed here are the same quantity Eq. 1 of the paper is written in.
ChromaDB's default is squared L2; on the normalized MiniLM embeddings used here
the two are related by ``L2^2 = 2 - 2*cos``, i.e. ``d_cos = d_L2^2 / 2``, so the
*ranking* is identical but the numbers differ by a factor of two. Earlier
collections (``reguli_matematice``, Romanian; ``reguli_matematice_en``, English
in L2 space) are left untouched on disk so past runs stay reproducible.
"""

import chromadb

_DB_PATH = "./chroma_db_reguli"
_COLLECTION_NAME = "reguli_matematice_en_cosine"

# Cosine-distance thresholds (range [0, 2]; 0 = identical direction).
#
# DEFAULT_MAX_DISTANCE gates the fallback path, which queries with an LLM-written
# problem-type description — short, on-topic text that lands close to the rules.
# DIRECT_MAX_DISTANCE gates the direct-embedding path of Eq. 1, which queries
# with the raw problem statement. That is a much looser match (word problems are
# mutually similar as prose regardless of the mathematics), so it needs the
# tighter gate: a prescriptive hint pulled from the wrong rule actively poisons
# the generated program. Both were previously expressed as squared-L2 distances
# (1.2 and 0.9); the values here are those thresholds converted to cosine and
# select exactly the same matches.
DEFAULT_MAX_DISTANCE = 0.6
DIRECT_MAX_DISTANCE = 0.45

_collection = None


def _get_collection():
    """Return the ChromaDB collection, building/populating it on first use."""
    global _collection
    if _collection is not None:
        return _collection

    client = chromadb.PersistentClient(path=_DB_PATH)
    collection = client.get_or_create_collection(
        name=_COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )

    if collection.count() == 0:
        from math_rules import MATH_RULES

        print("[ChromaDB] Empty store - generating rule embeddings...")
        collection.add(
            documents=[rule["description"] for rule in MATH_RULES],
            metadatas=[{"hint": rule["hint"], "rule_id": rule["id"]} for rule in MATH_RULES],
            ids=[rule["id"] for rule in MATH_RULES],
        )
        print(f"[ChromaDB] Indexed {collection.count()} math rules.")

    _collection = collection
    return _collection


def _safe_print(msg: str) -> None:
    """Print that survives legacy Windows console encodings (cp1252)."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", "backslashreplace").decode("ascii"))


def find_hints(query: str, n_results: int = 2,
               max_distance: float = DEFAULT_MAX_DISTANCE) -> str:
    """Retrieve the top-N most relevant hints by embedding similarity.

    Implements Eq. 1 of the paper: ``H = argmax cos(E(P), E(r_i))`` — the query
    can be the raw problem text itself, no LLM classification needed. Hints
    whose cosine distance exceeds ``max_distance`` are discarded; the kept
    matches are joined into a single hint block.
    """
    if not query or not query.strip():
        return ""

    try:
        results = _get_collection().query(query_texts=[query], n_results=n_results)

        hints = []
        for distance, metadata in zip(
            results["distances"][0], results["metadatas"][0], strict=True
        ):
            # 'id_regula' is the metadata key used by older persisted DBs.
            rule_id = metadata.get("rule_id") or metadata.get("id_regula", "UNKNOWN_ID")
            hint = metadata.get("hint", "")

            if distance < max_distance:
                _safe_print(f"    [Chroma Match] Rule {rule_id} (cosine distance {distance:.2f})")
                hints.append(hint)
            else:
                _safe_print(
                    f"    [Chroma Miss] Closest rule {rule_id} rejected "
                    f"(cosine distance {distance:.2f} >= {max_distance})."
                )

        return "\n\n".join(hints)
    except Exception as exc:  # noqa: BLE001 - never let RAG break the pipeline
        print(f"[ChromaDB Error] Query failed: {exc}")
        return ""
