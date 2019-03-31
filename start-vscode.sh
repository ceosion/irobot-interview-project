#!/bin/bash

###
# Linux script for launching Visual Studio Code in an
# isolated/independent environment. This means that the user data
# and extensions are separate from the main user instance that is
# normally launched when you simply type 'code'.
#
# You can open files in this specific isolated environment by
# using this script again... e.g.
#   ./start-vscode.sh file1 file2
#
# Author: Alex Richard Ford (arf4188@gmail.com)
# Website: http://www.alexrichardford.com
# License: MIT License
###

function error() {
    EXIT_CODE="$1"
    ERROR_MSG="$2"
    echo -e "[ \e[31mERRO\e[0m ] ${ERROR_MSG}"
    exit ${EXIT_CODE}
}

THIS_SCRIPT="$(realpath $0)"
PROJECT_DIR="$(dirname ${THIS_SCRIPT})"
PROJECT_NAME="$(basename ${PROJECT_DIR})"

which code >/dev/null 2>&1
if [ $? != 0 ]; then
    error 1 "Visual Studio Code not found on the path!"
fi

CWD="$(pwd)"
cd "${PROJECT_DIR}"

# Rename default workspace file to match directory name
if [ -e "./default.code-workspace" ]; then
    mv ./default.code-workspace ${PROJECT_NAME}.code-workspace
fi

ls ${PROJECT_NAME}.code-workspace >/dev/null 2>&1
if [ $? != 0 ]; then
    error 1 "can't continue: ${PROJECT_NAME}.code-workspace doesn't exist!"
fi

# TODO: possible to look at code-workspace file and install the list of extensions from there?

code --verbose \
     --user-data-dir "./.vscode/user-data/" \
     --extensions-dir "./.vscode/extensions/" \
     "./${PROJECT_NAME}.code-workspace" \
     $@

cd "${CWD}"

