from dataclasses import asdict
from ..twitter_scrapper.auxiliar_classes import TweetFields


def test_activate_fields():
    tweetfields_class = TweetFields.activate_fields()

    assert all([value for key, value in asdict(tweetfields_class).items()])


def test_activate_public_fields():
    non_public_fields = [
        "non_public_metrics",
        "organic_metrics",
        "promoted_metrics",
    ]

    tweetfields_class = TweetFields.activate_public_fields()

    assert not any(
        [
            value
            for key, value in asdict(tweetfields_class).items()
            if key in non_public_fields
        ]
    )
