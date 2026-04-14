import re
import requests
import logging
logging.basicConfig(level=logging.INFO, format='[EXTRACTOR] %(message)s')
logger = logging.getLogger(__name__)
SYSTEM_PROMPT_TEMPLATE = 'Esti un asistent matematic precis. Rezolva problema pas cu pas.\n\n\n\n{hint_bloc}\n\n\n\nREGULI OBLIGATORII DE FORMATARE A RASPUNSULUI:\n\n1. Poti folosi tag-urile <think>...</think> pentru rationament intern.\n\n2. ULTIMA linie din raspunsul tau TREBUIE sa fie EXACT in formatul:\n\n   RASPUNS_FINAL: <valoarea_numerica_sau_expresia_simplificata>\n\n\n\n   Exemple corecte:\n\n   RASPUNS_FINAL: 42\n\n   RASPUNS_FINAL: -3/4\n\n   RASPUNS_FINAL: x=5 sau x=-2\n\n   RASPUNS_FINAL: (2, 7)\n\n\n\n3. Nu adauga NIMIC dupa linia RASPUNS_FINAL.\n\n4. Nu scrie "RASPUNS_FINAL:" de mai multe ori.\n\n\n\nPROBLEMA:\n\n{problema}\n\n'

def construieste_prompt(problema: str, hint: str='') -> str:
    if hint:
        hint_bloc = f'INDICIU SIMBOLIC (reguli matematice relevante):\n{hint}\n'
    else:
        hint_bloc = ''
    return SYSTEM_PROMPT_TEMPLATE.format(hint_bloc=hint_bloc, problema=problema)

def extrage_layer1_tag_explicit(text: str) -> str | None:
    pattern = re.compile('(?:RASPUNS_FINAL|raspuns_final|Raspuns\\s*[Ff]inal)\\s*:\\s*(.+?)(?:\\n|$)', re.IGNORECASE)
    matches = pattern.findall(text)
    if matches:
        rezultat = matches[-1].strip()
        rezultat = _curata_rezultat(rezultat)
        if rezultat:
            logger.info(f"Layer 1 success: '{rezultat}'")
            return rezultat
    return None

def extrage_layer2_dupa_think(text: str) -> str | None:
    text_fara_think = re.sub('<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    if not text_fara_think:
        think_match = re.search('<think>(.*?)</think>', text, re.DOTALL)
        if think_match:
            text_fara_think = think_match.group(1)
    patterns = ['x\\s*=\\s*[-\\d.,/\\s]+(?:sau|or|si|and|,)\\s*x\\s*=\\s*[-\\d.,/]+', 'x\\s*=\\s*[-\\d.,/]+', '\\(\\s*[-\\d.,/]+\\s*,\\s*[-\\d.,/]+\\s*\\)', '[-]?\\d+\\s*/\\s*\\d+', '[-]?\\d+[.,]\\d+', '[-]?\\d+']
    for pat in patterns:
        matches = re.findall(pat, text_fara_think, re.IGNORECASE)
        if matches:
            rezultat = _curata_rezultat(matches[-1])
            if rezultat:
                logger.info(f"Layer 2 success: '{rezultat}'")
                return rezultat
    return None

def extrage_layer3_llm_extractor(text_brut: str, ollama_url: str='http://localhost:11434/api/generate', model: str='deepseek-r1:8b') -> str | None:
    prompt_extractor = f'Din textul de mai jos, extrage DOAR valoarea numerica finala sau solutia matematica finala.\n\nRaspunde cu UN SINGUR RAND in formatul: RASPUNS_FINAL: <valoare>\n\nNu adauga explicatii.\n\n\n\nTEXT:\n\n{text_brut[:2000]}  \n\n'
    payload = {'model': model, 'prompt': prompt_extractor, 'stream': False, 'options': {'temperature': 0.0, 'num_predict': 50}}
    try:
        resp = requests.post(ollama_url, json=payload, timeout=30)
        resp.raise_for_status()
        text_extras = resp.json().get('response', '')
        rezultat = extrage_layer1_tag_explicit(text_extras)
        if rezultat:
            logger.info(f"Layer 3 (LLM extractor) success: '{rezultat}'")
            return rezultat
    except Exception as e:
        logger.warning(f'Layer 3 failed: {e}')
    return None

def extrage_rezultat(text_brut: str, use_llm_fallback: bool=True, ollama_url: str='http://localhost:11434/api/generate', model_fallback: str='deepseek-r1:8b') -> str:
    if not text_brut or text_brut.strip() in ('', '\\', '/', '|'):
        logger.warning('Raspuns brut gol sau invalid.')
        return 'Extractie Esuata'
    rezultat = extrage_layer1_tag_explicit(text_brut)
    if rezultat:
        return rezultat
    rezultat = extrage_layer2_dupa_think(text_brut)
    if rezultat:
        return rezultat
    if use_llm_fallback:
        rezultat = extrage_layer3_llm_extractor(text_brut, ollama_url, model_fallback)
        if rezultat:
            return rezultat
    logger.error('Toate layerele de extractie au esuat.')
    logger.debug(f'Text brut problematic (primele 500 chars): {text_brut[:500]}')
    return 'Extractie Esuata'

def _curata_rezultat(s: str) -> str:
    s = s.strip()
    s = re.sub('^[\\\\/*`]+$', '', s)
    s = re.sub('[`*]', '', s)
    s = s.strip()
    return s
if __name__ == '__main__':
    teste = ['Am rezolvat ecuatia.\n<think>calcul intern</think>\nDeci solutia este x=5.\nRASPUNS_FINAL: 5', 'RASPUNS_FINAL: 3\n... de fapt RASPUNS_FINAL: 7', '\\', '<think>2x+4=10, deci 2x=6, x=3</think>\nRaspunsul este 3.', 'Solutia ecuatiei este -3/4.\nRASPUNS_FINAL: -3/4', 'x=2 sau x=-5\nRASPUNS_FINAL: x=2 sau x=-5']
    print('=== TEST EXTRACTOR ===\n')
    for i, t in enumerate(teste):
        rez = extrage_rezultat(t, use_llm_fallback=False)
        print(f"Test {i + 1}: '{rez}'")
        print(f'  Input: {repr(t[:80])}\n')
