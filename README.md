🌦️ MétéoFlow — Pipeline de données complet (Airflow, Snowflake, dbt, Grafana)

MétéoFlow est un projet complet de Data Engineering permettant de :

Extraire des données météo depuis l’API OpenWeather

Transformer et nettoyer les données

Charger les données dans Snowflake

Automatiser le pipeline complet avec Airflow

Modéliser les données avec dbt

Visualiser les métriques météo dans Grafana

Surveiller l’exécution du pipeline

Ce projet présente une architecture moderne, réaliste, et conçue pour un usage professionnel.

📁 Architecture du projet
projet_data_engineering/
│
├── airflow/
│   ├── dags/
│   │   └── weather_etl_dag.py
│   ├── etl/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py
│   ├── logs/
│   └── docker-compose.yml
│
├── data/
│   ├── raw/
│   └── processed/
│       └── weather_multi_clean.csv
│
├── meteo_flow/   (projet dbt)
│
└── README.md

🚀 Fonctionnalités
🔹 1. Extraction

Récupération de données météo via l’API OpenWeather (format JSON)

Multi-villes possible

Enregistrement dans /data/raw/

🔹 2. Transformation

Nettoyage des données (types, formats, colonnes)

Normalisation des unités (°C → °F)

Enregistrement dans /data/processed/

🔹 3. Chargement Snowflake

Création automatique de la table WEATHER_CURRENT

Insertion massive via write_pandas

Gestion des schémas (RAW, STAGING, ANALYTICS)

🔹 4. Automatisation avec Airflow

Pipeline ETL complet dans un DAG :

extract >> transform >> load


Exécution quotidienne (@daily), logs consultables via l’interface web Airflow.

🔹 5. Modélisation dbt

Source : RAW.WEATHER_CURRENT

Modèle staging : STG_WEATHER_CURRENT

Agrégations métriques dans ANALYTICS.WEATHER_METRICS

Documentation automatique dbt

🔹 6. Visualisation Grafana / PostgreSQL

Les métriques agrégées sont exportées vers PostgreSQL

Grafana se connecte à PostgreSQL pour afficher :

Températures moyennes par ville

Variation d’humidité

Évolution du vent

État du ciel (Sunny, Rain, Cloudy…)

🐳 Lancer tout le projet avec Docker Compose

Depuis le dossier /airflow :

docker compose up --build


Ce qui démarre automatiquement :

✔ Airflow Scheduler
✔ Airflow Webserver
✔ Airflow Postgres
✔ Grafana PostgreSQL
✔ Grafana UI
