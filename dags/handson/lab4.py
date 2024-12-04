from airflow.models.dag import DAG
from airflow.datasets import Dataset, DatasetAlias
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.datasets.metadata import Metadata
from datetime import datetime
import pandas as pd

alias = 'HANDSON_LAB4_DATASET_ALIAS'
lines = 1000

dag = DAG(
    dag_id='handson_lab4',
    schedule_interval='@once',
    start_date=datetime(2024,12,3),
    tags=['lab4', 'handson'],
    catchup=False
)


def funcao(**context):
    data = {
        'col1':[x for x in range(0,lines)],
        'col2':[x for x in range(0,lines)],
        'col3':[f'{str(x)*200}' for x in range(0,lines)],
    }
    df = pd.DataFrame(data)
    yield Metadata(
        Dataset(f"HANDSON_LAB4_DATASET"),
        extra={'data':repr(df.to_dict(orient='list'))}, 
        alias=alias,
    )
    

task1 = PythonOperator(
    task_id='TASK1_PY',
    python_callable=funcao,
    outlets=[DatasetAlias('HANDSON_LAB4_DATASET_ALIAS')],
    dag=dag
)

task2 = DummyOperator(
    task_id='TASK2_DUMMY',
    dag=dag
)

task1