#!/usr/bin/env python2

"""Unit tests for the food2fork_api module.

Author: Alex Richard Ford (arf4188@gmail.com)
"""

import pytest
import colorlog

from food_finder import food2fork_api

colorlog.basicConfig(level="INFO")
_log = colorlog.getLogger(__name__)

# Attempt to load the Food2Fork API Key from file, if it exists. Otherwise,
# just set the API Key to some fake testing value.
try:
    with open("./secrets/f2f_api_key", "r") as key_file:
        _KEY = key_file.readline().strip()
except:
    _KEY = "fakeFood2ForkApiKey"


def test_build_query_endpoint_url():
    api = food2fork_api.Food2ForkAPI(_KEY)

    # Query endpoint requires a string type, so giving it None or some other
    # type should throw an exception
    with pytest.raises(AssertionError):
        urlActual = api._build_query_endpoint_url(None)
    with pytest.raises(AssertionError):
        urlActual = api._build_query_endpoint_url(5)
    
    # Subtest 2: query may be left empty, which defaults to q="", and is a valid
    # API request.
    urlActual = api._build_query_endpoint_url()
    urlExpected = "{}?key={}".format(food2fork_api._QUERY_ENDPOINT,
                                     _KEY)
    _log.info("Asserting that '{}' equals '{}'".format(urlActual, urlExpected))
    assert urlActual == urlExpected


def test_build_recipe_details_endpoint_url():
    api = food2fork_api.Food2ForkAPI(_KEY)
    urlActual = api._build_recipe_details_endpoint_url()
    urlExpected = "{}?key={}".format(food2fork_api._RECIPE_DETAILS_ENDPOINT,
                                     _KEY)
    _log.info("Asserting that '{}' equals '{}'".format(urlActual, urlExpected))
    assert urlActual == urlExpected


def test_query_recipe():
    # TODO: provide way to mock the API instead of actually doing it!
    api = food2fork_api.Food2ForkAPI(_KEY)
    api.query_recipe(["vanilla", "butter", "cream cheese"])
