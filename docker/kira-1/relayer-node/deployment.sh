#!/bin/bash

exec 2>&1
set -e
set -x

echo "Building node..."

pip3 install --upgrade setuptools
python3 -m pip install joblib
