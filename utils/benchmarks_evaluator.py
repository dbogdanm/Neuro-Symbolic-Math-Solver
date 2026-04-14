import json
import csv
import requests
import time


MODEL = "deepseek-r1:14b"
INPUT_FILE = "../tests/aime2025.jsonl"
OUTPUT_FILE = "../tests/rezultate_benchmark_14b_ablation.csv"
TIMEOUT_SECONDS = 240  
OLLAMA_URL = "http://localhost:11434/api/generate"


def run_benchmark():
    
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['id', 'problem', 'response', 'status', 'time_taken_seconds']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        try:
            
            with open(INPUT_FILE, 'r', encoding='utf-8') as jsonl_file:
                for index, line in enumerate(jsonl_file):
                    if not line.strip():
                        continue

                    data = json.loads(line)

                    
                    
                    problem_text = data.get("problem", "")

                    print(f"[{index}] Se proceseaza problema... (Timeout setat la {TIMEOUT_SECONDS}s)")
                    start_time = time.time()

                    try:
                        
                        response = requests.post(
                            OLLAMA_URL,
                            json={
                                "model": MODEL,
                                "prompt": problem_text,
                                "stream": False  
                            },
                            timeout=TIMEOUT_SECONDS
                        )
                        response.raise_for_status()  

                        result = response.json()
                        model_response = result.get("response", "")
                        status = "success"

                    except requests.exceptions.Timeout:
                        print(f"   [!] Timeout: Problema {index} a depasit 4 minute. Se trece mai departe.")
                        model_response = "TIMEOUT"
                        status = "timeout"
                    except requests.exceptions.RequestException as e:
                        print(f"   [X] Eroare la problema {index}: {e}")
                        model_response = f"ERROR: {str(e)}"
                        status = "error"

                    end_time = time.time()
                    time_taken = round(end_time - start_time, 2)

                    
                    writer.writerow({
                        'id': index,
                        'problem': problem_text,
                        'response': model_response,
                        'status': status,
                        'time_taken_seconds': time_taken
                    })

                    print(f"   [-] Gata in {time_taken} secunde. Status: {status}\n")

        except FileNotFoundError:
            print(f"Eroare: Fisierul '{INPUT_FILE}' nu a fost gasit in directorul curent.")
        except json.JSONDecodeError:
            print(f"Eroare: Fisierul '{INPUT_FILE}' nu este un JSONL valid.")


if __name__ == "__main__":
    print("Incepem benchmark-ul...")
    run_benchmark()
    print(f"Benchmark finalizat. Rezultatele au fost salvate in '{OUTPUT_FILE}'.")