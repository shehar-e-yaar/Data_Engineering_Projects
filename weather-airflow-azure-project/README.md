# Weather Data Pipeline using Apache Airflow & Azure Blob

## Overview
This project builds an ETL pipeline using Apache Airflow to:
1. Fetch weather data from OpenWeather API
2. Transform the data
3. Store it as CSV
4. Upload it to Azure Blob Storage

## Technologies
- Apache Airflow
- Python
- Azure Blob Storage
- OpenWeather API

## Airflow Connections Required
### 1. weather_api
- Type: HTTP
- Host: https://api.openweathermap.org/

### 2. azure_blob
- Type: Azure Blob Storage
- Extra:
```json
{
  "account_name": "<your_storage_account>",
  "account_key": "<your_key>"
}

