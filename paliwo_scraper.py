import os
import json
import google.generativeai as genai

def pobierz_ceny_przez_ai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("BŁĄD: Brak klucza API w Secrets!")
        return

    genai.configure(api_key=api_key)
    
    # Deklarujemy narzędzie wyszukiwania zgodnie ze standardem Gemini 3.1
    # Używamy modelu 3.1 Pro, który widnieje w Twoich notatkach jako najnowszy
    try:
        model = genai.GenerativeModel(
            model_name='gemini-3.1-pro-preview',
            tools=[{'google_search': {}}]
        )

        prompt = """
        Search the internet for current petrol (E10) prices in GL3 (Gloucester, UK). 
        Focus on Tesco Brockworth and Shell. 
        Return ONLY a JSON list of objects.
        Format: [{"stacja": "Tesco", "cena": 142.9, "postcode": "GL3"}]
        """

        print("Agent Gemini 3.1 Pro szuka cen w Google...")
        response = model.generate_content(prompt)
        
        # Oczyszczanie tekstu (AI czasem dodaje ```json ... ```)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        data = json.loads(text)
        print("Sukces! Dane pobrane.")

    except Exception as e:
        print(f"Błąd podczas pracy Gemini 3.1: {e}")
        # Bezpiecznik: tworzymy plik z błędem, aby Git go znalazł
        data = [{"stacja": "Błąd AI", "cena": 0, "error": str(e)}]

    # Zapisujemy plik poza blokiem try, aby zawsze istniał dla Gita
    with open('ceny.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Plik ceny.json został wygenerowany.")

if __name__ == "__main__":
    pobierz_ceny_przez_ai()
