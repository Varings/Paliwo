import os
import json
import google.generativeai as genai

def pobierz_ceny_przez_ai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("BŁĄD: Brak klucza API!")
        return

    genai.configure(api_key=api_key)
    
    # Wersja 2026: Poprawna deklaracja narzędzia wyszukiwania
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        tools=[{'google_search_retrieval': {}}] # ZMIANA: dodano _retrieval
    )

    prompt = """
    Search the internet for current petrol (E10) prices in GL3 (Gloucester, UK). 
    Focus on Tesco Brockworth and Shell. 
    Return ONLY a JSON list of objects.
    Format: [{"stacja": "Tesco", "cena": 142.9, "postcode": "GL3"}]
    """

    try:
        print("Łączę się z Gemini 1.5 Pro (Search Mode)...")
        response = model.generate_content(prompt)
        
        # Wyciąganie czystego JSONa
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        data = json.loads(text)

        with open('ceny.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"SUKCES! Zapisano dane dla {len(data)} stacji.")

    except Exception as e:
        print(f"Błąd krytyczny: {e}")
        # Tworzymy plik z błędem dla HA
        with open('ceny.json', 'w') as f:
            json.dump([{"error": str(e)}], f)

if __name__ == "__main__":
    pobierz_ceny_przez_ai()
