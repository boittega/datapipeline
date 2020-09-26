from os.path import isfile
from ..twitter_search.transformation import (
    export_parquet,
    get_first_level,
    export_tweets,
    export_users,
    twitter_search_transform,
)


def test_export_parquet(spark_session, twitter_df, tmp_path):
    export_parquet(spark=spark_session, df=twitter_df, dest=str(tmp_path))

    assert isfile(tmp_path / "_SUCCESS")


def test_get_first_level(spark_session, twitter_df):
    df = get_first_level(
        spark=spark_session,
        df=twitter_df,
        first_level_col="data",
        column_list=["text"],
    )

    result_df = ['{"text":"Tweet test"}']

    assert df.select("text").toJSON().collect() == result_df


def test_export_tweets(spark_session, twitter_df, tmp_path):
    export_tweets(
        spark=spark_session,
        df=twitter_df,
        dest=str(tmp_path),
        tweet_columns=["text"],
    )
    assert isfile(tmp_path / "tweet/_SUCCESS")


def test_export_user(spark_session, twitter_df, tmp_path):
    export_users(
        spark=spark_session,
        df=twitter_df,
        dest=str(tmp_path),
        user_columns=["name"],
    )
    assert isfile(tmp_path / "user/_SUCCESS")


def test_twitter_search_transform(spark_session, tmp_path):

    twitter_search_transform(
        spark=spark_session,
        src="tests/data/twitter_test.json",
        dest=str(tmp_path),
        tweet_columns=["text"],
        export_users_flag=True,
        user_columns=["name"],
    )
    assert isfile(tmp_path / "user/_SUCCESS")
    assert isfile(tmp_path / "tweet/_SUCCESS")
