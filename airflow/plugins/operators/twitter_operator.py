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

    :param query: Query string, templated
    :type query: str
    :param file_path: Export file path, templated
    :type file_path: str
    :param conn_id: Connection name, optional
    :type conn_id: Optional[str]
    :param bearer: Twitter authentication bearer token, gets from
    connection if not sent, optional
    :type bearer: Optional[str]
    :param start_time: Twitter query start time, templated and optional
    :type start_time: Optional[str]
    :param end_time: Twitter query end time, templated and optional
    :type end_time: Optional[str]
    :param tweet_fields: List of tweet columns to return, optional
    :type tweet_fields: Optional[TweetFields]
    :param user_data: Flag to user data, optional
    :type user_data: Optional[bool]
    :param user_fields: List of user columns to return, optional
    :type user_fields: Optional[UserFields]
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
        """
        Create parent folder if not exists
        """
        Path(Path(self.file_path).parent).mkdir(parents=True, exist_ok=True)

    def execute(self, context):
        """
        Extract Twitter search data into json file
        """
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
