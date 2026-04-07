import json
import csv
import time
import re
from extractor_robust import extrage_rezultat
from baza_reguli_chroma import gaseste_hint
from neuro_symbolic import run_neuro_symbolic_pipeline


FISIER_DATASET = "tests/1problema.jsonl"
FISIER_REZULTATE = "test.csv"
MAX_PROBLEME = 1


def extrage_ground_truth(dataset_type: str, answer_data: str) -> str:
    if "gsm8k" in dataset_type.lower():
        match = re.search(r'####\s*(.+)', answer_data)
        return match.group(1).strip() if match else ""
    elif "math" in dataset_type.lower():
        match = re.search(r'\\boxed\{(.+?)\}', answer_data)
        return match.group(1).strip() if match else answer_data.strip()
    return answer_data


def curata_rezultat(rezultat: str) -> str:
    if rezultat in ["Extractie Esuata", "Extracție Esuata"]:
        return rezultat
    rez = str(rezultat).strip().replace(',', '')
    if rez.endswith('.0'):
        rez = rez[:-2]
    return rez


def evalueaza_local():
    print(f"\n=== Evaluare Locala (Max {MAX_PROBLEME} probleme) ===")
    print(f"Dataset: {FISIER_DATASET}\n")

    statistici = {"total": 0, "corecte": 0, "erori_extractie": 0}

    with open(FISIER_REZULTATE, mode='w', encoding='utf-8-sig', newline='') as f_out:
        writer = csv.writer(f_out, delimiter=';')
        writer.writerow(["ID", "Problema", "Ground_Truth", "Rezultat_8B_NS", "Corect", "Timp_Executie_s"])

        try:
            with open(FISIER_DATASET, 'r', encoding='utf-8') as f_in:
                for idx, linie in enumerate(f_in):
                    if idx >= MAX_PROBLEME:
                        break

                    data = json.loads(linie)
                    problema = data.get("question", data.get("problem", ""))
                    raspuns_complet_gt = data.get("answer", data.get("solution", ""))

                    gt = extrage_ground_truth(FISIER_DATASET, raspuns_complet_gt)
                    gt_curatat = curata_rezultat(gt)

                    print(f"\n[{idx + 1}/{MAX_PROBLEME}] Procesam problema...")

                    t0 = time.time()

                    # 1. RAG
                    hint = gaseste_hint(problema)

                    # 2. rulare pipeline Neuro-Simbolic (8B)
                    text_brut_ns = run_neuro_symbolic_pipeline(problema, hint)

                    # 3. extragere rezultat final
                    rezultat_8b = extrage_rezultat(text_brut_ns, use_llm_fallback=True)
                    timp_total = round(time.time() - t0, 1)

                    rez_curatat = curata_rezultat(rezultat_8b)

                    # 4. validare
                    is_correct = (rez_curatat == gt_curatat)

                    statistici["total"] += 1
                    if is_correct:
                        statistici["corecte"] += 1
                    if rezultat_8b in ["Extractie Esuata", "Extractie Esuata"]:
                        statistici["erori_extractie"] += 1

                    # 5. salvaree in .csv
                    writer.writerow([
                        idx + 1,
                        problema,
                        gt,
                        rezultat_8b,
                        is_correct,
                        timp_total
                    ])
                    f_out.flush()  # ca sa se salveze pe loc

                    status = "CORECT" if is_correct else "GRESIT"
                    print(f"  -> GT: {gt_curatat} | 8B: {rez_curatat} | {status} (Timp: {timp_total}s)")

        except FileNotFoundError:
            print(f"\n[EROARE] Fisierul '{FISIER_DATASET}' nu a fost gasit.")
            return

    # Raport Final
    print("\n" + "=" * 50)
    print("=== RAPORT FINAL 8B NEURO-SIMBOLIC ===")
    print("=" * 50)
    if statistici["total"] > 0:
        acc = (statistici["corecte"] / statistici["total"]) * 100
        print(f"Total evaluate    : {statistici['total']}")
        print(f"Raspunsuri Corecte: {statistici['corecte']} ({acc:.2f}%)")
        print(f"Esecuri Extractie : {statistici['erori_extractie']}")
        print(f"\nRezultatele au fost salvate in: {FISIER_REZULTATE}")
    else:
        print("Nu au fost evaluate probleme.")


if __name__ == "__main__":
    evalueaza_local()