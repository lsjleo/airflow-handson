from airflow.decorators import dag, task
from airflow.datasets import Dataset, DatasetAlias
from airflow.datasets.metadata import Metadata

alias = "DatasetName"


@dag(
    start_date=None,
    schedule=None,
    catchup=False,
    tags=['lab3', 'handson_']
)
def dataset_producer_dag():

    @task(outlets=[Dataset("/tmp/teste.json")])
    def dataset_producer_task():
        pass
    
    @task(outlets=[DatasetAlias(alias)])
    def attach_event_to_alias_metadata():
        yield Metadata(
            Dataset(f"/tmp/teste.json"),
            extra={"k": "v"},  # extra has to be provided, can be {}
            alias=alias,
        )

    dataset_producer_task() >> attach_event_to_alias_metadata()


dataset_producer_dag()


# from airflow.models.dag import DAG
# from airflow.datasets import Dataset
# from airflow.operators.python import PythonOperator

# with DAG(
#     dag_id="my_producer_dag",
#     start_date=None,
#     schedule=None,
#     catchup=False,
# ):

#     def my_function():
#         pass

#     my_task = PythonOperator(
#         task_id="my_producer_task",
#         python_callable=my_function,
#         outlets=[Dataset("/tmp/")]
#     )