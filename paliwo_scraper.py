import os
import json
import google.generativeai as genai

def pobierz_ceny_przez_ai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("BŁĄD: Brak klucza API!")
        return

    genai.configure(api_key=api_key)

    # Według logu błędu 400, Twój plan wymaga nazwy 'google_search'
    tools = [{"google_search": {}}]

    try:
        # Korzystamy z Gemini 3.1 Pro (zgodnie z Twoją prośbą o najnowszą wersję)
        model = genai.GenerativeModel(
            model_name='gemini-3.1-pro-preview',
            tools=tools
        )

        prompt = """
        Search the internet for current petrol (E10) prices in GL3 (Gloucester, UK). 
        Specifically look for Tesco Brockworth and Shell.
        Return ONLY a JSON list of objects.
        Required format: [{"stacja": "Tesco", "cena": 142.9, "postcode": "GL3", "data_sprawdzenia": "YYYY-MM-DD"}]
        """

        print("Agent Gemini 3.1 Pro przeszukuje internet...")
        
        # Wymuszamy czysty format JSON
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        data = json.loads(response.text)
        print(f"Sukces! Pobrano dane dla: {len(data)} stacji.")

    except Exception as e:
        print(f"Wystąpił błąd podczas pracy AI: {e}")
        data = [{"stacja": "Błąd AI", "cena": 0, "error": str(e)}]

    # Zapis do pliku - zawsze wykonywany, aby GitHub Actions nie zgłosiło błędu 128
    with open('ceny.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Plik ceny.json został zaktualizowany.")

if __name__ == "__main__":
    pobierz_ceny_przez_ai()
