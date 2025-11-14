# 🌦️ MétéoFlow

[![Status Build](https://img.shields.io/badge/Pipeline-Stable-brightgreen)](http://localhost:8080)
[![Technologies](https://img.shields.io/badge/Stack-Airflow%20%7C%20Snowflake%20%7C%20dbt-blue)]()
[![Licence](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)

**MétéoFlow** est un pipeline complet de *Data Engineering* conçu pour collecter, transformer, stocker et visualiser des données météorologiques **en temps réel**. Il s’appuie sur une architecture moderne utilisant **Airflow** pour l'orchestration et **Snowflake** comme Data Warehouse.

---

## 🧭 Table des Matières

* [🎯 Objectifs du Projet](#-objectifs-du-projet)
* [🏗️ Architecture Globale](#️-architecture-globale)
* [🚀 Pour Commencer](#-pour-commencer)
* [⚙️ Installation (Docker)](#️-installation-docker)
* [▶️ Démarrage](#️-démarrage)
* [🛠️ Fabriqué avec](#️-fabriqué-avec)
* [✒️ Auteurs & Contact](#️-auteurs--contact)
* [⚖️ Licence](#️-licence)

---

## 🎯 Objectifs du Projet

Le pipeline a été conçu pour :

* Collecter automatiquement des données météo depuis l'***API OpenWeather***.
* Orchestrer l'ensemble du workflow **ETL** avec **Airflow**.
* Stocker les données historisées dans **Snowflake**.
* Modéliser les données analytiques avec **dbt**.
* Exposer les métriques en *temps réel* dans un dashboard **Grafana**.

---

## 🏗️ Architecture Globale

Le flux de données est géré par un DAG Airflow qui pilote les transformations Python et dbt :

> OpenWeather API → **Airflow** → ETL Python → **Snowflake** (RAW → STAGING → ANALYTICS) → **PostgreSQL** → **Grafana**

### Schéma Logique

| Composant | Rôle |
| :--- | :--- |
| **Airflow** | **Orchestration** des tâches (Extract, Transform, Load, Model). |
| **Snowflake** | **Data Warehouse** Cloud central. |
| **dbt** | Modélisation des données SQL et création des tables BI. |
| **Grafana** | Visualisation et Dashboards métier. |

---

## 🚀 Pour Commencer

Ce projet nécessite **Docker** et **Docker Compose** pour initialiser l'infrastructure complète. Vous aurez également besoin de vos credentials de services cloud.

### Pré-requis

* **Docker** et **Docker Compose** (vérifiez l'installation avec `docker --version`).
* Une clé d'API valide pour **OpenWeatherMap**.
* Des identifiants de connexion **Snowflake** (compte, utilisateur, mot de passe).

### Gestion des Credentials (IMPORTANT)

Vous devez créer un fichier nommé **`.env`** dans le dossier `/airflow` pour y placer les secrets. Ce fichier est ignoré par Git.

```bash
# Exemple de contenu pour .env
OPENWEATHER_API_KEY=votre_cle_api_secrete_ici

SNOWFLAKE_ACCOUNT=votre_compte
SNOWFLAKE_USER=votre_user
SNOWFLAKE_PASSWORD=votre_mot_de_passe
# ... autres variables DB et POSTGRES
