#!/bin/bash

exec 2>&1
set -e
set -x

echo "Building node..."

pip3 install --upgrade setuptools
pip3 install 'python-dateutil>=2.7.0,<2.9.9' --force-reinstall
python3 -m pip install joblib