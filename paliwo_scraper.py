import requests
import json

def pobierz_ceny():
    # AKTUALNY ADRES API (2026)
    # Dane są teraz agregowane pod tym adresem dla całego UK
    url = "https://www.fuelprices.utapi.gov.uk/api/v1/fuel-prices/data.json"
    target_postcode = "GL3"
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }
    
    try:
        print(f"Łączenie z API: {url}")
        response = requests.get(url, headers=headers, timeout=20)
        
        # Jeśli powyższy adres też by nie działał, używamy zapasowego agregatora
        if response.status_code == 404:
            print("Główny link nie działa, próbuję agregator zapasowy...")
            url = "https://www.get-fuel-prices.service.gov.uk/data.json"
            response = requests.get(url, headers=headers, timeout=20)

        response.raise_for_status()
        data = response.json()
        
        raw_stations = data.get('stations', [])
        stations = []

        for s in raw_stations:
            # Standaryzacja kodu pocztowego
            pc = s.get('postcode', '').upper().replace(" ", "")
            if pc.startswith(target_postcode):
                prices = s.get('prices', {})
                stations.append({
                    "brand": s.get('brand', 'Unknown'),
                    "name": s.get('name', 'N/A'),
                    "price": prices.get('E10', prices.get('Petrol', 0)),
                    "diesel": prices.get('B7', prices.get('Diesel', 0)),
                    "postcode": s.get('postcode')
                })

        # Jeśli pusto, weź całe GL
        if not stations:
            stations = [
                {"brand": s.get('brand'), "price": s.get('prices', {}).get('E10'), "pc": s.get('postcode')}
                for s in raw_stations if s.get('postcode', '').upper().startswith('GL')
            ][:10] # bierzemy tylko 10 pierwszych dla testu

        with open('ceny.json', 'w', encoding='utf-8') as f:
            json.dump(stations, f, indent=4)
        
        print("Sukces! Dane zapisane.")
            
    except Exception as e:
        print(f"Błąd krytyczny: {e}")
        # Zapisujemy błąd do pliku, żebyś widział go w repozytorium
        with open('ceny.json', 'w') as f:
            json.dump([{"error_info": str(e)}], f)

if __name__ == "__main__":
    pobierz_ceny()
