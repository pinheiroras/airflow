from __future__ import annotations
from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG

from airflow.operators.base import BaseOperator

with DAG(
  "alomundo",
  default_args={
    "depends_on_past": False,
    "email": ["pinheiro.ras@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
  },
  
)