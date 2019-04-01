iRobot Interview Project
========================

Leverages the [Food2Fork API](https://www.food2fork.com/about/api) in order to search for recipes based on ingredients the user specifies.

# What You'll Need

* Python 2.7+
* Pipenv
* A Food2Fork account, which gives you a free API Key

# Quick Start

## Using the application

```bash
pipenv install
pipenv run python food_finder/food_finder.py "enter-your-API-key-here" "ingredient 1" "ingredient 2" ...
```

## Development

```bash
pipenv install --dev
./start-vscode.sh
```

## Testing

```bash
pipenv run pytest -s
```

See https://docs.pytest.org/en/latest/usage.html for additional information.
