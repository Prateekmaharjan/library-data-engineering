from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Add your library_dw project path so Airflow can find your ETL functions
sys.path.insert(0, '/mnt/d/library_management_db - ETL/03-data-warehouse')

# Import your ETL functions
from etl_to_warehouse import (
    extract_and_load_dim_member,
    extract_and_load_dim_book,
    load_dim_date,
    extract_and_load_fact_borrow
)

# Default arguments for the DAG
default_args = {
    'owner': 'pratik',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Define the DAG
with DAG(
    dag_id='library_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for library data warehouse',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    # Task 1
    task_dim_member = PythonOperator(
        task_id='load_dim_member',
        python_callable=extract_and_load_dim_member
    )

    # Task 2
    task_dim_book = PythonOperator(
        task_id='load_dim_book',
        python_callable=extract_and_load_dim_book
    )

    # Task 3
    task_dim_date = PythonOperator(
        task_id='load_dim_date',
        python_callable=load_dim_date
    )

    # Task 4
    task_fact_borrow = PythonOperator(
        task_id='load_fact_borrow',
        python_callable=extract_and_load_fact_borrow
    )

    # Define order — dimensions first then fact
    [task_dim_member, task_dim_book, task_dim_date] >> task_fact_borrow