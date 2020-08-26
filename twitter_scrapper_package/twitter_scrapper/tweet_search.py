from typing import Iterator

from .auxiliar_classes import TweetFields, UserFields
from .core import TweetScrapper


class TweetSearch(TweetScrapper):
    """
    Class to request Twitter Search API endpoint

    :param bearer_token: Twitter authentication bearer token
    :type bearer_token: str
    :param url_scheme: Twitter URL Scheme, defaults to "https"
    :type url_scheme: str
    :param url_base: Twitter URL base, defaults to "api.twitter.com"
    :type url_base: str
    :param url_path: Twitter URL path, defaults to "/2/tweets/search/recent"
    :type url_path: str
    :param url_query: Twitter URL query, defaults to {}
    :type url_query: dict
    """

    def __init__(
        self,
        bearer_token,
        url_scheme=None,
        url_base=None,
        url_path=None,
        url_query=None,
    ):
        self.url_path = url_path or "/2/tweets/search/recent"
        super().__init__(
            bearer_token, url_scheme, url_base, self.url_path, url_query
        )

    def tweet_search(
        self,
        query,
        tweet_fields=TweetFields(),
        user_data=False,
        user_fields=UserFields(),
    ) -> Iterator[dict]:
        """
        Queries Twitter Search

        :param query: Query string
        :type query: str
        :param tweet_fields: Tweet fields requested, defaults to TweetFields()
        :type tweet_fields: TweetFields class, optional
        :param user_data: Include user data, defaults to False
        :type user_data: bool, optional
        :param user_fields: User fields requested, defaults to UserFields()
        :type user_fields: UserFields class, optional
        :yield: Yields Twitter Search results
        :rtype: Iterator[dict]
        """
        query_dict = {
            "query": query,
            "tweet.fields": tweet_fields.get_activated_fields(),
        }

        if user_data:
            query_dict.update(
                {
                    "expansions": "author_id",
                    "user.fields": user_fields.get_activated_fields(),
                }
            )

        self.url_query.update(query_dict)
        yield from self.paginate()
