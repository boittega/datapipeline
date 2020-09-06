import pytest

from ..twitter_scrapper.core import TweetScrapper, requests
from ..twitter_scrapper.tweet_search import TweetSearch


@pytest.fixture
def test_data() -> list:
    return [
        {
            "data": [{"data": "1"}],
            "includes": {"users": [{"user": "1"}]},
            "meta": {"next_token": "123"},
        },
        {
            "data": [{"data": "1"}],
            "includes": {"users": [{"user": "1"}]},
            "meta": {},
        },
    ]


@pytest.fixture
def tweetscrapper_class():
    return TweetScrapper(bearer_token="")


@pytest.fixture
def tweetsearch_class():
    return TweetSearch(bearer_token="")


class MockResponse:
    def __init__(self, url, json_data, status_code):
        self.url = url
        self.json_data = json_data
        self.status_code = status_code
        self.call_n = 0

    @staticmethod
    def raise_for_status():
        pass

    def json(self):
        if "next_token" in self.url:
            self.call_n += 1
        return self.json_data[self.call_n]


@pytest.fixture(autouse=True)
def mock_request(monkeypatch, test_data):
    def mock_get(*args, **kwargs):
        return MockResponse(
            url=kwargs["url"], json_data=test_data, status_code=200
        )

    monkeypatch.setattr(requests, "get", mock_get)
