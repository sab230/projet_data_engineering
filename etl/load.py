import os
import pandas as pd
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

# ==========================
# CHARGEMENT DU .ENV
# ==========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

print("DEBUG - Compte :", os.getenv("SNOWFLAKE_ACCOUNT"))
print("DEBUG - Utilisateur :", os.getenv("SNOWFLAKE_USER"))
print("DEBUG - Mot de passe présent :", bool(os.getenv("SNOWFLAKE_PASSWORD")))

# ==========================
# CONFIG
# ==========================
INPUT_PATH = "data/processed/weather_multi_clean.csv"

conn_params = {
    "account":   os.getenv("SNOWFLAKE_ACCOUNT"),
    "user":      os.getenv("SNOWFLAKE_USER"),
    "password":  os.getenv("SNOWFLAKE_PASSWORD"),
    "role":      os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "WH_DE"),
    "database":  os.getenv("SNOWFLAKE_DATABASE", "WEATHER_DB"),
    "schema":    os.getenv("SNOWFLAKE_SCHEMA", "RAW"),
}

# ==========================
# LOAD LOGIC
# ==========================
def main():
    print("📥 Lecture du fichier transformé…")
    df = pd.read_csv(INPUT_PATH)

    # Harmoniser les colonnes
    df.columns = [c.strip().upper() for c in df.columns]

    expected_cols = [
        "DATE", "CITY", "TEMPERATURE", "TEMPERATURE_F",
        "HUMIDITY", "PRESSURE", "WEATHER", "WIND_SPEED", "DATETIME"
    ]
    df = df[expected_cols]

    # Conversion des types
    # Conversion des types
    df["DATE"] = pd.to_datetime(df["DATE"]).dt.date
    df["DATETIME"] = pd.to_datetime(df["DATETIME"]).dt.strftime("%Y-%m-%d %H:%M:%S")


    print("🔌 Connexion à Snowflake…")
    with connect(**conn_params) as conn:
        # Sélectionner la base et le schéma
        with conn.cursor() as cur:
            cur.execute(f"USE DATABASE {conn_params['database']}")
            cur.execute(f"USE SCHEMA {conn_params['schema']}")
            # Créer la table si elle n'existe pas
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS WEATHER_CURRENT (
                    DATE DATE,
                    CITY STRING,
                    TEMPERATURE FLOAT,
                    TEMPERATURE_F FLOAT,
                    HUMIDITY NUMBER,
                    PRESSURE NUMBER,
                    WEATHER STRING,
                    WIND_SPEED FLOAT,
                    DATETIME TIMESTAMP_NTZ
                )
            """)

        print("⏫ Écriture en masse avec write_pandas…")
        success, nchunks, nrows, _ = write_pandas(
            conn,
            df,
            table_name="WEATHER_CURRENT",
            database=conn_params["database"],
            schema=conn_params["schema"],
            quote_identifiers=False
        )

        if success:
            print(f"✅ Chargement terminé : {nrows} lignes insérées en {nchunks} batch(s).")
        else:
            print("❌ Échec de l’insertion.")

if __name__ == "__main__":
    main()
