from rules_base import gaseste_hint
from neuro_symbolic import extrage_tip_problema

problema_benchmark = (
    r'ixteen chairs are arranged in a row. Eight people each select a chair in which to sit so that no person sits next to two other people. Let $N$ be the number of subsets of $16$ chairs that could be selected. Find the remainder when $N$ is divided by $1000$.'
)

print("=" * 60)
print("PROBLEMA:")
print(problema_benchmark)
print("=" * 60)


print("\n[VARIANTA 1] Query cu enuntul brut:")
hint_brut = gaseste_hint(problema_benchmark)
if hint_brut:
    print(hint_brut)
else:
    print("Nu s-a gasit nicio regula.")


print("\n[VARIANTA 2] Query dupa reformulare LLM:")
tip = extrage_tip_problema(problema_benchmark)
print(f"   Tip extras: {tip}\n")
hint_reformulat = gaseste_hint(tip)
if hint_reformulat:
    print(hint_reformulat)
else:
    print("Nu s-a gasit nicio regula.")

print("\n" + "=" * 60)
print("CONCLUZIE:")
if hint_brut == hint_reformulat:
    print("Ambele variante au returnat acelasi hint.")
elif hint_reformulat and not hint_brut:
    print("Reformularea a gasit un hint pe care enuntul brut NU l-a gasit!")
elif hint_brut and not hint_reformulat:
    print("Enuntul brut a gasit ceva, reformularea nu — verifica promptul.")
else:
    print("Ambele au gasit hinturi, dar DIFERITE — reformularea poate fi mai relevanta.")
print("=" * 60)