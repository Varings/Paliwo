import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.fuel-finder.uk/?q=gl3+4zl&lat=51.849030&lng=-2.170875&radius=10&fuel=petrol"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def pobierz_ceny():
    try:
        response = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        stations_data = []

        # Nowy, szerszy sposób szukania - szukamy wszystkich divów, które mogą zawierać ceny
        # Szukamy tekstu zawierającego 'p' (jak pence) obok liczb
        for item in soup.find_all(['div', 'tr', 'li']):
            text = item.get_text(separator=' ', strip=True)
            if 'p' in text and any(char.isdigit() for char in text):
                # Prosta logika wyciągania danych z tekstu, jeśli klasa zawiodła
                lines = text.split()
                if len(lines) > 2:
                    stations_data.append({
                        "info": text[:100] # Zapisujemy początek tekstu, żeby zobaczyć co złapał
                    })

        # Jeśli powyższe nie zadziała, używamy konkretnych klas (stan na kwiecień 2026)
        # Spróbujmy znaleźć kontenery stacji po specyficznych słowach
        stations = soup.select('div[class*="station"], div[class*="result"]')
        
        results = []
        for s in stations:
            # Szukamy ceny (zazwyczaj duża liczba z literą p)
            price_elem = s.find(string=lambda x: 'p' in x and any(c.isdigit() for c in x))
            name_elem = s.find(['h3', 'h4', 'strong'])
            
            if price_elem and name_elem:
                results.append({
                    "stacja": name_elem.get_text().strip(),
                    "cena": price_elem.strip(),
                    "odleglosc": "GL3 area"
                })

        with open('ceny.json', 'w', encoding='utf-8') as f:
            json.dump(results if results else [{"error": "Nie znaleziono stacji, sprawdz kod strony"}], f, ensure_ascii=False, indent=4)

    except Exception as e:
        with open('ceny.json', 'w') as f:
            json.dump([{"error": str(e)}], f)

if __name__ == "__main__":
    pobierz_ceny()
