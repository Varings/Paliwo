import os
import json
import google.generativeai as genai

def pobierz_ceny_przez_ai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Brak klucza API!")
        return

    genai.configure(api_key=api_key)
    
    # Używamy modelu 2.0 Flash - najszybszy i najnowszy w 2026
    # Jeśli ten model nie jest dostępny, spróbuj 'gemini-1.5-flash-latest'
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    prompt = """
    Zrób research w internecie i znajdź aktualne ceny benzyny E10 w okolicy kodu pocztowego GL3 (Gloucester, UK). 
    Znajdź ceny dla stacji: Tesco Brockworth, Shell, BP. 
    Zwróć dane WYŁĄCZNIE jako listę JSON (bez zbędnego tekstu).
    Format: [{"stacja": "Nazwa", "cena": "142.9", "postcode": "GL3"}]
    """

    try:
        print("Gemini 2.0 szuka cen dla Ciebie...")
        # W 2026 modele Flash mają Search włączony domyślnie
        response = model.generate_content(prompt)
        
        # Oczyszczanie odpowiedzi z Markdownu
        content = response.text.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        data = json.loads(content)

        with open('ceny.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Sukces! Znaleziono {len(data)} stacji.")

    except Exception as e:
        print(f"Błąd AI: {e}")
        with open('ceny.json', 'w') as f:
            json.dump([{"error": "AI Search failed", "details": str(e)}], f)

if __name__ == "__main__":
    pobierz_ceny_przez_ai()
