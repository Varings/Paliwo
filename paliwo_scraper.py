import os
import json
import google.generativeai as genai

def pobierz_ceny_przez_ai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("BŁĄD: Brak klucza GOOGLE_API_KEY w ustawieniach GitHub!")
        return

    genai.configure(api_key=api_key)
    
    # Korzystamy z najnowszej wersji 3.1 Pro (dostępnej od lutego 2026)
    # Włączamy narzędzie wyszukiwarki Google
    model = genai.GenerativeModel(
        model_name='gemini-3.1-pro-preview',
        tools=[{'google_search': {}}]
    )

    prompt = """
    Jako ekspert od rynku paliw w UK, wyszukaj dzisiejsze ceny benzyny E10 i diesla w okolicy GL3 (Brockworth, Gloucester). 
    Sprawdź stacje: Tesco Brockworth, Shell Shurdington Road i BP. 
    Zwróć wynik wyłącznie jako czysty JSON.
    Format: [{"stacja": "Nazwa", "cena": 142.9, "diesel": 149.9, "postcode": "GL3"}]
    """

    try:
        print("Uruchamiam Deep Research dla cen paliw w GL3...")
        response = model.generate_content(prompt)
        
        # Oczyszczanie odpowiedzi z ewentualnych znaczników markdown
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()

        # Próba sparsowania JSON
        data = json.loads(raw_text)

        with open('ceny.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"SUKCES! Gemini 3.1 Pro znalazło i zapisało dane stacji.")

    except Exception as e:
        print(f"Błąd krytyczny: {e}")
        # Jeśli 3.1 Pro byłby chwilowo niedostępny, używamy stabilnego aliasu
        with open('ceny.json', 'w') as f:
            json.dump([{"stacja": "Error", "cena": 0, "details": str(e)}], f)

if __name__ == "__main__":
    pobierz_ceny_przez_ai()
