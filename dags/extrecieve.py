from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.dates import days_ago

def consume_data(ti):
    # Recupera os dados da DAG `producer_dag`
    data = ti.xcom_pull(
        task_ids="produce_data",
        dag_id="producer_dag",
        key="shared_data"
    )
    print(f"Dados consumidos: {data}")

with DAG(
    "consumer_dag",
    default_args={"retries": 1},
    description="DAG que consome dados de outra DAG",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    wait_for_producer = ExternalTaskSensor(
        task_id="wait_for_producer",
        external_dag_id="producer_dag",
        external_task_id="produce_data",
        mode="poke",
    )

    consume_data_task = PythonOperator(
        task_id="consume_data",
        python_callable=consume_data,
    )

    wait_for_producer >> consume_data_task
