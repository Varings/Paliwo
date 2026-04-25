import os
import json
import google.generativeai as genai

def pobierz_ceny_przez_ai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("BŁĄD: Brak klucza API!")
        return

    genai.configure(api_key=api_key)
    
    # Korzystamy z modelu 1.5 Pro (najbardziej stabilny Search) 
    # lub gemini-3.1-pro-preview jeśli wolisz nowszy
    model = genai.GenerativeModel('gemini-3.1-pro-preview')

    prompt = """
    Search the internet for current petrol (E10) prices in GL3 (Gloucester, UK). 
    Check Tesco Brockworth and Shell. 
    Return ONLY a JSON list: [{"stacja": "Tesco", "cena": 142.9, "postcode": "GL3"}]
    """

    try:
        # Wersja 2026: Grounding (wyszukiwanie) wywołujemy bezpośrednio w parametrze
        print("Agent Gemini szuka aktualnych cen...")
        response = model.generate_content(prompt, tools="google_search_retrieval")
        
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        data = json.loads(text)
        print("Sukces! Dane pobrane i przetworzone.")

    except Exception as e:
        print(f"Błąd podczas pobierania: {e}")
        data = [{"stacja": "Błąd AI", "cena": 0, "error": str(e)}]

    with open('ceny.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Plik ceny.json zaktualizowany.")

if __name__ == "__main__":
    pobierz_ceny_przez_ai()
