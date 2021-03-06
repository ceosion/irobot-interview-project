"""Provides a light abstraction to the online Food2Fork API.

See https://www.food2fork.com/about/api for more information.

Author: Alex Richard Ford (arf4188@gmail.com)
"""

import urllib
import urlparse
import colorlog
import requests
import json
import re

# All search requests should be made to the search API URL.
_QUERY_ENDPOINT = "https://www.food2fork.com/api/search"

# All recipe requests should be made to the recipe details API URL.
_RECIPE_DETAILS_ENDPOINT = "https://www.food2fork.com/api/get"

class Food2ForkAPI:
    """Provides a light interface to the online Food2Fork API.
    
    Construct this using the desired API key and it will be used for all
    requests made by this instance.
    """

    _log = None

    def __init__(self, api_key):
        """
        Constructs a new Food2Fork API instance using the provided `api_key`.
        """
        self._api_key = api_key
        self._log = colorlog.getLogger("food_finder.{}".format(__name__))


    def _add_api_key_param(self, params):
        """
        Private function for adding the 'api_key' param correctly.
        """
        params['key'] = self._api_key


    def _add_query_param(self, query, params):
        """
        Private function for adding the 'query' param correctly. The query
        argument to this method should be a list of ingredient strings which
        will be formatted appropriately for the Food2Fork API (comma delimited).
        """
        assert type(query) is list, "`query` argument should be a list, but was: {}".format(query)
        params['q'] = ",".join(query)


    def _add_sort_param(self, sort, params):
        """
        Private function for adding the 'sort' param correctly.
        """
        assert type(sort) is str
        params['sort'] = sort
    
    def _add_recipe_id_param(self, rId, params):
        """
        Private function for adding the 'recipe ID' param correctly.
        """
        assert (type(rId) is str) or (type(rId) is int) or (type(rId) is unicode), "Invalid type for 'rId', received type: {}".format(type(rId))
        params['rId'] = rId
    

    def _build_query_endpoint_url(self,
                                 query=[""],
                                 sort="r",
                                 page=None):
        """
        Private function which builds the URL for a query of the Food2Fork API.
        
        An empty `query` may be specified (as is the default) which will simply
        return the current most popular recipes. The 'sort' query parameter is
        set to default to 'r' which means receipes returned will be sorted by
        social media rating.

        Parameters:
            query (list(str)):  a list of ingredients to search for.
            
            sort (char):        either 'r' or 't' to change how rating is done.
            
            page (int):         page number to get, where each page contains up
                                to 30 recipe results.

        Returns:
            str:    a URL ready for use against the Food2Fork API.
        """
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
        """
        Private function which builds the URL for getting recipe details.
        """
        # initialized 'url' with the correct base URL
        url = _RECIPE_DETAILS_ENDPOINT
        # start with empty dict, fill with needed query params
        params = {}
        self._add_api_key_param(params)
        self._add_recipe_id_param(recipe_id, params)
        encodedParams = urllib.urlencode(params)
        return "{}?{}".format(url, encodedParams)
    

    def query_recipe(self, ingredients):
        """
        Provides the most popular recipe containing all specified ingredients.
        
        Parameters:
            ingredients (list(str)): A list containing one or more of the
                                     ingredients desired.
        
        Returns:
            Recipe (dict): A dictionary representing the Recipe attributes as
                           given by the Food2Fork API, along with a 
                           'missing_ingredients' attribute which is the
                           difference between the specified `ingredients` and
                           the ones needed by the recipe.
                           'None' is returned if there were no results.
        """
        url = self._build_query_endpoint_url(query=ingredients)
        self._log.debug("Built Query URL: {}".format(url))
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError("The response from Food2Fork indicates a "
                               "problem with status code '{}' and message '{}'."
                               .format(response.status_code, response.reason))
        r_json = response.json()
        self._log.debug("r_json = {}".format(r_json))

        # our JSON response should already be sorted by 'popularity' thanks to
        # the sort='r' query param, so as long as we have results, the one we
        # want should just be the first item!
        self._log.debug("r_json['count'] = {}".format(r_json["count"]))
        if r_json["count"] == 0:
            return None

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

        # Once found, we need to display the missing ingredients to the user.
        ingredients_list = r_json["recipe"]["ingredients"]
        self._log.debug("ingredients_list = {}".format(ingredients_list))
        # Subtract list items that contain our input ingredients
        for input_ing in ingredients:
            rexp = re.compile(".*{}.*".format(input_ing), re.IGNORECASE)
            for needed_ing in ingredients_list: 
                if rexp.match(needed_ing):
                    self._log.debug("We have a match!")
                    ingredients_list.remove(needed_ing)
        self._log.debug("Missing ingredients are: {}".format(ingredients_list))

        # Add the missing ingredients determined above as another attribute
        # of the recipe object and return that
        recipe = r_json["recipe"]
        recipe["missing_ingredients"] = ingredients_list
        return recipe
