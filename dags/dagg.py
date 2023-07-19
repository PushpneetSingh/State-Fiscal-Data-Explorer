from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(dag_id="hello_world_dag",
        start_date=datetime(2023,7,7),
		schedule_interval="@daily",
        catchup=False) as dag:

		task1 = BashOperator(
				task_id='extract_data',
				bash_command="python3 '$AIRFLOW_HOME/src/Extract.py.py'")
    
		task2 = BashOperator(
				task_id='transform_and_load_data',
				bash_command="python3 '$AIRFLOW_HOME/src/TransformLoad.py'")

		task1>>task2