import requests
import json

URL_COLAB = 'trycloudflare.com/api/generate'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("Scrie 'exit' pentru a iesi.\n")

while True:
    intrebare = input('\nTu: ')
    if intrebare.lower() in ['exit', 'quit']:
        break

    payload = {
        'model': 'deepseek-r1:14b',
        'prompt': intrebare,
        'stream': True
    }

    try:
        print('14B: ', end='', flush=True)
        response = requests.post(URL_COLAB, json=payload, headers=HEADERS, stream=True, timeout=120)

        if response.status_code != 200:
            print(f"\n[Eroare HTTP {response.status_code}]:")
            print(response.text[:200])
            continue

        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode('utf-8'))
                print(chunk.get('response', ''), end='', flush=True)
                if chunk.get('done'):
                    break
        print()

    except Exception as e:
        print(f'\n[Eroare]: {e}')