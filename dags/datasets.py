from airflow import DAG, Dataset
from airflow.decorators import task
from airflow.utils.dates import days_ago
from datetime import timedelta

# Definição do Dataset
my_dataset = Dataset("s3://my-bucket/my-dataset.csv")

# DAG 1: Produzindo o Dataset
with DAG(
    dag_id="producer_dag",
    schedule_interval="0 12 * * *",  # Executa diariamente ao meio-dia
    start_date=days_ago(1),
    catchup=False,
    tags=["dataset", "producer"]
) as dag1:
    @task
    def produce_data():
        # Simula a produção de dados e salva em um local
        print("Produzindo dados e publicando o dataset.")

    # Tarefa que publica o dataset
    produce_data().publish_to(my_dataset)

# DAG 2: Consumindo o Dataset
with DAG(
    dag_id="consumer_dag",
    schedule=[my_dataset],  # Define a execução com base no Dataset
    start_date=days_ago(1),
    catchup=False,
    tags=["dataset", "consumer"]
) as dag2:
    @task
    def consume_data():
        # Simula o consumo de dados do Dataset
        print("Consumindo os dados do Dataset.")

    consume_data()
