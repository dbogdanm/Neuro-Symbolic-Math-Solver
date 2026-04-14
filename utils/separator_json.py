import json


fisier_intrare = 'tests/svamp.json'
fisier_iesire = 'svamp_no_answers.json'

try:
    
    with open(fisier_intrare, 'r', encoding='utf-8') as f:
        date_originale = json.load(f)

    
    
    date_filtrate = [
        {
            "ID": item.get("ID"),
            "Body": item.get("Body"),
            "Question": item.get("Question")
        }
        for item in date_originale
    ]

    
    with open(fisier_iesire, 'w', encoding='utf-8') as f:
        json.dump(date_filtrate, f, indent=4, ensure_ascii=False)

    print(f"Succes! Am extras {len(date_filtrate)} intrari in '{fisier_iesire}'.")

except FileNotFoundError:
    print(f"Eroare: Nu am gasit fisierul '{fisier_intrare}'. Asigura-te ca e in acelasi folder.")
except Exception as e:
    print(f"A aparut o eroare neasteptata: {e}")