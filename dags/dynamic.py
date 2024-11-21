from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Função de exemplo que será chamada dinamicamente
def process_table(table_name):
    print(f"Processando a tabela: {table_name}")

# Configurações da DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}

# Função para criar as tarefas dinamicamente
def create_dynamic_dag(dag_id, schedule, tables):
    dag = DAG(
        dag_id,
        default_args=default_args,
        schedule_interval=schedule,
        start_date=datetime(2024, 11, 1),
        catchup=False,
    )

    with dag:
        for table in tables:
            task = PythonOperator(
                task_id=f"process_table_{table}",
                python_callable=process_table,
                op_args=[table],
            )

    return dag

# Listagem de tabelas (ou dados externos)
table_list = ["clientes", "pedidos", "produtos"]

# Criando a DAG dinâmica
dag_id = "dynamic_table_processing"
schedule = "@daily"

globals()[dag_id] = create_dynamic_dag(dag_id, schedule, table_list)
