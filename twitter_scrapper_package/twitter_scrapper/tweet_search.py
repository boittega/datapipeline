from typing import Iterator, Optional, Dict, Any

from .auxiliar_classes import TweetFields, UserFields
from .core import TweetScrapper

TWEET_SEARCH_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"


class TweetSearch(TweetScrapper):
    """
    Class to request Twitter Search API endpoint

    :param bearer_token: Twitter authentication bearer token
    :type bearer_token: Optional[str]
    :param url_scheme: Twitter URL Scheme, defaults to "https"
    :type url_scheme: Optional[str]
    :param url_base: Twitter URL base, defaults to "api.twitter.com"
    :type url_base: Optional[str]
    :param url_path: Twitter URL path, defaults to "/2/tweets/search/recent"
    :type url_path: Optional[str]
    :param url_query: Twitter URL query, defaults to {}
    :type url_query: Optional[Dict[str, str]]
    """

    def __init__(
        self,
        bearer_token,
        url_scheme: Optional[str] = None,
        url_base: Optional[str] = None,
        url_path: Optional[str] = None,
        url_query: Optional[Dict[str, str]] = None,
    ):
        self.url_path = url_path or "/2/tweets/search/recent"
        super().__init__(
            bearer_token, url_scheme, url_base, self.url_path, url_query
        )

    def tweet_search(
        self,
        query: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        tweet_fields: Optional[TweetFields] = TweetFields(),
        user_data: Optional[bool] = False,
        user_fields: Optional[UserFields] = UserFields(),
    ) -> Iterator[Dict[str, Any]]:
        """
        Queries Twitter Search

        :param query: Query string
        :type query: Optional[str]
        :param start_time: The oldest UTC timestamp, from most recent 7 days,
        to which the Tweets will be provided. Format YYYY-MM-DDTHH:mm.ssZ.
        Defaults to None
        :type start_time: Optional[str]
        :param end_time: The most recent UTC timestamp, as recent as 30 seconds
        ago, to which the Tweets will be provided. Format YYYY-MM-DDTHH:mm.ssZ.
        Defaults to None.
        :type end_time: Optional[str]
        :param tweet_fields: Tweet fields requested, defaults to TweetFields()
        :type tweet_fields: Optional[TweetFields]
        :param user_data: Include user data, defaults to False
        :type user_data: Optional[bool]
        :param user_fields: User fields requested, defaults to UserFields()
        :type user_fields: Optional[UserFields]
        :yield: Yields Twitter Search results
        :rtype: Iterator[Dict[str, Any]]
        """
        query_dict = {
            "query": query,
            "tweet.fields": tweet_fields.get_activated_fields(),
        }

        if start_time:
            query_dict.update({"start_time": start_time})

        if end_time:
            query_dict.update({"end_time": end_time})

        if user_data:
            query_dict.update(
                {
                    "expansions": "author_id",
                    "user.fields": user_fields.get_activated_fields(),
                }
            )

        self.url_query.update(query_dict)
        yield from self.paginate()
