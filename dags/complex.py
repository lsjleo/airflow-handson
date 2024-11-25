from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.dates import days_ago

# Funções auxiliares
def extract_data(source):
    print(f"Extraindo dados da fonte: {source}")
    # Simular extração de dados
    return f"Dados extraídos de {source}"

def transform_data(source_file):
    print(f"Transformando dados: {source_file}")
    # Simular transformação
    return f"Dados transformados de {source_file}"

def load_data_to_db():
    print("Carregando dados para o banco de dados")
    # Simular carga no banco

def notify_success(context):
    print("DAG concluída com sucesso!")

def notify_failure(context):
    print("DAG falhou!")

# Configuração padrão da DAG
default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': notify_failure,
    'on_success_callback': notify_success
}

with DAG(
    dag_id='complex_etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL com extração, transformação, validação e carga',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
) as dag:

    start = DummyOperator(task_id='start')

    # Tarefa 1: Extrair dados de múltiplas fontes
    sources = ['api1', 'api2', 'file_source']
    extract_tasks = [
        PythonOperator(
            task_id=f'extract_from_{source}',
            python_callable=extract_data,
            op_args=[source],
        ) for source in sources
    ]

    # Tarefa 2: Transformar dados
    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_args=['data_file'],
    )

    # Tarefa 3: Validação com um sensor
    validation = FileSensor(
        task_id='validate_file',
        filepath='/tmp/arquivo.txt',
        poke_interval=30,
        timeout=600,
    )

    # Tarefa 4: Carga para o banco de dados
    load_data = PostgresOperator(
        task_id='load_to_db',
        postgres_conn_id='postgres_default',
        sql="INSERT INTO target_table SELECT * FROM staging_table;",
    )

    # Tarefa 5: Enviar notificações
    slack_success = SlackWebhookOperator(
        task_id='slack_notify_success',
        slack_webhook_conn_id='slack_webhook',
        message="DAG **complex_etl_pipeline** finalizada com sucesso!",
    )
    slack_failure = SlackWebhookOperator(
        task_id='slack_notify_failure',
        slack_webhook_conn_id='slack_webhook',
        message="DAG **complex_etl_pipeline** falhou. Verificar o log.",
        trigger_rule='one_failed',
    )

    end = DummyOperator(task_id='end')

    # Dependências
    start >> extract_tasks >> transform >> validation >> load_data
    load_data >> [slack_success, slack_failure] >> end
