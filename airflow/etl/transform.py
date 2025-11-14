import pandas as pd
import os

# ==========================
# CONFIGURATION
# ==========================
INPUT_PATH = "data/raw/weather_multi.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "weather_multi_clean.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================
# FONCTION DE TRANSFORMATION
# ==========================
def transform_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie et enrichit les données météo"""
    print("🔄 Début de la transformation des données...")

    # 🔹 Normaliser les noms de colonnes
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # 🔹 Supprimer les doublons (si plusieurs exécutions)
    df = df.drop_duplicates()

    # 🔹 Ajouter une colonne température Fahrenheit
    df["temperature_f"] = df["temperature"] * 9/5 + 32

    # 🔹 Ajouter la date du jour (utile pour historiser)
    df["date"] = pd.to_datetime("now").date()

    # 🔹 Réorganiser les colonnes pour la clarté
    df = df[["date", "city", "temperature", "temperature_f", "humidity", "pressure", "weather", "wind_speed", "datetime"]]

    print("✅ Transformation terminée avec succès !")
    return df

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    try:
        print(f"📂 Lecture du fichier brut : {INPUT_PATH}")
        df_raw = pd.read_csv(INPUT_PATH)

        df_transformed = transform_weather_data(df_raw)

        df_transformed.to_csv(OUTPUT_PATH, index=False)
        print(f"💾 Données transformées sauvegardées dans : {OUTPUT_PATH}")
        print(df_transformed.head())

    except FileNotFoundError:
        print("❌ Fichier source introuvable. Exécute d'abord extract.py.")
    except Exception as e:
        print(f"⚠️ Erreur lors de la transformation : {e}")
