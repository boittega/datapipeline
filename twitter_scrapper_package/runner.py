import argparse
import json
from datetime import datetime, timedelta

from twitter_scrapper.auxiliar_classes import TweetFields, UserFields
from twitter_scrapper.tweet_search import TweetSearch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twitter Scrapper")
    parser.add_argument("--search", help="Search string")
    parser.add_argument("--bearer", help="Twitter bearer token")

    args = parser.parse_args()
    ts = TweetSearch(args.bearer)

    tf = TweetFields()
    tf.activate_all_public_fields()

    uf = UserFields()
    uf.activate_all_fields()

    timestamp_format = "%Y-%m-%dT%H:%M:%S.00Z"

    with open(f"{args.search}.json", "w") as f:
        t = ts.tweet_search(
            query=args.search,
            start_time=(datetime.now().date() - timedelta(days=2)).strftime(
                timestamp_format
            ),
            end_time=(datetime.now().date() - timedelta(days=1)).strftime(
                timestamp_format
            ),
            tweet_fields=tf,
            user_data=True,
            user_fields=uf,
        )
        for page in t:
            json.dump(page, f, ensure_ascii=False)
            f.write("\n")
