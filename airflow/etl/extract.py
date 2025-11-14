import requests
import pandas as pd
import logging
import os
import time

# ==========================
# CONFIGURATION
# ==========================
API_KEY = "970513d5c813ea00609b42818eb3a3ee"  # ta clé OpenWeather
CITIES = ["Paris", "Lyon", "Marseille"]

# Dossier de sortie
os.makedirs("data/raw", exist_ok=True)
OUTPUT_PATH = "data/raw/weather_multi.csv"

# ==========================
# LOGGING
# ==========================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ==========================
# FONCTION D'EXTRACTION
# ==========================
def extract_weather(city: str, api_key: str) -> pd.DataFrame:
    """Extrait les données météo depuis l'API OpenWeather pour une ville donnée"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    logging.info(f"Appel de l'API pour la ville : {city}")
    response = requests.get(url)
    response.raise_for_status()  # Vérifie si l'appel a échoué

    data = response.json()

    weather_dict = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "datetime": pd.to_datetime("now")
    }

    return pd.DataFrame([weather_dict])

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    all_data = []

    for city in CITIES:
        try:
            df_city = extract_weather(city, API_KEY)
            all_data.append(df_city)
            time.sleep(1)  # petite pause pour éviter de surcharger l’API
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur lors de l'appel API pour {city} : {e}")

    if all_data:
        df_final = pd.concat(all_data, ignore_index=True)
        df_final.to_csv(OUTPUT_PATH, index=False)
        logging.info(f"Données sauvegardées dans : {OUTPUT_PATH}")
        print(df_final)
    else:
        logging.warning("Aucune donnée n'a été extraite.")
