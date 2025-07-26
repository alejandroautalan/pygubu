#!/bin/bash
#
# usage: ./run.sh command [argument ...]
#
# Commands used during development / CI.
# Also, executable documentation for project dev practices.
#
# See https://death.andgravity.com/run-sh
# for an explanation of how it works and why it's useful.


# First, set up the environment.
# (Check the notes at the end when changing this.)

set -o nounset
set -o pipefail
set -o errexit

# Change the current directory to the project root.
PROJECT_ROOT=${0%/*}
if [[ $0 != $PROJECT_ROOT && $PROJECT_ROOT != "" ]]; then
    cd "$PROJECT_ROOT"
fi
readonly PROJECT_ROOT=$( pwd )

# Store the absolute path to this script (useful for recursion).
readonly SCRIPT="$PROJECT_ROOT/$( basename "$0" )"



# Commands follow.

# System requirements:
# apt install python3-build twine
#

python3bin=$(which python3)

function tests {
    cd tests; $python3bin -W default -m unittest -v; cd ..;
}

function build {
    $python3bin -m build
}

function upload_testpypi {
    build && \
    twine upload --skip-existing -r test_pygubu dist/*
}

function upload_pypi {
    build && \
    twine upload --skip-existing -r pygubu_project dist/*
}

# Commands end. Dispatch to command.

if [[ -z "$@" ]]; then
  echo "No subcommand provided."
  echo "Available commands:"
  compgen -A function | sed -e $'s/^/    /'
  exit 1
else
  "$@"
fi


# Some dev notes for this script.
#
# The commands *require*:
#
# * The current working directory is the project root.
# * The shell options and globals are set as they are.
#
# Inspired by http://www.oilshell.org/blog/2020/02/good-parts-sketch.html
#
