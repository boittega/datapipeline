from dataclasses import dataclass, fields, asdict
from typing import Optional, List


@dataclass
class TweetBaseDataclass:
    @classmethod
    def activate_fields(
        cls,
        include_only: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None,
    ) -> "TweetBaseDataclass":
        """
        Set Fields to true.

        :param include_only: List of fields to activate, activate all
        if None is sent, defaults to None
        :type include_only: Optional[List[str]], optional
        :param exclude: List of fields to not activate, defaults to None
        :type exclude: Optional[List[str]], optional
        """
        obj = cls()
        for key in fields(obj):
            if (
                (include_only and key.name in include_only)
                or (exclude and key.name not in exclude)
                or not include_only
            ):
                setattr(obj, key.name, True)
        return obj

    def get_activated_fields(self) -> str:
        """
        Return a comma separated list of field names
        """
        return ",".join([key for key, value in asdict(self).items() if value])


@dataclass
class TweetFields(TweetBaseDataclass):
    id: bool = True
    text: bool = True
    attachments: bool = False
    author_id: bool = False
    context_annotations: bool = False
    conversation_id: bool = False
    created_at: bool = False
    entities: bool = False
    geo: bool = False
    in_reply_to_user_id: bool = False
    lang: bool = False
    non_public_metrics: bool = False
    public_metrics: bool = False
    organic_metrics: bool = False
    promoted_metrics: bool = False
    possibly_sensitive: bool = False
    referenced_tweets: bool = False
    source: bool = False
    withheld: bool = False

    @classmethod
    def activate_public_fields(cls) -> "TweetFields":
        """
        Activate all but the non public fields.
        """
        return cls.activate_fields(
            exclude=[
                "non_public_metrics",
                "organic_metrics",
                "promoted_metrics",
            ]
        )


@dataclass
class UserFields(TweetBaseDataclass):
    id: bool = True
    name: bool = True
    username: bool = True
    created_at: bool = False
    description: bool = False
    entities: bool = False
    location: bool = False
    pinned_tweet_id: bool = False
    profile_image_url: bool = False
    protected: bool = False
    public_metrics: bool = False
    url: bool = False
    verified: bool = False
    withheld: bool = False
