from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from pipelines.redditpipeline import redditpipeline
from pipelines.awss3pipeline import upload_s3_pipeline

default_args = {
    'owner': 'Rhea Santhmayor',
    'start_date': datetime(2025, 6, 21)
}

dag = DAG(
    dag_id='etl_reddit_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['reddit', 'etl', 'pipeline']
)

extract = PythonOperator(
    task_id='reddit_extraction',
    python_callable=redditpipeline,
    op_kwargs={
        "file_name": 'reddit_{{ ds_nodash }}',  # dynamic file name based on DAG run date
        'subreddit': 'news',
        'time_filter': 'day',
        'limit': 100
    },
    dag=dag
)

upload_s3 = PythonOperator(
    task_id='s3_upload',
    python_callable=upload_s3_pipeline,
    dag=dag
)

extract >> upload_s3  # Set dependency so upload waits for extraction