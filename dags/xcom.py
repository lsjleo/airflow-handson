from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago

# Função para a primeira task (produzir valor)
def push_xcom(**kwargs):
    data_to_push = "Este é o valor enviado via XCom!"
    # Salvar o valor no XCom
    kwargs['ti'].xcom_push(key='meu_dado', value=data_to_push)

# Função para a segunda task (consumir valor)
def pull_xcom(**kwargs):
    # Recuperar o valor do XCom
    valor_recebido = kwargs['ti'].xcom_pull(task_ids='push_task', key='meu_dado')
    print(f"Valor recebido via XCom: {valor_recebido}")

# Definição da DAG
with DAG(
    dag_id='exemplo_xcom',
    default_args={'start_date': days_ago(1)},
    schedule_interval=None,  # Execução manual
    catchup=False,
) as dag:

    # Task 1: Produzindo dados e enviando via XCom
    push_task = PythonOperator(
        task_id='push_task',
        python_callable=push_xcom,
        provide_context=True,
    )

    # Task 2: Consumindo os dados enviados via XCom
    pull_task = PythonOperator(
        task_id='pull_task',
        python_callable=pull_xcom,
        provide_context=True,
    )

    # Definir a sequência das tasks
    push_task >> pull_task
