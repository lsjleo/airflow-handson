from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from time import sleep
from random import randint

def tarefa1(x,t):
    sleep(t)
    print('VALOR RECEBIDO', x)

# Definir os argumentos padrão para a DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

listaTasks = []

# Criar a DAG
with DAG(
    dag_id='handson_lab1',
    default_args=default_args,
    description='LAB 1 HANDS ON',
    schedule_interval='30 8 * * *',#timedelta(days=1),  # Execução diária
    start_date=datetime(2024,11,10),#days_ago(1),  # Data inicial (ajuste conforme necessário)
    catchup=True,  # Evitar execução retroativa
    tags=['exemplo', 'lab1', 'handson'],
) as dag:
    t1 = DummyOperator(task_id="start")
    for i in range(0,18):
        listaTasks.append(PythonOperator(task_id=f'python_op{i}',python_callable=tarefa1,op_kwargs={'x': 'value1','t':randint(1,10)}))
    
    t3 = DummyOperator(task_id="stop")
    
    t1 >> listaTasks >> t3