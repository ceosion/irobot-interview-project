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
  - [Coverage](#coverage)
- [Sensitive Data](#sensitive-data)
- [Unaddressed Considerations / Known Problems](#unaddressed-considerations--known-problems)

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

## Coverage

Code coverage can be calculated using:

```bash
pipenv run pytest --cov=food_finder test/
```

See https://docs.pytest.org/en/latest/usage.html for additional information.

# Sensitive Data

The `./secrets` directory should be used to store local files containing any sensitive data. The entire `./secrets/` directory should be excluded from Git, so nothing in this directory should be committed to source control.

The `./secrets/f2f_api_key` file may be used to specify your Food2Fork API key. This file is *optional*, but may be used by the app in different circumstances, if provided.

# Unaddressed Considerations / Known Problems

The following is a list of problems or nuances that apply to this application, which may be fixed in the future if desired:

* The Free-tier of the Food2Fork API is limited to 50 requests per day, and the application has not been tested for when this happens.
    * The code does nothing specific to handle this, and hasn't been tested when this case occurs. With that said, the code does check for a 200 (Success) HTTP status code and should enter a failure path assuming Food2Fork sets this code to something other than 200.

* Sensitive data is allowed in the `./secrets/` directory, which is excluded from Git via the `.gitignore` file. This works, but could still make some folks uncomfortable because a slip-up while modifying `.gitignore` or failure to keep sensitive files isolated within `./secrets/` could leak sensitive data.
    * A trivial refactoring could be done to move all sensitive files out of the applciation's project directory entirely, thus increasing the degree of separation between sensitive and non-sensitive files. (e.g. move `./secrets/` to `../food_finder_secrets/`)
    * The data in `./secrets/` is not shared with the team in an defined way, at the moment. There are many ways to accomplish this, but one possible way is to archive and encrypt the sensitive files and actually commit the encrypted archive to Git. This is especially useful when sharing things like SSL certs and other non-user-specific sensitive files (i.e. not just a single API key file, which is specific to a user anyway). Then, the only thing that needs to be shared with team members is the password used to encrypt the sensitive data archive. (`git-crypt` and other tools can also be used to accomplish similar results.)

  * At least one of the tests requires a valid API key and access to the actual Food2Fork API in order to pass.
      * This makes automated testing more difficult. The API could be mocked in order to provide an isolated/offline environment for the test to run without the need for a real API key or the real Food2Fork API.
