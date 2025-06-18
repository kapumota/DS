"""
ETL simple: lee input.csv, calcula value_squared y lo vuelca a Postgres.
Se ejecuta tanto en el contenedor "etl-app" como desde Airflow.
"""
import os
import json
import pandas as pd
import psycopg2
from contextlib import closing

DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "etl_db")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "pass")
CSV_PATH = os.getenv("CSV_PATH", "/app/data/input.csv")

def extract() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH)

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df["value_squared"] = df["value"] ** 2
    return df

def load(df: pd.DataFrame) -> None:
    with closing(
        psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASS
        )
    ) as conn, conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_data (
                id SERIAL PRIMARY KEY,
                name TEXT,
                value INTEGER,
                value_squared INTEGER
            );
            """
        )
        cur.executemany(
            """
            INSERT INTO processed_data (name, value, value_squared)
            VALUES (%(name)s, %(value)s, %(value_squared)s)
            """,
            df.to_dict(orient="records"),
        )

# Permite invocar desde CLI o importarlo en Airflow
def run_etl():
    df = transform(extract())
    load(df)

if __name__ == "__main__":
    run_etl()
