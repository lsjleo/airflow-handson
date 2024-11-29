from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
from airflow.models import Variable
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import logging
lines = 10000
def run_code(**context):
    print(context)
    logging.error(context['execution_date'] - timedelta(hours=3))
    param1 = Variable.get('PARAM1',deserialize_json=True)
    logging.warning(param1['param2'])
    data = {
        'col1':[x for x in range(0,lines)],
        'col2':[x for x in range(0,lines)],
        'col3':[f'{str(x)*200}' for x in range(0,lines)],
    }
    # df = pd.DataFrame(data)
    
    hook = PostgresHook(postgres_conn_id='afl', schema='airflow')
    con = hook.get_conn()
    df = pd.read_sql("""
    SELECT dr.id, x.run_id FROM dag_run dr 
    INNER JOIN xcom x ON dr.id = x.dag_run_id 
    WHERE dr.dag_id = 'LAB1_SIMPLES'                 
    """, con)
    
    context['ti'].xcom_push(key='xcom',value=df.to_dict(orient='list'))
    
    logging.error(hook)
    
def consume(**context):
    df = pd.DataFrame(context['ti'].xcom_pull(key='xcom',task_ids='TASK4_PY'))
    # df['col4'] = [x for x in range(0,lines)]
    print(df)
    hook = PostgresHook(postgres_conn_id='lab', schema='lab')
    con = hook.get_connection('lab')
    engine = create_engine(
        f"postgresql+psycopg2://{con.login}:{con.password}@{con.host}/{con.schema}"
    )
    df.to_sql(
        name='tb_dag_run1',
        schema='lab1',
        if_exists='append',
        con=engine
    )
    

dag = DAG(
    dag_id='LAB1_SIMPLES',
    # default_args={
    #     'depends_on_past':True
    # },
    schedule_interval='30 8 * * *',
    start_date=datetime(2024,11,26), # pode ser utilizado days_ago(1) ou datetime(2024,11,28)
    tags=['simples'],
    catchup=True
)

tg = TaskGroup('GRUPO', dag=dag)

task1 = DummyOperator(
    task_id='TASK1_DUMMY',
    dag=dag   
)

task2 = DummyOperator(
    task_id='TASK2_DUMMY',
    task_group=tg,
    dag=dag   
)

task3 = DummyOperator(
    task_id='TASK3_DUMMY',
    task_group=tg,
    dag=dag   
)

task4 = PythonOperator(
    task_id='TASK4_PY',
    dag=dag,
    python_callable=run_code
)

task5 = DummyOperator(
    task_id='TASK5_DUMMY',
    task_group=tg,
    dag=dag   
)

task6 = PythonOperator(
    task_id='TASK6_PY',
    dag=dag,
    python_callable=consume
)

task7 = PostgresOperator(
    task_id='TASK7_PG',
    postgres_conn_id='lab',
    sql="""
    TRUNCATE TABLE lab1.tb_dag_run1;
    """
)

sensor1 = FileSensor(
    task_id='SENSOR1',
    filepath='/opt/airflow/plugins/example.txt',
    fs_conn_id='teste_file',
    mode='reschedule', # Pode ser 'poke' ou 'reschedule' (melhor para recursos)
    poke_interval=10
)

task8 = DummyOperator(
    task_id='TASK8_DUMMY',
    dag=dag   
)

task1 >> [task2,task3] >> task5 >> task4 >> task7 >> task6  >> sensor1 >> task8