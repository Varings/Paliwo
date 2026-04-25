import os
import json
from google import genai
from google.genai import types

def pobierz_ceny_przez_ai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("BŁĄD: Brak klucza API!")
        return

    # Nowy Klient - Standard 2026
    client = genai.Client(api_key=api_key)
    model_id = "gemini-3.1-pro" 

    try:
        prompt = """
        Search the internet for current petrol (E10) prices in GL3 (Gloucester, UK). 
        Focus on Tesco Brockworth and Shell. 
        Return ONLY a JSON list of objects.
        Format: [{"stacja": "Tesco", "cena": 142.9, "postcode": "GL3"}]
        """

        print(f"Agent {model_id} przeszukuje internet...")

        # Nowa składnia wywołania
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                response_mime_type="application/json"
            )
        )
        
        data = json.loads(response.text)
        print("Sukces! Dane pobrane.")

    except Exception as e:
        print(f"Błąd: {e}")
        # Tworzymy plik z błędem, aby Git go widział
        data = [{"stacja": "Błąd AI", "cena": 0, "error": str(e)}]

    with open('ceny.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    pobierz_ceny_przez_ai()
