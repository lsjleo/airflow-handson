import logging
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime, timedelta
from airflow.models import DagRun

def get_most_recent_dag_run(dt):
    dag_runs = DagRun.find(dag_id="ExternalTaskSensorProducer")
    dag_runs.sort(key=lambda x: x.execution_date, reverse=True)
    print('DECORATOR',(dt - timedelta(hours=3)).astimezone())
    if dag_runs:
        last_dag_run = (dag_runs[0].execution_date - timedelta(hours=3)).astimezone()
        print('DAG',last_dag_run)
        print(last_dag_run >= (dt - timedelta(hours=3)).astimezone())
        if last_dag_run >= (dt - timedelta(hours=3)).astimezone():
            print('DAGRUN Encontrado')
            return dag_runs[0].execution_date
        else:
            print('DAGRUN Não Encontrado')
            return (datetime.now() + timedelta(hours=20)).astimezone()
    else:
        print('DAGRUN Não Encontrado2')
        return (datetime.now() + timedelta(hours=20)).astimezone()
    
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
args = {"owner": "airflow", "start_date": airflow.utils.dates.days_ago(1)}
dag = DAG(
    dag_id="ExternalTaskSensorConsumer", 
    default_args=args, 
    schedule_interval='55 06 * * *',
    tags=['lab2', 'handson']
)
def pp(ti):
    print('Deu certo!',ti.xcom_pull(dag_id='ExternalTaskSensorProducer',task_ids='first_task',key='test'))
    logging.getLogger('Second Dependent Task')
    
 
with dag:
    Sensor = ExternalTaskSensor(    
        task_id='Ext_Sensor_Task',
        external_dag_id='ExternalTaskSensorProducer',
        external_task_id='first_task',
        # execution_delta = timedelta(hours=500000),
        execution_date_fn=get_most_recent_dag_run,
        timeout=120,
        mode="poke", # reschedule ou poke
        dag=dag
    )
    
    Second_Task=PythonOperator(task_id="Second_Task", python_callable=pp,dag=dag)
    
    Sensor>>Second_Task