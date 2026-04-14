import chromadb
from math_rules import MATH_RULES


client = chromadb.PersistentClient(path="./chroma_db_reguli")



collection = client.get_or_create_collection(name="reguli_matematice")


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


def find_hint(problem_type: str, max_distance: float = 1.2) -> str:
    """
    Searches for the most relevant hint based on the problem description.
    Returns the hint if the semantic distance is below the threshold, otherwise returns an empty string,
    but prints what it found in the console for debugging.
    """
    if not problem_type or problem_type.strip() == "":
        return ""

    try:
        results = collection.query(
            query_texts=[problem_type],
            n_results=1
        )

        
        distance = results['distances'][0][0]
        found_metadata = results['metadatas'][0][0]
        rule_id = found_metadata.get('rule_id', 'UNKNOWN_ID')
        found_hint = found_metadata.get('hint', 'NO_HINT')

        if distance < max_distance:
            print(f"    [Chroma Match] Success! Rule ID: {rule_id} (Distance: {distance:.2f})")
            return found_hint
        else:
            print(f"    [Chroma Miss] Distance above threshold ({distance:.2f} > {max_distance}). Ignoring.")
            
            print(f"    [DEBUG Chroma] The rule it wanted to choose was ID: '{rule_id}'")
            print(f"    [DEBUG Chroma] Rejected hint: {found_hint[:200]}...")  
            return ""

    except Exception as e:
        print(f"[ChromaDB Error] Could not query the database: {e}")
        return ""