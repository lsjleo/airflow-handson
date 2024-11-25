from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

# Callback para quando uma tarefa falhar
def task_fail_callback(context):
    task_instance = context['task_instance']
    print(f"Tarefa {task_instance.task_id} falhou.")

# Callback para quando uma tarefa for bem-sucedida
def task_success_callback(context):
    task_instance = context['task_instance']
    print(f"Tarefa {task_instance.task_id} foi bem-sucedida.")

# Função de exemplo com possível erro
def process_data():
    raise ValueError("Simulando erro no processamento.")

# Função de recuperação
def error_handler():
    print("Executando a tarefa de recuperação.")

# Função para decidir o fluxo baseado no status anterior
def decide_next_step(**kwargs):
    ti = kwargs['ti']
    previous_task_status = ti.xcom_pull(task_ids='process_data_task', key='return_value')
    if previous_task_status is None:  # Significa que falhou
        return 'error_handling_task'
    return 'success_task'

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'on_failure_callback': task_fail_callback,
    'on_success_callback': task_success_callback,
    'email_on_failure': False,
    'email_on_retry': False,
}

with DAG(
    dag_id='dag_with_error_handling',
    default_args=default_args,
    description='DAG com tratamento de erros',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    tags=['error_handling'],
) as dag:

    start = DummyOperator(task_id='start')

    process_data_task = PythonOperator(
        task_id='process_data_task',
        python_callable=process_data,
    )

    decide_task = BranchPythonOperator(
        task_id='decide_task',
        python_callable=decide_next_step,
        provide_context=True,
    )

    error_handling_task = PythonOperator(
        task_id='error_handling_task',
        python_callable=error_handler,
    )

    success_task = DummyOperator(task_id='success_task')

    end = DummyOperator(task_id='end')

    # Definindo o fluxo da DAG
    start >> process_data_task >> decide_task
    decide_task >> error_handling_task >> end
    decide_task >> success_task >> end
