iRobot Interview Project
========================

Leverages the [Food2Fork API](https://www.food2fork.com/about/api) in order to search for recipes based on ingredients the user specifies to a command line application.

See the [Take Home Assignment](./docs/take-home-assignment.md) page for the original assignment text.

**Table of Contents**
- [iRobot Interview Project](#irobot-interview-project)
- [What You'll Need](#what-youll-need)
- [Quick Start](#quick-start)
  - [Using the application](#using-the-application)
  - [Development](#development)
  - [Testing](#testing)
- [Sensitive Data](#sensitive-data)

# What You'll Need

* Python 2.7+
* Pipenv
    * Pipenv can be easily installed using `pip` with this command:
    ```bash
    pip install pipenv
    ```
* A [Food2Fork](https://www.food2fork.com) account, which gives you a free API Key

# Quick Start

## Using the application

This application is a command line-based utility and so you will need to use it from one. Bash is recommended, and the instructions here are written with Bash in mind.

```bash
git clone ...
cd irobot-interview-project
pipenv install
pipenv run python food_finder/food_finder.py --f2f_api_key "enter-your-API-key-here" "ingredient 1" "ingredient 2" ...
```

Built-in help may be accessed with the command:

```bash
pipenv run python food_finder/food_finder.py --help
```

Your Food2Fork API Key may also be placed in a file so you don't have to specify it as an argument to the program. See the [Sensitive Data](#sensitive-data) section for more details.

## Development

This project was developed using [Visual Studio Code](https://code.visualstudio.com). `start-vscode` scripts have been provided which will launch Visual Studio Code (VS Code) in an isolated environment separate from any existing user installation(s). The first step is to ensure you have the needed software: Python 2.7+, Pipenv, and VS Code. Then you can execute the following commands:

```bash
pipenv install --dev
./start-vscode.sh
```

When launching for the first time, you should proceed to install all of the workspace's recommended extensions, as they have been selected specifically for use with this project.

## Testing

Unit tests leverage the [pytest](https://docs.pytest.org/en/latest/) framework. They can be ran after the steps in [Development](##development) with the following:

```bash
pipenv run pytest -s
```

See https://docs.pytest.org/en/latest/usage.html for additional information.

# Sensitive Data

The `./secrets` directory should be used to store local files containing any sensitive data. The entire `./secrets/` directory should be excluded from Git, so nothing in this directory should be committed to source control.

The `./secrets/f2f_api_key` file may be used to specify your Food2Fork API key. This file is *optional*, but may be used by the app in different circumstances, if provided.
