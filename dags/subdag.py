from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator


# Função que retorna o SubDAG
def create_subdag(parent_dag_name, child_dag_name, args):
    subdag = DAG(
        f"{parent_dag_name}.{child_dag_name}",
        default_args=args,
        schedule_interval="@daily",
    )
    with subdag:
        start = DummyOperator(task_id="start")
        task_1 = PythonOperator(
            task_id="subdag_task_1",
            python_callable=lambda: print("Executando tarefa 1"),
        )
        task_2 = PythonOperator(
            task_id="subdag_task_2",
            python_callable=lambda: print("Executando tarefa 2"),
        )
        end = DummyOperator(task_id="end")

        start >> [task_1, task_2] >> end
    return subdag


# Definição do DAG principal
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2023, 1, 1),
}

with DAG(
    "example_dag_with_subdag",
    default_args=default_args,
    description="Exemplo de DAG com SubDAG",
    schedule_interval=timedelta(days=1),
) as dag:
    start = DummyOperator(task_id="start")

    subdag_task = SubDagOperator(
        task_id="subdag_task",
        subdag=create_subdag("example_dag_with_subdag", "subdag_task", default_args),
    )

    end = DummyOperator(task_id="end")

    start >> subdag_task >> end
