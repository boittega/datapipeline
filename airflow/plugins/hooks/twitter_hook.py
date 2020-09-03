from typing import Iterator, Optional

from airflow.hooks.base_hook import BaseHook
from twitter_scrapper.auxiliar_classes import TweetFields, UserFields
from twitter_scrapper.tweet_search import TweetSearch


class TwitterHook(BaseHook):
    """
    """

    def __init__(
        self,
        query: str,
        conn_id: Optional[str] = None,
        bearer: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ):
        super().__init__()
        self.query = query
        self.conn_id = conn_id or "twitter_default"
        self.bearer = bearer or self._get_conn_bearer()
        self.start_time = start_time
        self.end_time = end_time

    def _get_conn_bearer(self) -> str:
        """
        Returns the bearer on connection extra
        """
        conn = self.get_connection(self.conn_id)
        return conn.extra_dejson.get("bearer")

    def tweet_search(self) -> Iterator[dict]:
        ts = TweetSearch(self.bearer)

        tf = TweetFields()
        tf.activate_all_public_fields()

        uf = UserFields()
        uf.activate_all_fields()

        yield from ts.tweet_search(
            query=self.query,
            start_time=self.start_time,
            end_time=self.end_time,
            tweet_fields=tf,
            user_data=True,
            user_fields=uf,
        )
