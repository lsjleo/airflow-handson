import logging
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
args = {"owner": "airflow", "start_date": airflow.utils.dates.days_ago(1)}
dag = DAG(
 dag_id="ExternalTaskSensorProducer", default_args=args, schedule_interval='45 06 * * *'
)
def pp():
 print('First Primary Task')
 
with dag:
 first_task=PythonOperator(task_id="first_task", python_callable=pp,dag=dag)
first_task