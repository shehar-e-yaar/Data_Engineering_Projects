import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine

# ✅ only new import (needed for batch reading)
import pyarrow.dataset as ds

#Connecting database using SQLAlchemy and loading environment variables using python-dotenv
load_dotenv("/opt/airflow/.env")
engine = create_engine(
    f"{os.getenv('DB_TYPE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

PARQUET_PATH = "/opt/airflow/data/yellow_tripdata_2025-02.parquet"

def process_parquet():
    
    if not os.path.exists(PARQUET_PATH):
        raise FileNotFoundError(f"Parquet file not found: {PARQUET_PATH}")
    print(f"Parquet file found: {PARQUET_PATH}")

def load_to_postgres(ti=None):
    print("Starting batch load to Postgres...")

    target_schema = "public"
    target_table = "yellow_taxi_data"

    # Read parquet as a dataset and stream it in batches
    dataset = ds.dataset(PARQUET_PATH, format="parquet")

    # Prepare cleaned column names once
    original_cols = dataset.schema.names
    cleaned_cols = [c.lower().replace(" ", "_") for c in original_cols]

    first_write = True
    total_rows = 0

    for batch in dataset.to_batches(batch_size=100_000):
        df = batch.to_pandas()

        # Same transformations you had
        df.columns = cleaned_cols
        df = df.dropna()

        if df.empty:
            continue

        if_exists_mode = "replace" if first_write else "append"

        df.to_sql(
            name=target_table,
            con=engine,
            schema=target_schema,
            if_exists=if_exists_mode,
            index=False,
            chunksize=10000,
            method="multi",
        )

        first_write = False
        total_rows += len(df)
        print(f"Wrote batch: {len(df):,} rows (total: {total_rows:,})")

    if first_write:
        print("No rows written (all data filtered out).")
    else:
        print(f"Data loaded to Postgres successfully. Total rows: {total_rows:,}")

with DAG(
    dag_id="parquet_to_postgres_etl",
    default_args=default_args,
    description="Read parquet, transform in pandas, load to Postgres",
    schedule_interval="@daily",
    catchup=False,
) as dag:

    process_task = PythonOperator(
        task_id="process_parquet_task",
        python_callable=process_parquet,
    )

    load_task = PythonOperator(
        task_id="load_to_postgres_task",
        python_callable=load_to_postgres,
    )

    process_task >> load_task