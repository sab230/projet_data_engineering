{{ config(materialized='table') }}

SELECT
    CITY,
    DATE,
    TEMPERATURE,
    TEMPERATURE_F,
    HUMIDITY,
    PRESSURE,
    WEATHER,
    WIND_SPEED,
    DATETIME,
    -- Exemple de métrique
    TEMPERATURE_F - 32 * 5/9 AS temp_celsius
FROM {{ ref('stg_weather_current') }}
