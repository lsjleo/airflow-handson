from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def produce_data(ti):
    data = {"key": "value", "number": 42}
    ti.xcom_push(key="shared_data", value=data)

with DAG(
    "producer_dag",
    default_args={"retries": 1},
    description="DAG que produz dados",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    produce_data_task = PythonOperator(
        task_id="produce_data",
        python_callable=produce_data,
    )
