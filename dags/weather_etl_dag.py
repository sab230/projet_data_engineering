from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

# === Paramètres généraux du DAG ===
default_args = {
    'owner': 'Sabrina',
    'retries': 1,
    'start_date': datetime(2025, 11, 1)
}

dag = DAG(
    dag_id='meteo_flow_dag',
    default_args=default_args,
    schedule_interval='@daily',  # exécution chaque jour
    catchup=False,
    description='Pipeline ETL météo automatisé (OpenWeather → Snowflake)'
)

# === Fonctions pour exécuter les scripts ===
def extract():
    os.system("python etl/extrac.py")

def transform():
    os.system("python etl/transform.py")

def load():
    os.system("python etl/load.py")

# === Tâches Airflow ===
t1 = PythonOperator(
    task_id='extract_weather_data',
    python_callable=extract,
    dag=dag
)

t2 = PythonOperator(
    task_id='transform_weather_data',
    python_callable=transform,
    dag=dag
)

t3 = PythonOperator(
    task_id='load_to_snowflake',
    python_callable=load,
    dag=dag
)

# === Dépendances entre tâches ===
t1 >> t2 >> t3
