import logging
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

args = {"owner": "airflow", "start_date": airflow.utils.dates.days_ago(1)}
dag = DAG(
    dag_id="ExternalTaskSensorProducer", 
    default_args=args, 
    schedule_interval='45 06 * * *',
    tags=['lab2', 'handson_']
)
def pp(ti):
    print('First Primary Task')
    ti.xcom_push(key='test',value='abc')
 
with dag:
    first_task=PythonOperator(task_id="first_task", python_callable=pp,dag=dag)
first_task