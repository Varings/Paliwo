import requests
from bs4 import BeautifulSoup
import json

# Twój konkretny link
URL = "https://www.fuel-finder.uk/?q=gl3+4zl&lat=51.849030&lng=-2.170875&radius=10&fuel=petrol"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def pobierz_ceny():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    stations_data = []

    # Szukamy stacji na stronie fuel-finder.uk
    stations = soup.find_all('div', class_='station-container')
    
    for s in stations:
        try:
            nazwa = s.find('h3').text.strip()
            cena = s.find('span', class_='price').text.strip()
            odleglosc = s.find('span', class_='distance').text.strip()
            
            stations_data.append({
                "stacja": nazwa,
                "cena": cena,
                "odleglosc": odleglosc
            })
        except:
            continue

    with open('ceny.json', 'w', encoding='utf-8') as f:
        json.dump(stations_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    pobierz_ceny()
