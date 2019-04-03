#!/usr/bin/env python2

"""Unit tests for the food2fork_api module."""

import pytest
import colorlog

from food_finder import food2fork_api

colorlog.basicConfig(level="INFO")
_log = colorlog.getLogger(__name__)

try:
    with open("./secrets/f2f_api_key", "r") as key_file:
        _KEY = key_file.readline()
except:
    _KEY = "fakeFood2ForkApiKey"

def test_build_query_endpoint_url():
    api = food2fork_api.Food2ForkAPI(_KEY)

    # Query endpoint requires a string type, so giving it None or some other
    # type should throw an exception
    with pytest.raises(AssertionError):
        url = api.build_query_endpoint_url(None)
    with pytest.raises(AssertionError):
        url = api.build_query_endpoint_url(5)
    
    # Subtest 2: query may be left empty, which defaults to q="", and is a valid
    # API request.
    url = api.build_query_endpoint_url()
    expected = "{}?key={}".format(food2fork_api._QUERY_ENDPOINT,
                                  _KEY)
    _log.info("Asserting that '{}' equals '{}'".format(url, expected))
    assert url == expected

def test_build_recipe_details_endpoint_url():
    api = food2fork_api.Food2ForkAPI(_KEY)
    url = api.build_recipe_details_endpoint_url()
    expected = "{}?key={}".format(food2fork_api._RECIPE_DETAILS_ENDPOINT,
                                  _KEY)
    _log.info("Asserting that '{}' equals '{}'".format(url, expected))
    assert url == expected
