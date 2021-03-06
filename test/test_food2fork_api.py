#!/usr/bin/env python2

"""Unit tests for the food2fork_api module.

Author: Alex Richard Ford (arf4188@gmail.com)
"""

import pytest
import colorlog
import urlparse

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
    
    # Now let's test for the nominal/expected behavior
    urlActual = api._build_query_endpoint_url()
    
    parseResult = urlparse.urlparse(urlActual)
    _log.debug("parseResult = {}".format(parseResult))
    queryParams = urlparse.parse_qs(parseResult.query)
    _log.debug("queryParams = {}".format(queryParams))
    assert queryParams.has_key("key"), \
        "Missing API Key (query param 'key')!"
    assert queryParams["key"][0] == _KEY, \
        "API Key did not match what was provided!"
    assert queryParams.has_key("sort"), \
        "Missing query param 'sort'!"
    assert queryParams["sort"][0] == "r", \
        "Query param 'sort' did not have expected value 'r'!"


def test_build_recipe_details_endpoint_url():
    api = food2fork_api.Food2ForkAPI(_KEY)
    rId = "12345"
    urlActual = api._build_recipe_details_endpoint_url(rId)

    parseResult = urlparse.urlparse(urlActual)
    _log.debug("parseResult = {}".format(parseResult))
    queryParams = urlparse.parse_qs(parseResult.query)
    _log.debug("queryParams = {}".format(queryParams))

    assert queryParams.has_key("key"), \
        "Missing API Key (query param 'key')!"
    assert queryParams["key"][0] == _KEY, \
        "API Key did not match what was provided!"
    assert queryParams.has_key("rId"), \
        "Missing 'recipe id' in generated URL!"
    assert queryParams["rId"][0] == rId, \
        "Query param 'recipe id' did not have expected value '{}'".format(rId)


def test_query_recipe():
    # TODO: provide way to mock the API instead of actually doing it against
    # the real one!
    api = food2fork_api.Food2ForkAPI(_KEY)
    # TODO: the following test only works if we always get the 
    # "Guiness Chocolate Cheesecake" as the actualRecipe... this is fine for
    # now, but for long term, this isn't a good assumption... besides, mocking
    # the API (see the TODO above) could take care of this problem!
    actualRecipe = api.query_recipe(["vanilla", "butter", "cream cheese"])
    _log.debug("recipe = {}".format(actualRecipe))
    full_ingredients_list = [
        "1 cup graham cracker crumbs",
        "2 tablespoons cocoa powder",
        "1 tablespoon sugar",
        "12 ounces dark chocolate, chopped",
        "2 tablespoons heavy cream",
        "1 cup sugar",
        "1/2 cup sour cream",
        "3 eggs",
        "3/4 cup Guinness\n"
    ]
    assert actualRecipe["ingredients"] == full_ingredients_list
    missing_ingredients_list = [
        "1 cup graham cracker crumbs",
        "2 tablespoons cocoa powder",
        "1 tablespoon sugar",
        "12 ounces dark chocolate, chopped",
        "2 tablespoons heavy cream",
        "1 cup sugar",
        "1/2 cup sour cream",
        "3 eggs",
        "3/4 cup Guinness\n"
    ]
    assert actualRecipe["missing_ingredients"] == missing_ingredients_list

