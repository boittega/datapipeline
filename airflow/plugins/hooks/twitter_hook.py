from typing import Iterator, Optional

from airflow.hooks.base_hook import BaseHook
from twitter_scrapper.auxiliar_classes import TweetFields, UserFields
from twitter_scrapper.tweet_search import TweetSearch


class TwitterHook(BaseHook):
    """
    Airflow Hook to get data from Twitter Scrapper package

    :param query: Query string
    :type query: str
    :param conn_id: Connection name, defaults to "twitter_default"
    :type conn_id: str
    :param bearer: Twitter authentication bearer token, gets from
    connection if not sent.
    :type bearer: str
    :param start_time: Twitter query start time
    :type start_time: str
    :param end_time: Twitter query end time
    :type end_time: str
    :param tweet_fields: List of tweet columns to return
    :type tweet_fields: TweetFields dataclass
    :param user_data: Flag to user data
    :type user_data: bool
    :param user_fields: List of user columns to return
    :type user_fields: UserFields dataclass
    """

    def __init__(
        self,
        query: str,
        conn_id: Optional[str] = None,
        bearer: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        tweet_fields: Optional[TweetFields] = None,
        user_data: Optional[bool] = None,
        user_fields: Optional[UserFields] = None,
    ):
        self.query = query
        self.conn_id = conn_id or "twitter_default"
        self.bearer = bearer or self._get_conn_bearer()
        self.start_time = start_time
        self.end_time = end_time
        self.tweet_fields = tweet_fields or TweetFields()
        self.user_data = user_data or False
        self.user_fields = user_fields or UserFields()

    def _get_conn_bearer(self) -> str:
        """
        Returns the bearer on connection extra
        """
        conn = self.get_connection(self.conn_id)
        return conn.extra_dejson.get("bearer")

    def tweet_search(self) -> Iterator[dict]:
        """
        Returns the TweetSearch query generator
        """
        ts = TweetSearch(self.bearer)

        yield from ts.tweet_search(
            query=self.query,
            start_time=self.start_time,
            end_time=self.end_time,
            tweet_fields=self.tweet_fields,
            user_data=self.user_data,
            user_fields=self.user_fields,
        )
