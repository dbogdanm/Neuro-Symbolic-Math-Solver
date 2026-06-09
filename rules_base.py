import chromadb
from math_rules import MATH_RULES


client = chromadb.PersistentClient(path="./chroma_db_reguli")


# "_en" collection: math_rules.py was translated to English (matching the
# English benchmarks), so the English corpus lives in its own collection.
# The legacy Romanian "reguli_matematice" collection is left untouched.
collection = client.get_or_create_collection(name="reguli_matematice_en")


def populate_database():
    """Checks if the database is empty and populates it from math_rules.py"""
    if collection.count() == 0:
        print("[ChromaDB] Database is empty. Starting embedding generation...")

        documents = []
        metadata_list = []
        ids = []

        for rule in MATH_RULES:
            
            
            documents.append(rule["description"])

            
            metadata_list.append({"hint": rule["hint"], "rule_id": rule["id"]})

            ids.append(rule["id"])

        collection.add(
            documents=documents,
            metadatas=metadata_list,
            ids=ids
        )
        print(f"[ChromaDB] Success! Indexed {len(documents)} math rules.")



populate_database()


def _safe_print(msg: str) -> None:
    """Print that survives legacy Windows console encodings (cp1252)."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", "backslashreplace").decode("ascii"))


def find_hints(query: str, n_results: int = 2, max_distance: float = 1.2) -> str:
    """
    Retrieves the top-N most relevant hints by embedding similarity (Eq. 1 in
    the paper: H = argmax cos(E(P), E(r_i))). Hints whose semantic distance is
    above the threshold are discarded; matches are joined into a single block.
    """
    if not query or query.strip() == "":
        return ""

    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )

        hints = []
        for distance, metadata in zip(results['distances'][0], results['metadatas'][0]):
            # 'id_regula' is the metadata key used by older persisted DBs.
            rule_id = metadata.get('rule_id') or metadata.get('id_regula', 'UNKNOWN_ID')
            found_hint = metadata.get('hint', 'NO_HINT')

            if distance < max_distance:
                _safe_print(f"    [Chroma Match] Success! Rule ID: {rule_id} (Distance: {distance:.2f})")
                hints.append(found_hint)
            else:
                _safe_print(f"    [Chroma Miss] Distance above threshold ({distance:.2f} > {max_distance}). Ignoring.")
                _safe_print(f"    [DEBUG Chroma] The rule it wanted to choose was ID: '{rule_id}'")
                _safe_print(f"    [DEBUG Chroma] Rejected hint: {found_hint[:200]}...")

        return "\n\n".join(hints)

    except Exception as e:
        print(f"[ChromaDB Error] Could not query the database: {e}")
        return ""


def find_hint(problem_type: str, max_distance: float = 1.2) -> str:
    """Backwards-compatible single-hint lookup."""
    return find_hints(problem_type, n_results=1, max_distance=max_distance)