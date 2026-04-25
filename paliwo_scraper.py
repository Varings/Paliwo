import requests
import json

def pobierz_ceny():
    # To jest najbardziej stabilny agregator danych rządowych w UK
    url = "https://www.petrolprices.com/public-api/fuel-prices-data.json"
    # Zapasowy adres (jeśli powyższy by zawiódł)
    backup_url = "https://get-fuel-prices.service.gov.uk/data.json"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        print("Próba pobrania danych...")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
        except:
            print("Pierwszy link zawiódł, próbuję zapasowy...")
            response = requests.get(backup_url, headers=headers, timeout=15)
            response.raise_for_status()

        data = response.json()
        stations = []
        
        # Przeszukujemy stacje
        for s in data.get('stations', []):
            pc = s.get('postcode', '').upper().replace(" ", "")
            # Szukamy wszystkiego co zaczyna się od GL3 lub GL (Gloucester)
            if pc.startswith("GL3") or pc.startswith("GL1"):
                prices = s.get('prices', {})
                stations.append({
                    "brand": s.get('brand', 'Unknown'),
                    "name": s.get('name', 'N/A'),
                    "price": prices.get('E10', prices.get('Petrol', '0')),
                    "diesel": prices.get('B7', prices.get('Diesel', '0')),
                    "postcode": s.get('postcode')
                })

        # Sortowanie po cenie benzyny
        stations.sort(key=lambda x: float(x['price']) if str(x['price']).replace('.','').isdigit() and float(x['price']) > 0 else 999)

        with open('ceny.json', 'w', encoding='utf-8') as f:
            json.dump(stations, f, indent=4)
        
        print(f"Sukces! Znaleziono {len(stations)} stacji.")
            
    except Exception as e:
        print(f"Błąd: {e}")
        with open('ceny.json', 'w') as f:
            json.dump([{"error": "API currently unavailable", "details": str(e)}], f)

if __name__ == "__main__":
    pobierz_ceny()
