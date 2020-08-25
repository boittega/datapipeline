from typing import Generator
from urllib.parse import urlencode, urlunparse

import requests


class TweetScrapper:
    def __init__(
        self,
        bearer_token,
        url_scheme=None,
        url_base=None,
        url_path=None,
        url_query=None,
    ):
        self.bearer_token = bearer_token
        self.url_scheme = url_scheme or "https"
        self.url_base = url_base or "api.twitter.com"
        self.url_path = url_path or ""
        self.url_query = url_query or {}

    def create_url(self) -> str:
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

    def paginate(self, next_token="") -> Generator:
        if next_token:
            self.url_query.update({"next_token": next_token})

        data = self.extract()
        yield data

        if "next_token" in data.get("meta", {}):
            yield from self.paginate(next_token=data["meta"]["next_token"])

    def extract(self) -> dict:
        response = requests.get(
            url=self.create_url(),
            headers={"Authorization": f"Bearer {self.bearer_token}"},
        )
        response.raise_for_status()
        return response.json()
