from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import HttpOperator
import json
import os
from airflow.operators.python import PythonOperator
import pandas as pd

# NEW imports for Azure SDK upload
from airflow.hooks.base import BaseHook
from azure.storage.blob import BlobServiceClient


def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit


def transform_load_data(task_instance):
    data = task_instance.xcom_pull(task_ids="extract_weather_data")
    city = data["name"]
    weather_description = data["weather"][0]["description"]
    temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp"])
    feels_like_farenheit = kelvin_to_fahrenheit(data["main"]["feels_like"])
    min_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_min"])
    max_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data["dt"] + data["timezone"])
    sunrise_time = datetime.utcfromtimestamp(data["sys"]["sunrise"] + data["timezone"])
    sunset_time = datetime.utcfromtimestamp(data["sys"]["sunset"] + data["timezone"])

    transformed_data = {
        "City": city,
        "Description": weather_description,
        "Temperature (F)": temp_farenheit,
        "Feels Like (F)": feels_like_farenheit,
        "Minimun Temp (F)": min_temp_farenheit,
        "Maximum Temp (F)": max_temp_farenheit,
        "Pressure": pressure,
        "Humidty": humidity,
        "Wind Speed": wind_speed,
        "Time of Record": time_of_record,
        "Sunrise (Local Time)": sunrise_time,
        "Sunset (Local Time)": sunset_time,
    }

    transformed_data_list = [transformed_data]
    df_data = pd.DataFrame(transformed_data_list)
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = "current_weather_data_London_" + dt_string

    os.makedirs("/home/2024-cs-075/airflow", exist_ok=True)
    df_data.to_csv(f"/home/2024-cs-075/airflow/{dt_string}.csv", index=False)

    return f"/home/2024-cs-075/airflow/{dt_string}.csv"


# NEW: upload function (uses your Airflow connection: azure_blob)
def upload_to_azure_blob_func(task_instance):
    local_file_path = task_instance.xcom_pull(task_ids="transform_load_weather_data")

    # read Airflow connection "azure_blob"
    conn = BaseHook.get_connection("azure_blob")
    extras = conn.extra_dejson

    account_name = extras["account_name"]
    account_key = extras["account_key"]

    blob_service_client = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=account_key,
    )

    container_name = "weather-data"

    # same output structure you wanted
    blob_name = f"lahore/{datetime.now().strftime('%Y-%m-%d')}/weather.csv"

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=blob_name
    )

    with open(local_file_path, "rb") as f:
        blob_client.upload_blob(f, overwrite=True)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["ssshery4946849@gmail.com"],
    "email_on_failure": False,
    "start_date": datetime(2026, 1, 3),
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    "weather_dag",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:

    is_weather_api_ready = HttpSensor(
        task_id="is_weather_api_ready",
        http_conn_id="weather_api",
        endpoint="data/2.5/weather?q=Lahore&appid=36368a8212b79a8aa7652a9d9890a204",
    )

    extract_weather_data = HttpOperator(
        task_id="extract_weather_data",
        http_conn_id="weather_api",
        endpoint="data/2.5/weather?q=Lahore&appid=36368a8212b79a8aa7652a9d9890a204",
        method="GET",
        response_filter=lambda r: json.loads(r.text),
        log_response=True,
    )

    transform_load_weather_data = PythonOperator(
        task_id="transform_load_weather_data",
        python_callable=transform_load_data,
    )

    # UPDATED: keep task_id same, but use PythonOperator instead of LocalFilesystemToWasbOperator
    upload_to_azure_blob = PythonOperator(
        task_id="upload_to_azure_blob",
        python_callable=upload_to_azure_blob_func,
    )

    is_weather_api_ready >> extract_weather_data >> transform_load_weather_data >> upload_to_azure_blob
