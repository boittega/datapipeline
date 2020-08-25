from dataclasses import dataclass, fields, asdict


@dataclass
class TweetBaseDataclass:
    def activate_all_fields(self, excetion=[]):
        for key in fields(self):
            if key.name not in excetion:
                setattr(self, key.name, True)

    def get_activated_fields(self) -> str:
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

    def activate_all_public_fields(self):
        self.activate_all_fields(
            excetion=["non_public_metrics", "organic_metrics", "promoted_metrics"]
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
