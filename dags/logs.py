from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import logging
from airflow.utils.dates import days_ago

# Função para tarefa que usa logs
def my_task_function(**kwargs):
    logging.info("Iniciando a tarefa...")
    logging.debug("Este é um log de depuração detalhado.")
    logging.warning("Este é um aviso que algo pode estar errado.")
    logging.error("Este é um log de erro (exemplo, mas sem erro real).")
    logging.info("Tarefa executada com sucesso!")
    return "Sucesso!"

# Função para exibir informações de execução
def log_execution_details(**kwargs):
    logging.info(f"Contexto completo: {kwargs}")
    execution_date = kwargs.get('execution_date')
    logging.info(f"Data de execução da tarefa: {execution_date}")

# Configuração da DAG
default_args = {
    'owner': 'usuario',
    'depends_on_past': False,
    'email': ['seu-email@exemplo.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dag_com_logs',
    default_args=default_args,
    description='Exemplo de DAG com Logs',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
    tags=['exemplo', 'logs'],
) as dag:

    # Tarefa principal
    task_with_logs = PythonOperator(
        task_id='task_with_logs',
        python_callable=my_task_function,
        provide_context=True,
    )

    # Tarefa para logar detalhes da execução
    log_execution_task = PythonOperator(
        task_id='log_execution_details',
        python_callable=log_execution_details,
        provide_context=True,
    )

    # Dependência entre as tarefas
    task_with_logs >> log_execution_task
