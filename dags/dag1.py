from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Funções para as tarefas
def tarefa1():
    print("Executando a Tarefa 1!")

def tarefa2():
    print("Executando a Tarefa 2!")

def tarefa3():
    print("Executando a Tarefa 3!")

# Definir os argumentos padrão para a DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Criar a DAG
with DAG(
    'dag_simples_teste',
    default_args=default_args,
    description='Uma DAG simples para testes',
    schedule_interval=timedelta(days=1),  # Execução diária
    start_date=datetime(2024, 1, 1),  # Data inicial (ajuste conforme necessário)
    catchup=False,  # Evitar execução retroativa
    tags=['exemplo', 'teste'],
) as dag:

    # Definir as tarefas usando PythonOperator
    tarefa_1 = PythonOperator(
        task_id='tarefa_1',
        python_callable=tarefa1
    )

    tarefa_2 = PythonOperator(
        task_id='tarefa_2',
        python_callable=tarefa2
    )

    tarefa_3 = PythonOperator(
        task_id='tarefa_3',
        python_callable=tarefa3
    )

    # Definir a ordem de execução das tarefas
    tarefa_1 >> tarefa_2 >> tarefa_3

