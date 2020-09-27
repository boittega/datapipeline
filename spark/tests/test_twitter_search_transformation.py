from os.path import isfile
from ..twitter_search.transformation import (
    export_csv,
    get_first_level,
    twitter_search_transform,
)


def test_export_csv(spark_session, tmp_path):
    df = spark_session.createDataFrame([(1, "test")], ["id", "name"])
    export_csv(df=df, dest=str(tmp_path))

    assert isfile(tmp_path / "_SUCCESS")


def test_get_first_level(twitter_df):
    df = get_first_level(
        df=twitter_df, first_level_col="data", column_list=["text"]
    )

    result_df = ['{"text":"Tweet test"}']

    assert df.select("text").toJSON().collect() == result_df


def test_twitter_search_transform(spark_session, tmp_path):
    processed_at = "123"
    twitter_search_transform(
        spark=spark_session,
        src="tests/data/twitter_test.json",
        dest=str(tmp_path),
        processed_at=processed_at,
        tweet_columns=["text"],
        export_users_flag=True,
        user_columns=["name"],
    )
    assert isfile(tmp_path / f"user/exported_date={processed_at}/_SUCCESS")
    assert isfile(tmp_path / f"tweet/exported_date={processed_at}/_SUCCESS")
