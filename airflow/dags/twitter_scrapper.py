from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.my_plugins import TwitterOperator

args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(15),
}


with DAG(
    "twitter_scrapper",
    default_args=args,
    schedule_interval="0 * * * *",
    max_active_runs=1,
) as dag:
    dummy = TwitterOperator(task_id="one")
