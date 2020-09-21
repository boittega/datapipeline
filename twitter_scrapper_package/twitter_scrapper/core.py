from typing import Iterator, Optional, Dict, Any
from urllib.parse import urlencode, urlunparse

import requests


class TweetScrapper:
    """
    Base class to request data from Twitter's API

    :param bearer_token: Twitter authentication bearer token
    :type bearer_token: Optional[str]
    :param url_scheme: Twitter URL Scheme, defaults to "https"
    :type url_scheme: Optional[str]
    :param url_base: Twitter URL base, defaults to "api.twitter.com"
    :type url_base: Optional[str]
    :param url_path: Twitter URL path, defaults to ""
    :type url_path: Optional[str]
    :param url_query: Twitter URL query, defaults to {}
    :type url_query: Optional[Dict[str, str]]
    """

    def __init__(
        self,
        bearer_token: str,
        url_scheme: Optional[str] = None,
        url_base: Optional[str] = None,
        url_path: Optional[str] = None,
        url_query: Optional[Dict[str, str]] = None,
    ):
        self.bearer_token = bearer_token
        self.url_scheme = url_scheme or "https"
        self.url_base = url_base or "api.twitter.com"
        self.url_path = url_path or ""
        self.url_query = url_query or {}

    def create_url(self) -> str:
        """
        Unparse the URL parameters into a single URL,
        encoding the query dictionary.
        It joins the url_scheme, url_base, url_path
        and encoded url_query.

        :return: URL string
        :rtype: str
        """
        return urlunparse(
            (
                self.url_scheme,
                self.url_base,
                self.url_path,
                "",
                urlencode(self.url_query),
                "",
            )
        )

    def paginate(self, next_token: str = "") -> Iterator[Dict[str, Any]]:
        """
        Paginage API requests

        :param next_token: Next page token, defaults to ""
        :type next_token: str, optional
        :yield: Yield one page
        :rtype: Iterator[Dict[str, Any]]
        """
        if next_token:
            self.url_query.update({"next_token": next_token})

        data = self.extract()
        yield data

        if "next_token" in data.get("meta", {}):
            yield from self.paginate(next_token=data["meta"]["next_token"])

    def extract(self) -> Dict[str, Any]:
        """
        Request data from API

        :return: The API JSON response
        :rtype: Dict[str, Any]
        """
        response = requests.get(
            url=self.create_url(),
            headers={"Authorization": f"Bearer {self.bearer_token}"},
        )
        response.raise_for_status()
        return response.json()
