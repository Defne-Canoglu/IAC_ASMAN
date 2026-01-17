import openmeteo_requests
import config

def hava_durumu_getir():
    # Koordinatların merkez noktasını bul
    coords = [float(x) for x in config.HEDEF_KOORDINATLAR.split(',')]
    lat = (coords[1] + coords[3]) / 2
    lon = (coords[0] + coords[2]) / 2

    print(f"\n🌍 Konum Taranıyor: Enlem {lat:.2f}, Boylam {lon:.2f}")
    
    # Open-Meteo API'sine bağlan
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "soil_moisture_0_to_1cm"]
    }
    
    try:
        responses = openmeteo_requests.Client().weather_api(url, params=params)
        response = responses[0]
        current = response.Current()
        
        # Verileri sözlük yap
        veriler = {
            "Sicaklik_C": current.Variables(0).Value(),
            "Nem_Yuzde": current.Variables(1).Value(),
            "Ruzgar_Hizi_kmh": current.Variables(2).Value(),
            "Toprak_Nemi": current.Variables(3).Value()
        }
        
        print(f"🌡️  Anlık Veriler: {veriler}")
        return veriler
        
    except Exception as e:
        print(f"❌ Hava durumu hatası: {e}")
        return None

if __name__ == "__main__":
    hava_durumu_getir()