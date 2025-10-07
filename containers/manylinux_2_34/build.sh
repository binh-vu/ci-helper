#!/bin/bash

set -ex

# Description: builds Python's wheels using Maturin.
# The script needs yum or apt
#
# Envionment Arguments: (handled by `args.py`)
#   PYTHON_ROOT_DIR: path to the Python installation. This is used to find the Python interpreters.
#   PYTHON_VERSION: list of Python versions to build for, space separated. Example: "3.8 3.9 3.10"
#   TARGET_PLATFORM: target platform. See https://doc.rust-lang.org/nightly/rustc/platform-support.html

PYTHON_VERSION=$(echo "$PYTHON_VERSION" | tr ' ' ',')

IFS=':' read -a PYTHON_INTERPRETERS < <(python -m wherepy --error-if-not-found --delimiter ' ' --return-execpath --python-versions $PYTHON_VERSION --search-dir "$PYTHON_ROOT_DIR")
if [ ${#PYTHON_INTERPRETERS[@]} -eq 0 ]; then
    echo "No Python found. Did you forget to set the environment variable PYTHON_ROOT_DIR?"
else
    for PYTHON_INTERPRETER in "${PYTHON_INTERPRETERS[@]}"
    do
        echo "Found $PYTHON_INTERPRETER"
    done
fi

PYTHON_INTERPRETERS_JOINED=$(IFS=' ' ; echo "${PYTHON_INTERPRETERS[*]/#/-i }")

maturin build -r -o dist $PYTHON_INTERPRETERS_JOINED --target $TARGET_PLATFORM