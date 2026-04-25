import os
import json
import google.generativeai as genai

def pobierz_ceny_przez_ai():
    # Pobieramy klucz z sekretów GitHub
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Brak klucza API!")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = """
    Search the internet for current petrol prices in the GL3 (Gloucester) area, UK. 
    Focus on stations like Tesco, Shell, or BP near GL3 4ZL. 
    Return the data ONLY as a JSON list of objects with keys: "stacja", "cena", "postcode".
    Example format: [{"stacja": "Tesco", "cena": "142.9", "postcode": "GL3 4ZL"}]
    """

    try:
        print("Gemini szuka cen dla Ciebie...")
        response = model.generate_content(prompt)
        
        # Wyciągamy tekst JSON z odpowiedzi AI
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(clean_json)

        with open('ceny.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print("Sukces! Gemini dostarczyło dane.")

    except Exception as e:
        print(f"Błąd AI: {e}")
        with open('ceny.json', 'w') as f:
            json.dump([{"error": "AI Search failed", "details": str(e)}], f)

if __name__ == "__main__":
    pobierz_ceny_przez_ai()
