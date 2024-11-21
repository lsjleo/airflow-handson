from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.subdag import SubDagOperator
from datetime import datetime
from subdagsec import create_subdag

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    "main_dag_with_subdag",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    start = DummyOperator(task_id="start")

    subdag_task = SubDagOperator(
        task_id="my_subdag",
        subdag=create_subdag("main_dag_with_subdag", "my_subdag", default_args),
        dag=dag,
    )

    end = DummyOperator(task_id="end")

    start >> subdag_task >> end
