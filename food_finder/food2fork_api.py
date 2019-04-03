"""Provides a light abstraction to the online Food2Fork API.

See https://www.food2fork.com/about/api for more information.

Author: Alex Richard Ford (arf4188@gmail.com)
"""

import urllib
import urlparse

# All search requests should be made to the search API URL.
_QUERY_ENDPOINT = "https://www.food2fork.com/api/search"

# All recipe requests should be made to the recipe details API URL.
_RECIPE_DETAILS_ENDPOINT = "https://www.food2fork.com/api/get"

class Food2ForkAPI:
    """Provides a light abstraction to the online Food2Fork API.
    
    Construct this using the desired API key and it will be used for all
    requests made by this instance.
    """

    def __init__(self, api_key):
        """Constructs a new Food2Fork API instance using the provided `api_key`."""
        self._api_key = api_key


    def _add_api_key_param(self, params):
        """Private function for adding the 'api_key' param correctly."""
        params['key'] = self._api_key


    def _add_query_param(self, query, params):
        """Private function for adding the 'query' param correctly."""
        assert type(query) is str
        params['q'] = query


    def _add_sort_param(self, sort, params):
        """Private function for adding the 'sort' param correctly."""
        assert type(sort) is str
        params['sort'] = sort
    

    def build_query_endpoint_url(self,
                                 query="",
                                 sort="r",
                                 page=None):
        """Builds a Query Endpoint URL for the Food2Fork API using the provided
        parameter values. An empty query may be specified (as is the default)
        which will simply return the current most popular recipes."""
        url = _QUERY_ENDPOINT
        params = {}
        self._add_api_key_param(params)
        self._add_query_param(query, params)
        self._add_sort_param(sort, params)
        encodedParams = urllib.urlencode(params)
        # TODO: consider using urlparse.urlunparse here?
        return "{}?{}".format(url, encodedParams)
    

    def build_recipe_details_endpoint_url(self,
                                          query=None,
                                          sort=None,
                                          page=None):
        return "{}?key={}".format(_RECIPE_DETAILS_ENDPOINT, self._api_key)
    

    def query_recipe(self, ingredients):
        """Provides the most popular recipe that contains all of the specified
        ingredients."""
        raise NotImplementedError()

