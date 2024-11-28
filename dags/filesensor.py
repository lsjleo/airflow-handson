from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago

# Função que será executada após o sensor detectar o arquivo
def process_file(**kwargs):
    print("Arquivo detectado! Processando...", kwargs)

# Definição do DAG
with DAG(
    'example_file_sensor',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
    },
    description='Exemplo de FileSensor',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['lab4', 'handson_']
) as dag:

    # Sensor para esperar o arquivo
    wait_for_file = FileSensor(
        task_id='wait_for_file',
        filepath='/tmp/arquivo.txt',  # Substituir pelo caminho real
        fs_conn_id='fs_default',  # Conexão do sistema de arquivos configurada no Airflow
        poke_interval=30,  # Intervalo (em segundos) entre tentativas de verificar o arquivo
        timeout=600,  # Tempo máximo (em segundos) para esperar o arquivo
        mode='poke',  # Pode ser 'poke' ou 'reschedule' (melhor para recursos)
    )

    # Operador Python para processar o arquivo
    process_task = PythonOperator(
        task_id='process_file',
        python_callable=process_file,
    )

    # Definindo a sequência de tarefas
    wait_for_file >> process_task
