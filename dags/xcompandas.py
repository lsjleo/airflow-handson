from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

# Função para criar e enviar um DataFrame via XCom
def create_dataframe(**kwargs):
    # Criar um DataFrame de exemplo
    df = pd.DataFrame({
        'nome': ['Alice', 'Bob', 'Charlie'],
        'idade': [25, 30, 35],
        'cidade': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte']
    })
    # Enviar o DataFrame como XCom (serializado para JSON)
    kwargs['ti'].xcom_push(key='dataframe', value=df.to_json(orient='split'))

# Função para consumir o DataFrame via XCom e realizar uma operação
def process_dataframe(**kwargs):
    # Recuperar o DataFrame enviado via XCom
    ti = kwargs['ti']
    df_json = ti.xcom_pull(task_ids='create_dataframe_task', key='dataframe')
    df = pd.read_json(df_json, orient='split')
    
    # Realizar alguma operação no DataFrame
    df['idade_duplicada'] = df['idade'] * 2
    print("DataFrame processado:\n", df)

# Definição da DAG
with DAG(
    dag_id='xcom_pandas_example',
    default_args={'start_date': datetime(2024, 11, 18)},
    schedule_interval=None,  # Execução manual
    catchup=False,
) as dag:

    # Task 1: Criar e enviar um DataFrame via XCom
    create_dataframe_task = PythonOperator(
        task_id='create_dataframe_task',
        python_callable=create_dataframe,
        provide_context=True,
    )

    # Task 2: Recuperar e processar o DataFrame
    process_dataframe_task = PythonOperator(
        task_id='process_dataframe_task',
        python_callable=process_dataframe,
        provide_context=True,
    )

    # Definir a sequência das tasks
    create_dataframe_task >> process_dataframe_task
