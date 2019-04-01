#!/usr/bin/env python2

"""Provides a light abstraction to the Food2Fork API.

See https://www.food2fork.com/about/api for more information.

Author: Alex Richard Ford (arf4188@gmail.com)
"""

# All search requests should be made to the search API URL.
_QUERY_ENDPOINT = "https://www.food2fork.com/api/search"

# All recipe requests should be made to the recipe details API URL.
_RECIPE_DETAILS_ENDPOINT = "https://www.food2fork.com/api/get"

class Food2ForkAPI:
    """Provides a light abstraction to the Food2Fork API."""


    def __init__(self, api_key):
        self.api_key = api_key
    
    def build_query_endpoint_url(self,
                                 query=None,
                                 sort=None,
                                 page=None):
        return "{}?key={}".format(_QUERY_ENDPOINT, self.api_key)
    
    def build_recipe_details_endpoint_url(self,
                                          query=None,
                                          sort=None,
                                          page=None):
        return "{}?key={}".format(_RECIPE_DETAILS_ENDPOINT, self.api_key)

