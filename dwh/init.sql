CREATE SCHEMA twitter;

CREATE TABLE twitter.tweet (
    id VARCHAR(20) PRIMARY KEY,
    text VARCHAR(500),
    created_at TIMESTAMP,
    author_id VARCHAR(20),
    conversation_id VARCHAR(20),
    in_reply_to_user_id VARCHAR(20),
    possibly_sensitive BOOLEAN,
    like_count BIGINT,
    quote_count BIGINT,
    reply_count BIGINT,
    lang VARCHAR(20),
    source VARCHAR(500),
    processed_at varchar(30),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE twitter.user (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50),
    username VARCHAR(15),
    created_at TIMESTAMP,
    description VARCHAR(500),
    location VARCHAR(500),
    pinned_tweet_id VARCHAR(20),
    profile_image_url VARCHAR(500),
    protected BOOLEAN,
    followers_count BIGINT,
    following_count BIGINT,
    listed_count BIGINT,
    tweet_count BIGINT,
    url VARCHAR(500),
    verified BOOLEAN,
    processed_at varchar(30),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE SCHEMA twitter_staging;

CREATE TABLE twitter_staging.tweet (
    id VARCHAR(20),
    text VARCHAR(500),
    created_at TIMESTAMP,
    author_id VARCHAR(20),
    conversation_id VARCHAR(20),
    in_reply_to_user_id VARCHAR(20),
    possibly_sensitive BOOLEAN,
    like_count BIGINT,
    quote_count BIGINT,
    reply_count BIGINT,
    lang VARCHAR(20),
    source VARCHAR(500),
    processed_at varchar(30)
);

CREATE TABLE twitter_staging.user (
    id VARCHAR(20),
    name VARCHAR(50),
    username VARCHAR(15),
    created_at TIMESTAMP,
    description VARCHAR(500),
    location VARCHAR(500),
    pinned_tweet_id VARCHAR(20),
    profile_image_url VARCHAR(500),
    protected BOOLEAN,
    followers_count BIGINT,
    following_count BIGINT,
    listed_count BIGINT,
    tweet_count BIGINT,
    url VARCHAR(500),
    verified BOOLEAN,
    processed_at varchar(30)
);
