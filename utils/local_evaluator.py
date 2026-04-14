import json
import time
import re
import csv
from rules_base import gaseste_hint
from neuro_symbolic import run_neuro_symbolic_pipeline
from extractor import extrage_rezultat




FISIER_JSONL = "tests/omni_math.jsonl"
FISIER_REZULTATE = "omni_math.csv"  
MAX_PROBLEME = 30


def extrage_ground_truth(raspuns_complet) -> str:
    
    
    raspuns_str = str(raspuns_complet)

    match_gsm8k = re.search(r'####\s*(.+)', raspuns_str)
    if match_gsm8k:
        return match_gsm8k.group(1).strip()

    match_math = re.search(r'\\boxed\{(.+?)\}', raspuns_str)
    if match_math:
        return match_math.group(1).strip()

    return raspuns_str.strip()


def curata_rezultat(rezultat: str) -> str:
    if rezultat in ["Extractie Esuata", "Extractie Esuata", None]:
        return "Eroare"
    rez = str(rezultat).strip().replace(',', '')
    if rez.endswith('.0'):
        rez = rez[:-2]
    return rez


def ruleaza_teste():
    print(f"=== INCEPE TESTAREA ({MAX_PROBLEME} probleme) ===")
    print(f"Sursa: {FISIER_JSONL}")
    print(f"Rezultatele vor fi salvate in: {FISIER_REZULTATE}\n")

    statistici = {"total": 0, "corecte": 0, "erori": 0}

    
    with open(FISIER_REZULTATE, mode='w', encoding='utf-8-sig', newline='') as f_out:
        writer = csv.writer(f_out, delimiter=';')
        
        writer.writerow(["ID_Problema", "Problema", "Ground_Truth", "Rezultat_Sistem", "Status", "Timp_Secunde"])

        try:
            with open(FISIER_JSONL, 'r', encoding='utf-8') as f_in:
                for idx, linie in enumerate(f_in):
                    if idx >= MAX_PROBLEME:
                        break

                    data = json.loads(linie)
                    problema = data.get("question", data.get("problem", ""))
                    raspuns_complet_gt = data.get("answer", data.get("solution", ""))

                    gt = extrage_ground_truth(raspuns_complet_gt)
                    gt_curatat = curata_rezultat(gt)

                    print(f"\n[{idx + 1}/{MAX_PROBLEME}] Problema: {problema[:80]}...")

                    t0 = time.time()

                    
                    hint = gaseste_hint(problema)
                    text_brut = run_neuro_symbolic_pipeline(problema, hint)
                    rezultat_brut = extrage_rezultat(text_brut, use_llm_fallback=True)
                    rezultat_curatat = curata_rezultat(rezultat_brut)

                    timp_executie = round(time.time() - t0, 1)

                    
                    is_correct = (rezultat_curatat == gt_curatat)
                    status_text = "CORECT" if is_correct else (
                        "EROARE EXTRACTIE" if rezultat_curatat == "Eroare" else "GRESIT")

                    statistici["total"] += 1
                    if is_correct:
                        statistici["corecte"] += 1
                    elif rezultat_curatat == "Eroare":
                        statistici["erori"] += 1

                    
                    writer.writerow([
                        idx + 1,
                        problema,
                        gt_curatat,
                        rezultat_curatat,
                        status_text,
                        timp_executie
                    ])
                    f_out.flush()

                    print(f"  -> Ground Truth : {gt_curatat}")
                    print(f"  -> Raspuns Sistem: {rezultat_curatat}")
                    print(f"  -> Status       : {' ' if is_correct else ' '}{status_text} ({timp_executie}s)")

        except FileNotFoundError:
            print(f"\n[EROARE] Fisierul {FISIER_JSONL} nu a fost gasit.")
            return

    
    print("\n" + "=" * 40)
    print("=== RAPORT FINAL ===")
    print("=" * 40)
    if statistici["total"] > 0:
        acuratete = (statistici["corecte"] / statistici["total"]) * 100
        print(f"Acuratete : {acuratete:.1f}% ({statistici['corecte']}/{statistici['total']})")
        print(f"Esecuri extr: {statistici['erori']}")
        print(f"Fisier salvat: {FISIER_REZULTATE}")
    else:
        print("Nu a fost procesata nicio problema.")


if __name__ == "__main__":
    ruleaza_teste()