from pathlib import Path
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.my_plugins import TwitterOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from twitter_scrapper.auxiliar_classes import TweetFields, UserFields
from twitter_scrapper.tweet_search import TWEET_SEARCH_TIME_FORMAT

args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(7),
}

base_folder = Path.joinpath(
    Path("~/Documents").expanduser(), "twitter_scrapper"
)
partition_folder = "exported_date={{ ts_nodash }}"
bronze_folder = Path.joinpath(base_folder, "bronze", partition_folder)
silver_folder = Path.joinpath(base_folder, "silver", partition_folder)


with DAG(
    "twitter_scrapper",
    default_args=args,
    schedule_interval="0 7 * * *",
    max_active_runs=1,
) as dag:
    twitter_search = TwitterOperator(
        task_id="get_twitter_aluraonline",
        query="AluraOnline",
        file_path=str(Path.joinpath(
            bronze_folder, "Twitter_AluraOnline_{{ ts_nodash }}.json"
        )),
        start_time=(
            "{{" f" execution_date.strftime('{TWEET_SEARCH_TIME_FORMAT}') " "}}"
        ),
        end_time=(
            "{{"
            f" next_execution_date.strftime('{TWEET_SEARCH_TIME_FORMAT}') "
            "}}"
        ),
        tweet_fields=TweetFields.activate_public_fields(),
        user_data=True,
        user_fields=UserFields.activate_fields(),
    )

    twitter_transform = SparkSubmitOperator(
        task_id="transform_twitter_aluraonline",
        application=str(Path.joinpath(
            Path(__file__).parents[2], "spark/twitter_search_transformation.py"
        )),
        name="Twitter_search_transformation",
        application_args=[
            "--src",
            str(bronze_folder),
            "--dest",
            str(silver_folder),
        ],
    )

    twitter_search >> twitter_transform
