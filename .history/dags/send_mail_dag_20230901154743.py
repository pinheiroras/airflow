from __future__ import annotations

import json

import pendulum

from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.email_operator import EmailOperator

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["unifametro"],
)
def pipeline_etl_api():

    @task()
    def extracao():
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        order_data_dict = json.loads(data_string)
        return order_data_dict

    @task(multiple_outputs=True)
    def transformacao(order_data_dict: dict):
        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value
        return {"total_order_value": total_order_value}

    @task()
    def ler(total_order_value: float):
        print(f"Total order value is: {total_order_value:.2f}")

    order_data = extracao()
    order_summary = transformacao(order_data)
    ler(order_summary["total_order_value"])

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
  tags=["unifametro"],
) as dag:
  email_consolidado = EmailOperator(
      task_id = "email_consolidado",
      to=['email@gmail.com'],
      subject='Consolidados de recebiveis',
      html_content=(
        'Consolidado dos recebiveis esperados para '
        'Data :<br><br>'
        "<b>Valor total :</b> R$ {{100}}<br>"
        "<b>Taxas:</b> R$ {{100}}<br>"
      ),
      files=None,
      dag=dag,
    )

pipeline_etl_api()
