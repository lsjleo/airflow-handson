from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

# Definição da DAG
default_args = {
    'start_date': datetime(2024, 11, 19),
}

with DAG(
    dag_id='example_taskgroup',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    # Tarefa inicial
    start = DummyOperator(task_id='start')

    # TaskGroup para agrupar tarefas relacionadas
    with TaskGroup("data_processing", tooltip="Tasks for data processing") as data_processing_group:
        task_1 = DummyOperator(task_id='extract_data')
        task_2 = DummyOperator(task_id='transform_data')
        task_3 = DummyOperator(task_id='load_data')

        # Definindo dependências dentro do TaskGroup
        task_1 >> task_2 >> task_3

    # Tarefa final
    end = DummyOperator(task_id='end')

    # Definindo dependências globais
    start >> data_processing_group >> end
