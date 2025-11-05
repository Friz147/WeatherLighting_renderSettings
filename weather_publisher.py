# 6fdc3167d0d06b03feff626be5e2f283 API key to openweather

import time
import json
import requests
import paho.mqtt.client as mqtt

# === CONFIG ===
CITY = "Lecco,it"
API_KEY = "6fdc3167d0d06b03feff626be5e2f283"
BROKER = "test.mosquitto.org"
TOPIC = "meteo/torretta1"
INTERVAL = 10  # secondi tra un aggiornamento e l’altro

def get_weather():
    """Ottiene i dati meteo reali da OpenWeather."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=it"
    response = requests.get(url)
    data = response.json()
    
    weather = {
        "temperatura": data["main"]["temp"],
        "umidita": data["main"]["humidity"],
        "condizione": data["weather"][0]["description"],
        "vento": data["wind"]["speed"]
    }
    return weather

def main():
    client = mqtt.Client()
    print(f"Connessione a {BROKER}...")
    client.connect(BROKER, 1883, 60)
    print("Connesso! Inizio pubblicazione meteo...\n")

    try:
        while True:
            meteo = get_weather()
            payload = json.dumps(meteo)
            client.publish(TOPIC, payload)
            print(f"[PUB] {TOPIC} → {payload}")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Terminato.")
        client.disconnect()

if __name__ == "__main__":
    main()
