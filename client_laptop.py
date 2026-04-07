import json
import time
import requests
from extractor_robust import extrage_rezultat
from baza_reguli_chroma import gaseste_hint
from neuro_symbolic import run_neuro_symbolic_pipeline


#IP_PC = '100.66.132.85'
#PORT = '8000'
#URL_PC = f'http://{IP_PC}:{PORT}/rezolva'
OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL_8B = 'deepseek-r1:8b'
#URL_COLAB = 'cloudflare/api/generate'
MAX_RETRY = 3
TEMP_INITIALA = 0.9
_TEMPLATE = '\nEsti un asistent matematic precis. Rezolva problema pas cu pas.\n\n\n\n{bloc_hint}\nPROBLEMA:\n\n{problema}\n\n\n\nREGULI OBLIGATORII DE RASPUNS:\n\n1. Poti folosi <think>...</think> pentru rationament intern.\n\n2. ULTIMA linie din raspuns trebuie sa fie EXACT:\n\n   RASPUNS_FINAL: <valoarea>\n\n   Exemple: RASPUNS_FINAL: 3  |  RASPUNS_FINAL: x=2 sau x=-5  |  RASPUNS_FINAL: -3/4\n\n3. Nu adauga nimic dupa linia RASPUNS_FINAL.\n\n'
MODEL_COLAB = 'deepseek-r1:14b'
GEMINI_API_KEY = "your_api_key"


GEMINI_URL = f"ai_studio_url?key={GEMINI_API_KEY}"

def _construieste_prompt(problema: str, hint: str, context_retry: str='') -> str:
    if hint:
        bloc_hint = f'INDICII MATEMATICE RELEVANTE:\n{hint}\n\n'
    else:
        bloc_hint = ''
    baza = _TEMPLATE.format(bloc_hint=bloc_hint, problema=problema)
    if context_retry:
        return f'Raspunsul tau anterior a fost INCORECT sau incomplet: "{context_retry}".\nReconsidera complet abordarea. Verifica domeniul de definitie.\n\n' + baza
    return baza


def _apeleaza_ollama(prompt: str, temperatura: float) -> str:
    payload = {'model': MODEL_8B, 'prompt': prompt, 'stream': True, 'options': {'temperature': temperatura, 'num_predict': 8192, 'num_ctx': 16384}}
    tokeni = []
    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=400) as resp:
            resp.raise_for_status()
            for linie in resp.iter_lines():
                if not linie:
                    continue
                try:
                    chunk = json.loads(linie)
                except json.JSONDecodeError:
                    continue
                token = chunk.get('response', '')
                if token:
                    tokeni.append(token)
                if len(tokeni) % 100 == 1:
                    print(f'    ... {len(tokeni)} tokeni primiti', end='\r')
                if chunk.get('done'):
                    motiv = chunk.get('done_reason', '?')
                    n_tok = chunk.get('eval_count', '?')
                    print(f'    Streaming complet: {n_tok} tokeni, motiv={motiv}          ')
                    break
    except requests.exceptions.Timeout:
        print('  [8B] Timeout Ollama!')
    except Exception as e:
        print(f'  [8B] Eroare Ollama: {e}')
    text = ''.join(tokeni)
    if not text.strip():
        print(f'  [8B] Raspuns gol! Verifica:')
        print(f"       1. Numele modelului: `ollama list` -> MODEL_8B='{MODEL_8B}'")
        print(f'       2. Memoria VRAM disponibila (model nerincarcat)')
        print(f'       3. Lungimea promptului ({len(prompt)} chars) vs num_ctx=16384')
    return text


def _apeleaza_pc(problema: str) -> str:
    prompt_formatat = _construieste_prompt(problema, hint="")


    payload = {
        "contents": [{
            "parts": [{"text": prompt_formatat}]
        }],
        "generationConfig": {
            "temperature": 0.1
        }
    }

    try:
        resp = requests.post(GEMINI_URL, json=payload, headers={'Content-Type': 'application/json'}, timeout=60)

        if resp.status_code != 200:
            print(f"  [Gemini 2.5] Eroare HTTP {resp.status_code}: {resp.text[:150]}")
            return 'Extractie Esuata'


        data = resp.json()
        try:
            text_brut = data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            print("  [Gemini 2.5] Structura JSON necunoscuta primita de la API.")
            return 'Extractie Esuata'


        rezultat_extras = extrage_rezultat(text_brut, use_llm_fallback=False)

        if rezultat_extras in ['Extractie Esuata', 'Extracție Esuata']:
            sfarsit = text_brut[-200:].replace('\n', ' | ')
            print(f"  [DEBUG Gemini] Raspuns brut: ...{sfarsit}")
            return 'Extractie Esuata'

        return rezultat_extras

    except requests.exceptions.Timeout:
        print('  [Gemini 2.5] Timpul a expirat (Timeout API).')
        return 'Extractie Esuata'
    except Exception as e:
        print(f'  [Gemini 2.5] Eroare API: {e}')
        return 'Extractie Esuata'


def rezolva(problema: str) -> dict:
    SEP = '=' * 62
    print(f'\n{SEP}')
    print(f"PROBLEMA: {problema[:80]}{('...' if len(problema) > 80 else '')}")
    print(SEP)

    # 1. RAG
    hint = gaseste_hint(problema)
    if hint:
        print(f'[RAG] S-au detectat reguli semantice.')
    else:
        print('[RAG] Nicio regula specifica detectata.')

    # 2. baselineul
    print('\n[Gemini 2.5 Flash] -> trimit pentru baseline...')
    t0 = time.time()
    rezultat_pc = _apeleaza_pc(problema)
    print(f'[Gemini 2.5 Flash] {time.time() - t0:.1f}s -> {rezultat_pc}')

    # 3.
    print('\n[LAPTOP 8B] -> pornesc pipeline-ul Neuro-Simbolic + RAG...')
    t1 = time.time()

    text_brut_ns = run_neuro_symbolic_pipeline(problema, hint)
    durata_ns = time.time() - t1


    rezultat_8b = extrage_rezultat(text_brut_ns, use_llm_fallback=True)

    print(f'  Durata completa NS: {durata_ns:.1f}s')
    print(f'  Extras 8B NS: {rezultat_8b}')

    # 4. eventual veto
    decizie = _decide(rezultat_pc, rezultat_8b)

    print(f'\n{SEP}')
    print(f'  PC (14B)       : {rezultat_pc}')
    print(f'  Laptop (8B NS) : {rezultat_8b}')
    print(f'  DECIZIE FINALA : {decizie}')
    print(SEP)

    return {'rezultat_pc': rezultat_pc, 'rezultat_8b': rezultat_8b, 'decizie': decizie}

def _decide(rez_pc: str, rez_8b: str) -> str:
    esec = 'Extractie Esuata'
    if rez_pc == esec and rez_8b == esec: return 'AMBII AGENTI AU ESUAT'
    if rez_pc == esec: return rez_8b
    if rez_8b == esec: return rez_pc
    if rez_pc.strip() == rez_8b.strip(): return rez_pc
    return rez_pc

if __name__ == '__main__':
    probleme_benchmark = ['$\\overline{BC}$ is parallel to the segment through $A$, and $AB = BC$. What is the number of degrees represented by $x$?\n\n[asy]\ndraw((0,0)--(10,0));\ndraw((0,3)--(10,3));\ndraw((2,3)--(8,0));\ndraw((2,3)--(4,0));\nlabel(\"$A$\",(2,3),N);\nlabel(\"$B$\",(4,0),S);\nlabel(\"$C$\",(8,0),S);\nlabel(\"$124^{\\circ}$\",(2,3),SW);\nlabel(\"$x^{\\circ}$\",(4.5,3),S);\n[/asy]"']
    for p in probleme_benchmark:
        rezolva(p)
        print()
