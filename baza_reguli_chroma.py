import chromadb
from baza_reguli import REGULI_MATEMATICE
PRAG_DISTANTA = 1.2
MAX_HINTS = 3
print('⏳ Initializam Baza de Date Vectoriala ChromaDB...')
_client = chromadb.Client()
_colectie = _client.create_collection(name='reguli_matematice', metadata={'hnsw:space': 'cosine'})
_colectie.add(ids=[r['id'] for r in REGULI_MATEMATICE], documents=[r['descriere'] for r in REGULI_MATEMATICE], metadatas=[{'hint': r['hint'], 'id': r['id']} for r in REGULI_MATEMATICE])
print(f' {len(REGULI_MATEMATICE)} reguli vectorizate in ChromaDB.\n')

def gaseste_hint(problema: str, n: int=MAX_HINTS) -> str:
    if not problema or not problema.strip():
        return ''
    rezultate = _colectie.query(query_texts=[problema], n_results=min(n, len(REGULI_MATEMATICE)))
    ids_gasite = rezultate['ids'][0]
    distante = rezultate['distances'][0]
    metadate = rezultate['metadatas'][0]
    hint_uri_selectate = []
    for id_r, dist, meta in zip(ids_gasite, distante, metadate):
        if dist < PRAG_DISTANTA:
            hint_uri_selectate.append(f"[{id_r} | distanta={dist:.3f}]: {meta['hint']}")
    if not hint_uri_selectate:
        return ''
    return '\n'.join(hint_uri_selectate)
if __name__ == '__main__':
    teste = ['Rezolvă log₂(x-1) + log₂(x+1) = 3. Verifică domeniul.', 'Calculează derivata lui f(x) = x² · sin(x).', 'Rezolvă ecuația biquadratică x⁴ - 5x² + 4 = 0.', 'Fie (x²-4)/(x-2). Calculează limita când x→2.', 'Dacă |2x - 3| = 7, găsește valorile lui x.', 'Câte combinări de 3 elemente din 7 există?', 'Cât face 5 + 5?']
    print('=' * 60)
    for i, p in enumerate(teste, 1):
        hint = gaseste_hint(p)
        print(f'\n[{i}] {p[:65]}')
        if hint:
            for linie in hint.split('\n'):
                print(f'   → {linie[:100]}...')
        else:
            print('   → [nicio regulă relevantă]')
    print('\n' + '=' * 60)
