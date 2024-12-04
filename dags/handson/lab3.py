from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.models import DagRun
from airflow.datasets import Dataset
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import logging
lines = 10000

def funcao_datetime(dt):
    dag_runs = DagRun.find(dag_id='handson_lab2')
    dag_runs.sort(key=lambda x: x.execution_date, reverse=True)
    if dag_runs:
        ultima_dag_run = dag_runs[0].execution_date
        if ultima_dag_run >= dt:
            return ultima_dag_run
        else:
            return dt + timedelta(hours=3)


def run_code(**context):
    print(context)
    logging.error(context['execution_date'] - timedelta(hours=3))
    param1 = Variable.get('PARAM1',deserialize_json=True)
    logging.warning(param1['param2'])
    data = {
        'col1':[x for x in range(0,lines)],
        'col2':[x for x in range(0,lines)],
        'col3':[f'{str(x)*200}' for x in range(0,lines)],
    }
    df = pd.DataFrame(data)
    context['ti'].xcom_push(key='xcom',value=df.to_dict(orient='list'))
    
def consume(**context):
    df = pd.DataFrame(context['ti'].xcom_pull(key='xcom',task_ids='TASK2_PY'))
    df['col4'] = [x for x in range(0,lines)]
    try:
        context['ti'].xcom_push(key='xcom2',value=df.to_dict(orient='list'))
    except Exception as e:
        pass

def funcao_branch(**context):
    resultado_execucao = context['ti'].xcom_pull(task_ids='TASK3_PY', key='xcom2')
    if not resultado_execucao:
        return 'TASK4_DUMMY'
    else:
        return 'TASK5B_PY'
    
def tratamento_erro(**context):
    df = pd.DataFrame(context['ti'].xcom_pull(key='xcom2',task_ids='TASK3_PY')) 
    
    

dag = DAG(
    dag_id='handson_lab3',
    schedule_interval='30 8 * * *',
    start_date=datetime(2024,11,26), # pode ser utilizado days_ago(1) ou datetime(2024,11,28)
    tags=['lab3', 'handson'],
    catchup=False
)

tg = TaskGroup('GRUPO', dag=dag)

task1 = DummyOperator(
    task_id='TASK1_DUMMY',
    dag=dag   
)

task2 = PythonOperator(
    task_id='TASK2_PY',
    dag=dag,
    python_callable=run_code
)

task3 = PythonOperator(
    task_id='TASK3_PY',
    dag=dag,
    python_callable=consume,
    task_group=tg
)

sensor1 = ExternalTaskSensor(
    task_id='SENSOR1',
    external_dag_id='handson_lab2',
    external_task_id='TASK6_PY',
    # execution_delta = timedelta(hours=3,minutes=3),
    execution_date_fn=funcao_datetime,
    timeout=180,
    mode='reschedule',
    poke_interval=2,
    task_group=tg  
)

task4 = DummyOperator(
    task_id='TASK4_DUMMY',
    dag=dag,
    task_group=tg   
)

branch1 = BranchPythonOperator(
    task_id='BRANCH1',
    python_callable=funcao_branch,
    provide_context=True,
    task_group=tg
)

task5 = PythonOperator(
    task_id='TASK5B_PY',
    dag=dag,
    python_callable=tratamento_erro,
    outlets=[
        Dataset('METADADOS_HANDSON_LAB3')
    ],
    task_group=tg
)

task1 >> task2 >> [sensor1,task3] 
task3 >> branch1
branch1 >> task4
branch1 >> task5