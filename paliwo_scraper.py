import os
import json
import google.generativeai as genai

def pobierz_ceny_przez_ai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("BŁĄD: Brak klucza API!")
        return

    genai.configure(api_key=api_key)
    
    # ZMIANA: Dla Gemini 1.5 używamy 'google_search_retrieval'
    # 'google_search' jest używane w nowym SDK (google-genai) lub modelach 2.0+
    tools_config = [{'google_search_retrieval': {}}]

    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-pro',
            tools=tools_config
        )

        prompt = """
        Search the internet for current petrol (E10) prices in GL3 (Gloucester, UK). 
        Focus on Tesco Brockworth and Shell. 
        Return ONLY a JSON list of objects.
        Format: [{"stacja": "Tesco", "cena": 142.9, "postcode": "GL3"}]
        """

        print("Agent Gemini (Search Mode) sprawdza ceny...")
        
        # Opcjonalnie: dodanie generation_config wymuszającego JSON
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Parsowanie odpowiedzi
        data = json.loads(response.text)
        print("Sukces! Dane pobrane.")

    except Exception as e:
        print(f"Błąd: {e}")
        data = [{"stacja": "Błąd AI", "cena": 0, "error": str(e)}]

    # Zapis do pliku
    with open('ceny.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Plik ceny.json zaktualizowany.")

if __name__ == "__main__":
    pobierz_ceny_przez_ai()
