import requests
import json

def pobierz_ceny():
    # Oficjalne API rządu UK - najbezpieczniejsze rozwiązanie w 2026
    url = "https://www.gov.uk/guidance/fuel-prices-api/data.json"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Filtrujemy stacje zaczynające się od Twojego kodu pocztowego GL3
        stations = [
            {
                "stacja": s.get('brand', 'Nieznana'),
                "cena": s.get('prices', {}).get('E10', '0'),
                "odleglosc": s.get('postcode', '')
            }
            for s in data.get('stations', [])
            if s.get('postcode', '').startswith('GL3')
        ]
        
        # Sortujemy od najtańszej
        stations.sort(key=lambda x: float(x['cena']) if str(x['cena']).replace('.','').isdigit() else 999)

        with open('ceny.json', 'w', encoding='utf-8') as f:
            json.dump(stations, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        with open('ceny.json', 'w') as f:
            json.dump([{"error": str(e)}], f)

if __name__ == "__main__":
    pobierz_ceny()
