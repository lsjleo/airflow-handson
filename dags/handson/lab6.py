from airflow.models.dag import DAG
from airflow.datasets import Dataset, DatasetAlias
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.datasets.metadata import Metadata
from airflow.models import Variable
from datetime import datetime
import pandas as pd


lines = 1000
datasets_dags = Variable.get(
    "datasets", deserialize_json=True, default_var=None
)

def create_dynamic_dags(dag_id, dataset, alias):
    dag = DAG(
        dag_id=dag_id,
        schedule_interval='@once',
        start_date=datetime(2024,12,3),
        tags=['lab6', 'handson'],
        catchup=False
    )


    def funcao(**context):
        
        yield Metadata(
            Dataset(dataset),
            extra={'k':'v'}, 
            alias=alias,
        )
        

    task1 = PythonOperator(
        task_id='TASK1_PY',
        python_callable=funcao,
        outlets=[DatasetAlias(alias)],
        dag=dag
    )

    task2 = DummyOperator(
        task_id='TASK2_DUMMY',
        dag=dag
    )

    task1 >> task2
    
    return dag

for i in datasets_dags:
    globals()[i['dag_id']] = create_dynamic_dags(i['dag_id'], i['dataset'],i['alias'])