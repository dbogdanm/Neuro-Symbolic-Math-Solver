import json
import time
import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor
from extractor import extrage_rezultat
from rules_base import gaseste_hint
from neuro_symbolic import run_neuro_symbolic_pipeline


OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL_8B = 'deepseek-r1:8b'
MAX_RETRY = 3
TEMP_INITIALA = 0.9

_TEMPLATE = (
    '\nEsti un asistent matematic precis. Rezolva problema pas cu pas.\n\n\n\n'
    '{bloc_hint}'
    'PROBLEMA:\n\n{problema}\n\n\n\n'
    'REGULI OBLIGATORII DE RASPUNS:\n\n'
    '1. Poti folosi <think>...</think> pentru rationament intern.\n\n'
    '2. ULTIMA linie din raspuns trebuie sa fie EXACT:\n\n'
    '   RASPUNS_FINAL: <valoarea>\n\n'
    '   Exemple: RASPUNS_FINAL: 3  |  RASPUNS_FINAL: x=2 sau x=-5  |  RASPUNS_FINAL: -3/4\n\n'
    '3. Nu adauga nimic dupa linia RASPUNS_FINAL.\n\n'
)

MODEL_COLAB = 'deepseek-r1:14b'
GEMINI_API_KEY = ""   
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"


_executor = ThreadPoolExecutor(max_workers=2)





def _construieste_prompt(problema: str, hint: str, context_retry: str = '') -> str:
    bloc_hint = f'INDICII MATEMATICE RELEVANTE:\n{hint}\n\n' if hint else ''
    baza = _TEMPLATE.format(bloc_hint=bloc_hint, problema=problema)
    if context_retry:
        return (
            f'Raspunsul tau anterior a fost INCORECT sau incomplet: "{context_retry}".\n'
            'Reconsidera complet abordarea. Verifica domeniul de definitie.\n\n' + baza
        )
    return baza


def _apeleaza_ollama(prompt: str, temperatura: float) -> str:
    payload = {
        'model': MODEL_8B,
        'prompt': prompt,
        'stream': True,
        'options': {'temperature': temperatura, 'num_predict': 8192, 'num_ctx': 16384}
    }
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
    """Apel sincron Gemini — folosit atat direct cat si din async wrapper."""
    prompt_formatat = _construieste_prompt(problema, hint="")

    payload = {
        "contents": [{"parts": [{"text": prompt_formatat}]}],
        "generationConfig": {"temperature": 0.1}
    }

    try:
        resp = requests.post(
            GEMINI_URL, json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
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

        if rezultat_extras in ['Extractie Esuata', 'Extractie Esuata']:
            sfarsit = text_brut[-200:].replace('\n', ' | ')
            print(f"  [DEBUG Gemini] Raspuns brut: ...{sfarsit}")
            return 'Extractie Esuata'

        return rezultat_extras

    except requests.exceptions.Timeout:
        print('  [Gemini 2.5] Timeout API.')
        return 'Extractie Esuata'
    except Exception as e:
        print(f'  [Gemini 2.5] Eroare API: {e}')
        return 'Extractie Esuata'





async def _async_run_ns(problema: str, hint: str, loop) -> str:
    """Ruleaza pipeline-ul NS (blocant) pe thread pool."""
    text_brut = await loop.run_in_executor(
        _executor,
        lambda: run_neuro_symbolic_pipeline(problema, hint)
    )
    return extrage_rezultat(text_brut, use_llm_fallback=True)


async def _async_run_gemini(problema: str, loop) -> str:
    """Ruleaza Gemini (blocant) pe thread pool."""
    return await loop.run_in_executor(
        _executor,
        lambda: _apeleaza_pc(problema)
    )





async def _rezolva_async(problema: str, ruleaza_gemini_paralel: bool = True) -> dict:
    """
    Core async.

    ruleaza_gemini_paralel=True   NS + Gemini pornesc simultan (benchmark mode).
    ruleaza_gemini_paralel=False  Gemini doar ca fallback daca NS esueaza
                                   (edge mode, economiseste API calls).
    """
    SEP = '=' * 62
    print(f'\n{SEP}')
    print(f"PROBLEMA: {problema[:80]}{('...' if len(problema) > 80 else '')}")
    print(SEP)

    hint = gaseste_hint(problema)
    print(f'[RAG] {"Reguli semantice detectate." if hint else "Nicio regula specifica."}')

    loop = asyncio.get_event_loop()
    t_start = time.time()

    if ruleaza_gemini_paralel:
        
        
        
        print('\n[ASYNC] NS pipeline + Gemini pornesc in paralel...')

        ns_task = asyncio.create_task(_async_run_ns(problema, hint, loop))
        gemini_task = asyncio.create_task(_async_run_gemini(problema, loop))

        
        rezultat_8b, rezultat_pc = await asyncio.gather(ns_task, gemini_task)

        durata = time.time() - t_start
        print(f'\n  [ASYNC] Ambele taskuri complete in {durata:.1f}s (wall time)')

        decizie = _decide(rezultat_pc, rezultat_8b)

    else:
        
        
        
        print('\n[LAPTOP 8B] -> pornesc pipeline-ul Neuro-Simbolic + RAG...')

        rezultat_8b = await _async_run_ns(problema, hint, loop)
        durata_ns = time.time() - t_start
        print(f'  Durata NS: {durata_ns:.1f}s | Extras: {rezultat_8b}')

        rezultat_pc = "Neapelat"
        if rezultat_8b in ["Extractie Esuata", None, "", "Eroare"]:
            print('\n[SELF-HEALING] NS a esuat  fallback Gemini...')
            t_gem = time.time()
            rezultat_pc = await _async_run_gemini(problema, loop)
            print(f'  [Gemini] {time.time() - t_gem:.1f}s -> {rezultat_pc}')

        decizie = rezultat_8b if rezultat_8b not in ["Extractie Esuata", None, "", "Eroare"] else rezultat_pc

    print(f'\n{SEP}')
    print(f'  PC (Gemini)    : {rezultat_pc}')
    print(f'  Laptop (8B NS) : {rezultat_8b}')
    print(f'  DECIZIE FINALA : {decizie}')
    print(SEP)

    return {'rezultat_pc': rezultat_pc, 'rezultat_8b': rezultat_8b, 'decizie': decizie}





def rezolva(problema: str, paralel: bool = True) -> dict:
    """
    Interfata sincrona — pastreaza compatibilitatea cu benchmarks_evaluator.py.

    paralel=True   NS + Gemini in paralel (default, recomandat pentru benchmark)
    paralel=False  Gemini doar ca fallback (economiseste API calls)
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(
                    asyncio.run, _rezolva_async(problema, paralel)
                )
                return future.result()
        else:
            return loop.run_until_complete(_rezolva_async(problema, paralel))
    except RuntimeError:
        return asyncio.run(_rezolva_async(problema, paralel))


def _decide(rez_pc: str, rez_8b: str) -> str:
    esec = 'Extractie Esuata'
    if rez_pc == esec and rez_8b == esec:
        return 'AMBII AGENTI AU ESUAT'
    if rez_pc == esec:
        return rez_8b
    if rez_8b == esec:
        return rez_pc
    if rez_pc.strip() == rez_8b.strip():
        return rez_pc
    return rez_pc


if __name__ == '__main__':
    
    probleme_benchmark = [
        r'If $-6\leq a \leq -2$ and $3 \leq b \leq 5$, what is the greatest possible value of \left(a+\frac{1}{b}\right)\left(\frac{1}{b}-a\right)?'
    ]
    for p in probleme_benchmark:
        rezolva(p, paralel=False)
        print()