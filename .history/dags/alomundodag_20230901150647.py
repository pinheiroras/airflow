from __future__ import annotations
from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator

with DAG(
  "trabalho_pipeline",
  default_args={
    "depends_on_past": False,
    "email": ["pinheiro.ras@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
  },
  description="Primeira DAG do curso",
  schedule=timedelta(days=1),
  start_date=datetime(2023, 9, 1),
  catchup=False,
  tags=["exemplo"],
) as dag:
    t1 = BashOperator(
      task_id="alomundotask",
      bash_command="echo 'Alo mundo do airflow'",
    )
    
    t2 = BashOperator(
      task_id = "print_date",
      bash_command = "date",
    )

    t3 = BashOperator(
      task_id = "sleep",
      depends_on_past=False,
      bash_command = "sleep 5",
      retries = 3,
    )

    t4 = BashOperator(
      task_id = "new_print_date",
      bash_command = "date",
    )
    
    t5 = BashOperator(
      task_id = "finish_him",
      bash_command = "echo 'terminou'",
    )
    
    def _calculador():
      print("Calculando a nota do trabalho...")
      
    run_script_calc = PythonOperator(
      task_id = "run_script_calc",
      python_callable = _calculador,
      provide_context = True,
    )
    
    vazio = EmptyOperator(task_id="other_task", dag=dag)
    
    t1 >> t2 >> [t3, other_task] >> t4 << vazio >> [t5, run_script_calc]