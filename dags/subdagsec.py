from airflow.models.dag import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

def create_subdag(parent_dag_name, child_dag_name, args):
    with DAG(
        dag_id=f"{parent_dag_name}.{child_dag_name}",
        default_args=args,
        schedule_interval="@daily",
        start_date=datetime(2024, 1, 1),
    ) as dag:
        start = DummyOperator(task_id="start")
        process = PythonOperator(
            task_id="process_task",
            python_callable=lambda: print("Processing inside SubDAG")
        )
        end = DummyOperator(task_id="end")
        
        start >> process >> end
    
    return dag
