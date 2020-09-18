import argparse
from os import path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode

tweet_columns = [
    "data.author_id",
    "data.conversation_id",
    "data.created_at",
    "data.id",
    "data.in_reply_to_user_id",
    "data.lang",
    "data.possibly_sensitive",
    "data.public_metrics.like_count",
    "data.public_metrics.quote_count",
    "data.public_metrics.reply_count",
    "data.source",
    "data.text",
]

user_columns = [
    "users.created_at",
    "users.description",
    "users.id",
    "users.location",
    "users.name",
    "users.pinned_tweet_id",
    "users.profile_image_url",
    "users.protected",
    "users.public_metrics.followers_count",
    "users.public_metrics.following_count",
    "users.public_metrics.listed_count",
    "users.public_metrics.tweet_count",
    "users.url",
    "users.username",
    "users.verified",
]


def tranform_search(src, dest):
    spark = SparkSession.builder.appName(
        name="twitter_search_transformation"
    ).getOrCreate()

    df = spark.read.json(src)

    tweet_df = df.select(explode(col("data")).alias("data")).select(
        *tweet_columns
    )

    user_df = df.select(explode(col("includes.users")).alias("users")).select(
        *user_columns
    )

    tweet_df.coalesce(1).write.mode("overwrite").parquet(
        path.join(dest, "tweet")
    )

    user_df.coalesce(1).write.mode("overwrite").parquet(path.join(dest, "user"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Spark Twitter Search tranformation"
    )
    parser.add_argument("--src", help="Source folder")
    parser.add_argument("--dest", help="Destination folder")

    args = parser.parse_args()

    tranform_search(args.src, args.dest)
