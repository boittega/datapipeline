INSERT INTO twitter.user
(
    created_at,
    description,
    id,
    location,
    name,
    pinned_tweet_id,
    profile_image_url,
    protected,
    followers_count,
    following_count,
    listed_count,
    tweet_count,
    url,
    username,
    verified,
    processed_at
) SELECT 
    created_at,
    description,
    id,
    location,
    name,
    pinned_tweet_id,
    profile_image_url,
    protected,
    followers_count,
    following_count,
    listed_count,
    tweet_count,
    url,
    username,
    verified,
    processed_at
FROM (
    SELECT *,
    row_number() over(partition by id) as rn
    FROM twitter_staging.user SUi
    WHERE processed_at = '{{ ts_nodash }}'
    AND NOT EXISTS(SELECT 1 FROM twitter.user TU WHERE TU.id = SUi.id AND TU.processed_at > SUi.processed_at)
) SU WHERE rn = 1
ON CONFLICT (id) DO UPDATE
SET
    created_at=EXCLUDED.created_at,
    description=EXCLUDED.description,
    location=EXCLUDED.location,
    name=EXCLUDED.name,
    pinned_tweet_id=EXCLUDED.pinned_tweet_id,
    profile_image_url=EXCLUDED.profile_image_url,
    protected=EXCLUDED.protected,
    followers_count=EXCLUDED.followers_count,
    following_count=EXCLUDED.following_count,
    listed_count=EXCLUDED.listed_count,
    tweet_count=EXCLUDED.tweet_count,
    url=EXCLUDED.url,
    username=EXCLUDED.username,
    verified=EXCLUDED.verified,
    processed_at=EXCLUDED.processed_at,
    updated_at=NOW();

DELETE FROM twitter_staging.user
WHERE processed_at = '{{ ts_nodash }}';
