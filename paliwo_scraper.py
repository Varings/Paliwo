import os
import json
import google.generativeai as genai

def pobierz_ceny_przez_ai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("BŁĄD: Brak klucza API w Secrets!")
        return

    genai.configure(api_key=api_key)
    
    # Lista modeli Gemini 3 według Twoich release notes z 2026
    modele_do_testu = ['gemini-3.1-pro-preview', 'gemini-3.1-flash-preview', 'gemini-3-pro-preview']
    
    response = None
    prompt = """
    Check real-time petrol (E10) prices for GL3 (Gloucester, UK). 
    Search for Tesco Brockworth and Shell. 
    Return ONLY a JSON list of objects.
    Format: [{"stacja": "Tesco", "cena": 142.9, "postcode": "GL3"}]
    """

    for model_name in modele_do_testu:
        try:
            print(f"Próbuję użyć modelu: {model_name}...")
            # W Gemini 3 Search jest często domyślnie dostępny lub jako narzędzie
            model = genai.GenerativeModel(
                model_name=model_name,
                tools=[{'google_search_retrieval': {}}]
            )
            response = model.generate_content(prompt)
            if response:
                print(f"Sukces z modelem {model_name}!")
                break
        except Exception as e:
            print(f"Model {model_name} nie odpowiedział: {e}")
            continue

    if not response:
        print("Żaden model Gemini 3 nie zadziałał. Sprawdź limity na koncie.")
        return

    try:
        # Oczyszczanie i zapisywanie danych
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        data = json.loads(text)

        with open('ceny.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print("Plik ceny.json został zaktualizowany przez Gemini 3!")

    except Exception as e:
        print(f"Błąd przetwarzania JSON: {e}")
        with open('ceny.json', 'w') as f:
            json.dump([{"error": "JSON parse error", "details": str(e)}], f)

if __name__ == "__main__":
    pobierz_ceny_przez_ai()
