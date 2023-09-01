from __future__ import annotations

import json

import pendulum

from airflow.decorators import dag, task
from airflow.timetables.trigger import CronTriggerTimetable

@dag(
    start_date=pendulum.datetime(2023, 9, 1, tz="UTC"),
    catchup=False,
    tags=["unifametro"],
    schedule=CronTriggerTimetable("*/3 * * * *", timezone="UTC"),
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
    def leitura(total_order_value: float):
        print(f"Total order value is: {total_order_value:.2f}")

    order_data = extracao()
    order_summary = transformacao(order_data)
    leitura(order_summary["total_order_value"])

pipeline_etl_api()
