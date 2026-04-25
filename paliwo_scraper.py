import requests
import json

def pobierz_ceny():
    # Oficjalne API rządu UK
    url = "https://www.gov.uk/guidance/fuel-prices-api/data.json"
    target_postcode = "GL3"
    
    try:
        print(f"Pobieranie danych z {url}...")
        response = requests.get(url, timeout=15)
        response.raise_for_status() # Sprawdzi czy nie ma błędu 404/500
        data = response.json()
        
        raw_stations = data.get('stations', [])
        print(f"Pobrano łącznie {len(raw_stations)} stacji z całego UK.")

        stations = []
        for s in raw_stations:
            pc = s.get('postcode', '').upper().replace(" ", "")
            # Sprawdzamy czy kod pocztowy zaczyna się od GL3
            if pc.startswith(target_postcode):
                prices = s.get('prices', {})
                stations.append({
                    "stacja": s.get('brand', 'Nieznana'),
                    "miejsce": s.get('name', 'Brak nazwy'),
                    "cena": prices.get('E10', '0'),
                    "diesel": prices.get('B7', '0'),
                    "postcode": s.get('postcode', '')
                })
        
        # Jeśli lista jest pusta, spróbujmy złapać cokolwiek z Gloucester (GL) 
        # żeby plik nie był pusty podczas testów
        if not stations:
            print("Nie znaleziono nic dla GL3, szukam dla GL...")
            for s in raw_stations:
                if s.get('postcode', '').upper().startswith('GL'):
                    stations.append({
                        "stacja": s.get('brand', 'Nieznana'),
                        "cena": s.get('prices', {}).get('E10', '0'),
                        "postcode": s.get('postcode', '')
                    })

        # Sortowanie po cenie (jeśli cena to liczba)
        stations.sort(key=lambda x: float(x['cena']) if str(x['cena']).replace('.','').isdigit() and float(x['cena']) > 0 else 999)

        with open('ceny.json', 'w', encoding='utf-8') as f:
            json.dump(stations, f, ensure_ascii=False, indent=4)
        
        print(f"Sukces! Zapisano {len(stations)} stacji do ceny.json")
            
    except Exception as e:
        print(f"WYSTĄPIŁ BŁĄD: {e}")
        with open('ceny.json', 'w') as f:
            json.dump([{"error": str(e)}], f)

if __name__ == "__main__":
    pobierz_ceny()
