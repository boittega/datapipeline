from typing import Generator

from .auxiliar_classes import TweetFields, UserFields
from .core import TweetScrapper


class TweetSearch(TweetScrapper):
    def __init__(
        self,
        bearer_token,
        url_scheme=None,
        url_base=None,
        url_path=None,
        url_query=None,
    ):
        self.url_path = url_path or "/2/tweets/search/recent"
        super().__init__(bearer_token, url_scheme, url_base, self.url_path, url_query)

    def tweet_search(
        self,
        query,
        tweet_fields=TweetFields(),
        user_data=False,
        user_fields=UserFields(),
    ) -> Generator:
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
