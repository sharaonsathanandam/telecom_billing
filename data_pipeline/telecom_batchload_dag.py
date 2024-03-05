from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.dataflow_operator import DataflowCreatePythonJobOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago



default_args = {
    'owner': 'your_owner',
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'telecomm_batchload_dag',
    default_args=default_args,
    description='DAG to trigger batchload process',
)

dataflow_task = DataflowCreatePythonJobOperator(
    task_id='telecomm-batchload',
    py_file='gs://sharaon-code-bucket/batchloader_df.py',
    options={
        'project_id': 'sunny-might-415700',
        'location': 'us-central1',
        'staging_location': 'gs://sharaon-logs-bucket/staging',
        'temp_location': 'gs://sharaon-logs-bucket/temp',
        'runner': 'DataflowRunner',
        'save_main_session': True,
    },
    dag=dag,
)

dummy_task = DummyOperator(task_id='dummy_task', dag=dag)

dummy_task >> dataflow_task