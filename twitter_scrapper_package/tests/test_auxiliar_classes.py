from dataclasses import asdict


def test_activate_all_fields(tweetfields_class):
    tweetfields_class.activate_all_fields()

    assert all([value for key, value in asdict(tweetfields_class).items()])


def test_activate_all_public_fields(tweetfields_class):
    non_public_fields = [
        "non_public_metrics",
        "organic_metrics",
        "promoted_metrics",
    ]

    tweetfields_class.activate_all_public_fields()

    assert all(
        [
            value
            for key, value in asdict(tweetfields_class).items()
            if key not in non_public_fields
        ]
    )
