Testing
=======

This document extends what is in the [README](../README.md) to further test and validate the function of the application. `pytest` is used as the fundamental Unit Testing library, but it is also used to test larger portions of the code in a semi-automated fashion.

# `pytest` Tips

## Execute a single test function

```bash
pipenv run pytest -s test/food2fork_api.py::test_query_reciper
```

## Get tons more output from tests

```bash
pipenv run pytest -srl --log-level "DEBUG" test/test_food2fork_api.py::test_query_recipe
```

# Test Cases

```bash
pipenv run python food_finder/food_finder.py --debug vanilla butter "cream cheese"
```
