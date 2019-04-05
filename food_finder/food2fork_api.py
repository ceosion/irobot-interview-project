"""Provides a light abstraction to the online Food2Fork API.

See https://www.food2fork.com/about/api for more information.

Author: Alex Richard Ford (arf4188@gmail.com)
"""

import urllib
import urlparse
import colorlog
import requests
import json

# All search requests should be made to the search API URL.
_QUERY_ENDPOINT = "https://www.food2fork.com/api/search"

# All recipe requests should be made to the recipe details API URL.
_RECIPE_DETAILS_ENDPOINT = "https://www.food2fork.com/api/get"

class Food2ForkAPI:
    """Provides a light abstraction to the online Food2Fork API.
    
    Construct this using the desired API key and it will be used for all
    requests made by this instance.
    """

    _log = None

    def __init__(self, api_key):
        """Constructs a new Food2Fork API instance using the provided `api_key`."""
        self._api_key = api_key
        self._log = colorlog.getLogger("food_finder.{}".format(__name__))


    def _add_api_key_param(self, params):
        """Private function for adding the 'api_key' param correctly."""
        params['key'] = self._api_key


    def _add_query_param(self, query, params):
        """Private function for adding the 'query' param correctly. The query
        argument to this method should be a list of ingredient strings which
        will be formatted appropriately for the Food2Fork API (comma delimited)."""
        assert type(query) is list, "`query` argument should be a list, but was: {}".format(query)
        params['q'] = ",".join(query)


    def _add_sort_param(self, sort, params):
        """Private function for adding the 'sort' param correctly."""
        assert type(sort) is str
        params['sort'] = sort
    
    def _add_recipe_id_param(self, rId, params):
        """Private function for adding the 'recipe ID' param correctly."""
        assert (type(rId) is str) or (type(rId) is int) or (type(rId) is unicode), "Invalid type for 'rId', received type: {}".format(type(rId))
        params['rId'] = rId
    

    def _build_query_endpoint_url(self,
                                 query=[""],
                                 sort="r",
                                 page=None):
        """Builds a Query Endpoint URL for the Food2Fork API using the provided
        parameter values. An empty query may be specified (as is the default)
        which will simply return the current most popular recipes. The 'sort'
        query parameter is set to default to 'r' which means receipes returned
        will be sorted by social media rating."""
        # initialize 'url' with the correct base URL
        url = _QUERY_ENDPOINT
        # create empty dict that we will then fill with our URL query parameters
        params = {}
        self._add_api_key_param(params)
        self._add_query_param(query, params)
        self._add_sort_param(sort, params)
        encodedParams = urllib.urlencode(params)
        # TODO: consider using urlparse.urlunparse here?
        return "{}?{}".format(url, encodedParams)
    

    def _build_recipe_details_endpoint_url(self,
                                           recipe_id):
        # initialized 'url' with the correct base URL
        url = _RECIPE_DETAILS_ENDPOINT
        # start with empty dict, fill with needed query params
        params = {}
        self._add_api_key_param(params)
        self._add_recipe_id_param(recipe_id, params)
        encodedParams = urllib.urlencode(params)
        return "{}?{}".format(url, encodedParams)
    

    def query_recipe(self, ingredients):
        """Provides the most popular recipe that contains all of the specified
        ingredients. The `ingredients` argument should be a list containing one
        or more of the ingredients desired."""
        url = self._build_query_endpoint_url(query=ingredients)
        self._log.debug("Built Query URL: {}".format(url))
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("The response from Food2Fork indicates a "
                               "problem with status code '{}' and message '{}'."
                               .format(response.status_code, response.reason))
        r_json = response.json()
        self._log.debug("{}".format(r_json))
        # our JSON response should already be sorted by 'popularity' thanks to
        # the sort='r' query param. Now we just need to find one that contains
        # all of the specified ingreidents.
        self._log.debug("r_json['count'] = {}".format(r_json["count"]))
        selected_recipe = r_json['recipes'][0]
        self._log.debug("selected_recipe = {}".format(selected_recipe))
        
        selected_rId = selected_recipe["recipe_id"]
        self._log.debug("Selected recipe ID is: {}".format(selected_rId))

        # Fetch the full recipe from Food2Fork
        url = self._build_recipe_details_endpoint_url(selected_rId)
        self._log.debug("url = {}".format(url))

        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("The response from Food2Fork's Recipe Endpoint "
                               "indicates a problem with status code '{}' and "
                               "message '{}'.".format(response.status_code,
                               response.reason))
        r_json = response.json()
        self._log.debug("{}".format(r_json))

        # TODO: Once found, we need to display the missing ingredients to the user.
