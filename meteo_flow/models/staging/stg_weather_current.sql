-- models/staging/stg_weather_current.sql

SELECT
    DATE,
    CITY,
    TEMPERATURE,
    TEMPERATURE_F,
    HUMIDITY,
    PRESSURE,
    WEATHER,
    WIND_SPEED,
    DATETIME,
    (TEMPERATURE - 32) * 5/9 AS TEMPERATURE_C
FROM {{ source('raw', 'WEATHER_CURRENT') }}
