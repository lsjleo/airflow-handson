from airflow.models.dag import DAG
from airflow.datasets import DatasetAlias
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime
from ast import literal_eval
import pandas as pd

alias = 'HANDSON_LAB4_DATASET_ALIAS'
dataset = DatasetAlias(alias)

dag = DAG(
    dag_id='handson_lab5',
    schedule_interval='@once',
    start_date=datetime(2024,12,3),
    tags=['lab5', 'handson'],
    catchup=False
)

def consume(**context):
    dados = context["inlet_events"][dataset]
    dados = literal_eval(dados[-1].extra['data'])
    df = pd.DataFrame(dados)
    print(df)
    
    
task1 = DummyOperator(
    task_id='TASK1_DUMMY',
    dag=dag   
)

task2 = PythonOperator(
    task_id='TASK2_PY',
    python_callable=consume,
    dag=dag,
    inlets=[dataset]    
)

