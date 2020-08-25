def test_extract(tweetscrapper_class, test_data):
    result = tweetscrapper_class.extract()

    test_result = test_data[0]

    assert result == test_result


def test_paginate(tweetscrapper_class, test_data):
    result = tweetscrapper_class.paginate()

    test_result = test_data

    assert [x for x in result] == test_result
