def test_tweet_search(tweetsearch_class, test_data):
    result = tweetsearch_class.tweet_search(query="test", user_data=True)

    test_result = test_data

    assert [x for x in result] == test_result
