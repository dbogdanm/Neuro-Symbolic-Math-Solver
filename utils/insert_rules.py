import json
from openai import OpenAI


LLM_BASE_URL = "http://localhost:11434/v1"
client = OpenAI(base_url=LLM_BASE_URL, api_key="ollama")


OLLAMA_MODEL_NAME = "gemma4:31b"

SYSTEM_PROMPT = """You are an expert AI architect for a Neuro-Symbolic Math System.
Your task is to analyze a math problem and output a concise, step-by-step 'Program-of-Thought' (PoT) hint.
This hint MUST guide a downstream Python/SymPy agent on HOW to solve the problem programmatically.
DO NOT write actual Python code. DO NOT calculate the final answer. 
Focus ONLY on the algorithmic strategy, equations, and SymPy functions needed.
Keep it strictly in English. Output ONLY the numbered hint."""


def generate_hint(problem_text):
    try:
        response = client.chat.completions.create(
            model=OLLAMA_MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate a SymPy execution hint for this problem:\n{problem_text}"}
            ],
            temperature=0.1,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[!] Eroare la generarea LLM: {e}")
        return None


def main():
    fisier_intrare = "tests/math500_noanswers.jsonl"
    fisier_iesire = "hinturi.jsonl"  

    print(f"Incepem... Rezultatele vor fi salvate in: {fisier_iesire}")

    
    with open(fisier_intrare, 'r', encoding='utf-8') as f_in, \
            open(fisier_iesire, 'w', encoding='utf-8') as f_out:

        for i, line in enumerate(f_in):
            data = json.loads(line)

            problem = data.get('problem', '')
            answer = data.get('answer', '')
            item_id = data.get('id', str(i))

            print(f"[{i + 1}/500] Generam hint pentru problema {item_id}...")
            hint = generate_hint(problem)

            if hint:
                
                rezultat_final = {
                    "id": item_id,
                    "descriere": problem,
                    "hint": hint,
                    "answer": answer
                }

                
                f_out.write(json.dumps(rezultat_final, ensure_ascii=False) + "\n")
                f_out.flush()
                print(f"  -> Salvat in fisier!")
            else:
                print(f"  -> Eroare. Nu s-a salvat.")

    print("\nProces complet! Poti deschide fisierul", fisier_iesire)


if __name__ == "__main__":
    main()