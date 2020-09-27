import argparse
from os import path
from typing import List

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, explode, lit

DEFAULT_TWEET_COLUMNS = [
    "author_id",
    "conversation_id",
    "created_at",
    "id",
    "in_reply_to_user_id",
    "lang",
    "possibly_sensitive",
    "public_metrics.like_count",
    "public_metrics.quote_count",
    "public_metrics.reply_count",
    "source",
    "text",
]

DEFAULT_USER_COLUMNS = [
    "created_at",
    "description",
    "id",
    "location",
    "name",
    "pinned_tweet_id",
    "profile_image_url",
    "protected",
    "public_metrics.followers_count",
    "public_metrics.following_count",
    "public_metrics.listed_count",
    "public_metrics.tweet_count",
    "url",
    "username",
    "verified",
]


def export_csv(df: DataFrame, dest: str):
    df.coalesce(1).write.option("header", True).mode("overwrite").csv(dest)


def get_first_level(
    df: DataFrame, first_level_col: str, column_list: List[str]
):
    return (
        df.select(explode(col(first_level_col)))
        .select("col.*")
        .select(*column_list)
    )


def twitter_search_transform(
    spark: SparkSession,
    src: str,
    dest: str,
    processed_at: str,
    tweet_columns: List[str],
    export_users_flag: bool,
    user_columns: List[str],
):
    df = spark.read.json(src)

    formatted_dest = path.join(
        dest, "{table_name}", f"exported_date={processed_at}"
    )

    tweet_df = get_first_level(
        df=df, first_level_col="data", column_list=tweet_columns
    ).withColumn("processed_at", lit(processed_at))
    export_csv(tweet_df, formatted_dest.format(table_name="tweet"))

    if export_users_flag:
        user_df = get_first_level(
            df=df, first_level_col="includes.users", column_list=user_columns
        ).withColumn("processed_at", lit(processed_at))
        export_csv(user_df, formatted_dest.format(table_name="user"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Spark Twitter Search tranformation"
    )
    parser.add_argument("--src", help="Source folder", required=True)
    parser.add_argument("--dest", help="Destination folder", required=True)
    parser.add_argument(
        "--processed-at", help="Processed timestamp", default=""
    )
    parser.add_argument(
        "--tweet-columns",
        default=DEFAULT_TWEET_COLUMNS,
        nargs="+",
        help="List of tweet columns to export",
    )
    parser.add_argument(
        "--export-users",
        default=True,
        type=bool,
        help="Export users flag (true/false), default true",
    )
    parser.add_argument(
        "--user-columns",
        default=DEFAULT_USER_COLUMNS,
        nargs="+",
        help="List of user columns to export",
    )

    args = parser.parse_args()

    spark = SparkSession.builder.appName(
        name="twitter_search_transformation"
    ).getOrCreate()

    twitter_search_transform(
        spark=spark,
        src=args.src,
        dest=args.dest,
        processed_at=args.processed_at,
        tweet_columns=args.tweet_columns,
        export_users_flag=args.export_users,
        user_columns=args.user_columns,
    )
