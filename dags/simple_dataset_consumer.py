from airflow.decorators import dag, task
from airflow.datasets import DatasetAlias
from airflow.operators.empty import EmptyOperator
from pendulum import datetime

alias = "DatasetName"
dataset = DatasetAlias(alias)

@dag(
    start_date=datetime(2024, 8, 1),
    schedule=[dataset],
    catchup=False,
    tags=['lab3', 'handson_']
)
def dataset_consumer_dag():

    @task(inlets=[dataset])
    def view_dataset(**context):
        # ds = DatasetAlias(my_alias_name)
        # ds = context#['outlet_events']
        print(context["inlet_events"][dataset])
        for i in context["inlet_events"][dataset]:
            print(i)
    
    EmptyOperator(task_id="empty_task") >> view_dataset()
    

dataset_consumer_dag()


# from airflow.models.dag import DAG
# from airflow.datasets import Dataset
# from airflow.operators.empty import EmptyOperator
# from pendulum import datetime 

# with DAG(
#     dag_id="my_consumer_dag",
#     start_date=datetime(2024, 8, 1),
#     schedule=[Dataset("/tmp/")],
#     catchup=False,
# ):

#     EmptyOperator(task_id="empty_task")
