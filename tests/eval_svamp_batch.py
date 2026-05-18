import json
import sys
import os
import time

# Add parent directory to path to import neuro_symbolic
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from neuro_symbolic import run_neuro_symbolic_pipeline

def evaluate_svamp(filepath, limit=20, model="deepseek-r1:8b"):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    problems = data[:limit]
    correct = 0
    total = len(problems)
    
    print(f"=== Începere Evaluare pe {total} probleme din SVAMP ===")
    
    start_time = time.time()
    
    for i, item in enumerate(problems, 1):
        problem_text = item['Body'] + " " + item['Question']
        expected_answer = float(item['Answer'])
        
        print(f"\n[{i}/{total}] Problema ID: {item['ID']}")
        print(f"Text: {problem_text}")
        print(f"Expected: {expected_answer}")
        
        # Suppress heavy logging from the pipeline for cleaner output
        # Let's just capture the result
        try:
            # We pass a dummy ui_callback that does nothing to keep the console clean
            # Actually, standard print inside _log will still output. We can redirect stdout temporarily or just let it print
            result_str = run_neuro_symbolic_pipeline(problem_text, model, ui_callback=lambda x: None)
            
            # Try to parse the result as float
            try:
                # remove any brackets or extra chars that might come from fallback boxed extraction
                clean_result = ''.join(c for c in str(result_str) if c.isdigit() or c in '.-')
                predicted_answer = float(clean_result)
            except ValueError:
                predicted_answer = None
                
            is_correct = predicted_answer == expected_answer
            if is_correct:
                correct += 1
                print(f"✅ Corect! (Răspuns: {result_str})")
            else:
                print(f"❌ Greșit! (Prezis: {result_str}, Așteptat: {expected_answer})")
                
        except Exception as e:
            print(f"⚠️ Eroare la execuție: {e}")

    end_time = time.time()
    duration = end_time - start_time
    
    accuracy = (correct / total) * 100
    print("\n" + "="*50)
    print(f"EVALUARE FINALIZATĂ")
    print(f"Timp total: {duration:.2f} secunde")
    print(f"Timp mediu per problemă: {duration/total:.2f} secunde")
    print(f"Acuratețe: {correct}/{total} ({accuracy:.2f}%)")
    print("="*50)

if __name__ == "__main__":
    svamp_path = os.path.join(os.path.dirname(__file__), 'svamp.json')
    evaluate_svamp(svamp_path, limit=20)
