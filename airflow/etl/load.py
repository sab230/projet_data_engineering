import os
import pandas as pd
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import psycopg2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

INPUT_PATH = "data/processed/weather_multi_clean.csv"

SNOWFLAKE_PARAMS = {
    "account":   os.getenv("SNOWFLAKE_ACCOUNT"),
    "user":      os.getenv("SNOWFLAKE_USER"),
    "password":  os.getenv("SNOWFLAKE_PASSWORD"),
    "role":      os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "WH_DE"),
    "database":  os.getenv("SNOWFLAKE_DATABASE", "WEATHER_DB"),
    "schema":    os.getenv("SNOWFLAKE_SCHEMA", "RAW"),
}

def main():

    print("📥 Lecture du fichier transformé…")
    df = pd.read_csv(INPUT_PATH)

    df.columns = [c.strip().upper() for c in df.columns]
    df["DATE"] = pd.to_datetime(df["DATE"]).dt.date
    df["DATETIME"] = pd.to_datetime(df["DATETIME"])

    # ========= SNOWFLAKE LOAD ==========
    print("🔌 Connexion Snowflake…")
    with connect(**SNOWFLAKE_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(f"USE DATABASE {SNOWFLAKE_PARAMS['database']}")
            cur.execute(f"USE SCHEMA {SNOWFLAKE_PARAMS['schema']}")

        write_pandas(
            conn,
            df,
            table_name="WEATHER_CURRENT",
            database=SNOWFLAKE_PARAMS["database"],
            schema=SNOWFLAKE_PARAMS["schema"]
        )

    print("☁️ Snowflake OK.")

    # ========= POSTGRESQL LOAD ==========
    print("🐘 Connexion PostgreSQL…")
    pg_conn = psycopg2.connect(
        host="localhost",   # <<< ➜ METS ICI TON IP DOCKER !!!
        dbname="postgres",
        user="postgres",
        password="admin",
        port=5432
    )

    cursor = pg_conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_metrics (
            date DATE,
            city VARCHAR(50),
            temperature FLOAT,
            temperature_f FLOAT,
            humidity FLOAT,
            pressure FLOAT,
            weather VARCHAR(100),
            wind_speed FLOAT,
            datetime TIMESTAMP
        )
    """)

    print("📤 Insertion dans PostgreSQL…")
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO weather_metrics VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, tuple(row))

    pg_conn.commit()
    cursor.close()
    pg_conn.close()

    print("🎉 Données insérées dans PostgreSQL !")

if __name__ == "__main__":
    main()
