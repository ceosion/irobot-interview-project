#!/usr/bin/env python2

import pytest
import colorlog

from food_finder import food2fork_api

colorlog.basicConfig(level="INFO")
_log = colorlog.getLogger(__name__)

_KEY = "5ca1864c5ca1864c5ca1864c"

def test_build_query_endpoint_url():
    api = food2fork_api.Food2ForkAPI(_KEY)
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
