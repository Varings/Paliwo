import requests
from bs4 import BeautifulSoup
import json
import re

def pobierz_ceny():
    # Ten link działał w przeglądarce, więc użyjemy go jako źródła
    url = "https://www.fuel-finder.uk/?q=gl3+4zl&lat=51.849030&lng=-2.170875&radius=10&fuel=petrol"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
    }

    try:
        print(f"Pobieranie strony: {url}")
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        stations = []

        # W 2026 strony często ukrywają dane wewnątrz skryptów JSON-LD lub prostych tabel
        # Szukamy wszystkich bloków, które wyglądają jak stacje paliw
        # Szukamy po klasach CSS, które są standardem dla tej witryny
        cards = soup.find_all(['div', 'li'], class_=re.compile(r'station|result|item', re.I))

        for card in cards:
            text = card.get_text(separator='|', strip=True)
            # Szukamy wzorca ceny (np. 142.9p lub 142.9)
            price_match = re.search(r'(\d{2,3}\.\d)', text)
            
            if price_match:
                # Próbujemy wyłuskać nazwę (zazwyczaj pierwszy tekst przed ceną)
                parts = text.split('|')
                brand = parts[0] if len(parts) > 0 else "Unknown"
                
                stations.append({
                    "stacja": brand,
                    "cena": price_match.group(1),
                    "postcode": "GL3",
                    "raw": text[:50] # dla debugowania
                })

        # Jeśli selektory zawiodły, szukamy po prostu liczb obok słowa 'p' lub '£'
        if not stations:
            print("Szukam wzorców tekstowych...")
            all_text = soup.get_text(separator=' ')
            prices = re.findall(r'([A-Za-z0-9\s]+)\s+(\d{3}\.\d)p', all_text)
            for p in prices:
                stations.append({"stacja": p[0].strip()[-15:], "cena": p[1], "postcode": "GL3"})

        # Jeśli nadal nic (np. blokada bota), zapisz wiadomość o błędzie
        if not stations:
             stations = [{"stacja": "Brak danych - strona zmieniła układ", "cena": "0"}]

        with open('ceny.json', 'w', encoding='utf-8') as f:
            json.dump(stations, f, indent=4)
        
        print(f"Zakończono. Znaleziono: {len(stations)}")

    except Exception as e:
        print(f"Błąd: {e}")
        with open('ceny.json', 'w') as f:
            json.dump([{"error": "Scraping failed", "details": str(e)}], f)

if __name__ == "__main__":
    pobierz_ceny()
