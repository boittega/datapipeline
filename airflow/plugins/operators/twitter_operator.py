import json
from typing import Optional
from pathlib import Path

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from hooks.twitter_hook import TwitterHook
from twitter_scrapper.auxiliar_classes import TweetFields, UserFields


class TwitterOperator(BaseOperator):
    """
    Airflow Operator to store Twitter data localy
    """

    template_fields = [
        "query",
        "file_path",
        "start_time",
        "end_time",
    ]
    template_ext = ()
    ui_color = "#1DA1F2"

    @apply_defaults
    def __init__(
        self,
        query: str,
        file_path: str,
        conn_id: Optional[str] = None,
        bearer: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        tweet_fields: Optional[TweetFields] = None,
        user_data: Optional[bool] = None,
        user_fields: Optional[UserFields] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.query = query
        self.file_path = file_path
        self.conn_id = conn_id
        self.bearer = bearer
        self.start_time = start_time
        self.end_time = end_time
        self.tweet_fields = tweet_fields
        self.user_data = user_data
        self.user_fields = user_fields

    def create_parent_folder(self):
        Path(Path(self.file_path).parent).mkdir(parents=True, exist_ok=True)

    def execute(self, context):
        self.create_parent_folder()
        with open(self.file_path, "w") as output_file:
            for page in TwitterHook(
                self.query,
                self.conn_id,
                self.bearer,
                self.start_time,
                self.end_time,
                self.tweet_fields,
                self.user_data,
                self.user_fields,
            ).tweet_search():
                json.dump(page, output_file, ensure_ascii=False)
                output_file.write("\n")
