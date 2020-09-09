from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.my_plugins import TwitterOperator
from twitter_scrapper.auxiliar_classes import TweetFields, UserFields
from twitter_scrapper.tweet_search import TWEET_SEARCH_TIME_FORMAT

args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(7),
}


with DAG(
    "twitter_scrapper",
    default_args=args,
    schedule_interval="0 7 * * *",
    max_active_runs=1,
) as dag:
    twitter_search = TwitterOperator(
        task_id="get_twitter_aluraonline",
        query="AluraOnline",
        file_path=(
            "/Users/rbottega/Documents/twitter_scrapper/"
            "exported_date={{ ts_nodash }}/"
            "Twitter_AluraOnline_{{ ts_nodash }}.json"
        ),
        start_time=(
            "{{"
            f" execution_date.strftime('{TWEET_SEARCH_TIME_FORMAT}') "
            "}}"
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
