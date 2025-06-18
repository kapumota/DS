import sys
sys.path.append("/opt/airflow/app")  # <- añade el módulo pipeline.py

from airflow.decorators import dag, task
from datetime import datetime, timedelta
import pandas as pd
from pipeline import extract as _extract, transform as _transform, load as _load

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    dag_id="etl_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 6, 18),
    schedule_interval="@daily",
    catchup=False,
)
def etl_pipeline():
    @task()
    def extract():
        return _extract().to_dict(orient="records")

    @task()
    def transform(rows):
        df = pd.DataFrame(rows)
        return _transform(df).to_dict(orient="records")

    @task()
    def load(rows):
        df = pd.DataFrame(rows)
        _load(df)

    load(transform(extract()))

etl_pipeline()
