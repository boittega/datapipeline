from typing import Iterator, Optional, Dict, Any

from airflow.hooks.base_hook import BaseHook
from twitter_scrapper.auxiliar_classes import TweetFields, UserFields
from twitter_scrapper.tweet_search import TweetSearch


class TwitterHook(BaseHook):
    """
    Airflow Hook to get data from Twitter Scrapper package

    :param query: Query string
    :type query: str
    :param conn_id: Connection name, defaults to "twitter_default"
    :type conn_id: Optional[str]
    :param bearer: Twitter authentication bearer token, gets from
    connection if not sent.
    :type bearer: Optional[str]
    :param start_time: Twitter query start time, optional
    :type start_time: Optional[str]
    :param end_time: Twitter query end time, optional
    :type end_time: Optional[str]
    :param tweet_fields: List of tweet columns to return, optional
    :type tweet_fields: Optional[TweetFields]
    :param user_data: Flag to user data, defaults to false
    :type user_data: Optional[bool]
    :param user_fields: List of user columns to return, optional
    :type user_fields: Optional[UserFields]
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

    def tweet_search(self) -> Iterator[Dict[str, Any]]:
        """
        Returns the TweetSearch query generator

        :yield: Yield each page
        :rtype: Iterator[Dict[str, Any]]
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
