#!/bin/bash

exec 2>&1
set -e
set -x

echo "Building node..."

echo "Updating Python Tools..."
pip3 install --upgrade setuptools
pip3 install 'python-dateutil>=2.7.0,<2.9.9' --force-reinstall
python3 -m pip install joblib
pip3 install --upgrade requests

echo "Updating Asmodat Automation helper tools..."
${SELF_SCRIPTS}/awshelper-update-v0.0.1.sh "v0.12.0"
AWSHelper version

${SELF_SCRIPTS}/cdhelper-update-v0.0.1.sh "v0.6.0"
CDHelper version