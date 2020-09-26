from pyspark.sql import DataFrame, SparkSession
import pytest


@pytest.fixture(scope="session")
def spark_session() -> SparkSession:
    spark = SparkSession.builder.appName("Test Twitter Spark job").getOrCreate()
    yield spark
    spark.stop()


@pytest.fixture(scope="session")
def twitter_df(spark_session) -> DataFrame:
    return spark_session.read.json("tests/data/twitter_test.json")
