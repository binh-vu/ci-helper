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
PYTHON_INTERPRETERS=$(python -m wherepy --error-if-not-found --delimiter ' ' --return-execpath --python-versions $PYTHON_VERSION --search-dir "$PYTHON_ROOT_DIR")

maturin build -r -o dist -i $PYTHON_INTERPRETERS --target $TARGET_PLATFORM