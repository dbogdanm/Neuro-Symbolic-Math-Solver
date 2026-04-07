import json
import csv
import time
import re
from client_laptop import rezolva

FISIER_DATASET = "tests/math500_noanswers.jsonl"
FISIER_REZULTATE = "rezultate_experimentale_math500.csv"
MAX_PROBLEME_DE_TESTAT = 30


def extrage_ground_truth_gsm8k(answer_text: str) -> str:
    match = re.search(r'####\s*(.+)', answer_text)
    if match:
        return match.group(1).strip()
    return ""


def curata_rezultat_pentru_comparatie(rezultat: str) -> str:
    if rezultat == "Extractie Esuata" or rezultat == "AMBII AGENTI AU ESUAT":
        return rezultat

    rez = rezultat.strip().replace(',', '')
    if rez.endswith('.0'):
        rez = rez[:-2]
    return rez


def evalueaza():
    print(f"=== EVALUARE BENCHMARK ({MAX_PROBLEME_DE_TESTAT} probleme) ===")

    statistici = {
        "total_testate": 0,
        "14b_corecte": 0,
        "8b_ns_corecte": 0,
        "ambii_corecti": 0
    }


    with open(FISIER_REZULTATE, mode='w', encoding='utf-8-sig', newline='') as f_out:
        writer = csv.writer(f_out, delimiter=';')

        writer.writerow([
            "ID_Problema", "Problema", "Ground_Truth",
            "Rezultat_14B", "Corect_14B",
            "Rezultat_8B_NS", "Corect_8B_NS", "Decizie_Sistem"
        ])

        try:
            with open(FISIER_DATASET, 'r', encoding='utf-8') as f_in:
                for idx, linie in enumerate(f_in):
                    if idx >= MAX_PROBLEME_DE_TESTAT:
                        break

                    data = json.loads(linie)
                    problema = data.get("question", "")
                    raspuns_complet_gt = data.get("answer", "")

                    ground_truth = extrage_ground_truth_gsm8k(raspuns_complet_gt)
                    gt_curatat = curata_rezultat_pentru_comparatie(ground_truth)

                    print(f"\n[{idx + 1}/{MAX_PROBLEME_DE_TESTAT}] Evaluam problema...")

                    # pipeline NS
                    t0 = time.time()
                    rezultate = rezolva(problema)
                    timp_total = time.time() - t0

                    rezultat_pc_curatat = curata_rezultat_pentru_comparatie(rezultate["rezultat_pc"])
                    rezultat_8b_curatat = curata_rezultat_pentru_comparatie(rezultate["rezultat_8b"])

                    #
                    corect_14b = (rezultat_pc_curatat == gt_curatat)
                    corect_8b = (rezultat_8b_curatat == gt_curatat)


                    statistici["total_testate"] += 1
                    if corect_14b: statistici["14b_corecte"] += 1
                    if corect_8b: statistici["8b_ns_corecte"] += 1
                    if corect_14b and corect_8b: statistici["ambii_corecti"] += 1


                    writer.writerow([
                        idx + 1,
                        problema,
                        ground_truth,
                        rezultate["rezultat_pc"], corect_14b,
                        rezultate["rezultat_8b"], corect_8b,
                        rezultate["decizie"]
                    ])
                    f_out.flush()
                    print(
                        f"  -> Ground Truth: {ground_truth} | 14B: {'Corect' if corect_14b else 'Gresit'} | 8B+NS: {'Corect' if corect_8b else 'Gresit'} (Timp: {timp_total:.1f}s)")

        except FileNotFoundError:
            print(f"\n[EROARE] Fisierul '{FISIER_DATASET}' nu a fost gasit. Asigura-te ca l-ai descarcat.")
            return

    print("\n" + "=" * 50)
    print("=== RAPORT FINAL EVALUARE ===")
    print("=" * 50)
    total = statistici["total_testate"]
    if total > 0:
        acc_14b = (statistici["14b_corecte"] / total) * 100
        acc_8b = (statistici["8b_ns_corecte"] / total) * 100
        print(f"Probleme testate : {total}")
        print(f"Acuratete 14B (Cloud)      : {acc_14b:.2f}% ({statistici['14b_corecte']}/{total})")
        print(f"Acuratete 8B + NS (Edge)   : {acc_8b:.2f}% ({statistici['8b_ns_corecte']}/{total})")
        print(f"Suprapunere (ambii corecti): {statistici['ambii_corecti']}")
        print(f"\nRezultatele detaliate au fost salvate in: {FISIER_REZULTATE}")
    else:
        print("Nu s-au putut procesa probleme.")


if __name__ == "__main__":
    evalueaza()