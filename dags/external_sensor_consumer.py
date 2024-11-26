import logging
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime, timedelta
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
args = {"owner": "airflow", "start_date": airflow.utils.dates.days_ago(1)}
dag = DAG(
 dag_id="ExternalTaskSensorConsumer", default_args=args, schedule_interval='55 06 * * *'
)
def pp():
 logging.getLogger('Second Dependent Task')
 
with dag:
    Sensor = ExternalTaskSensor(
        task_id='Ext_Sensor_Task',
        external_dag_id='ExternalTaskSensorProducer',
        external_task_id='first_task',
        execution_delta = timedelta(minutes=1),
        timeout=120,
        mode="reschedule",
        dag=dag
    )
    
    Second_Task=PythonOperator(task_id="Second_Task", python_callable=pp,dag=dag)
    
    Sensor>>Second_Task