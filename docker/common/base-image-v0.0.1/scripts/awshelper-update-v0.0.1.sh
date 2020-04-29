#!/bin/bash

exec 2>&1
set -e
set -x

VERSION=$1

echo "------------------------------------------------"
echo " STARTED: AWSHELPER UPDATE v0.0.1"
echo "------------------------------------------------"
echo "OLD-VERSION: $AWSHelperVersion"
echo "NEW-VERSION: $VERSION"
echo "------------------------------------------------"

if [ "$VERSION" == "$AWSHelperVersion" ]; then
    echo "AWSHelper will not be updated, new and old versions are the same."
    exit 0
else
    echo "New version detected, installing..."
fi

cd /usr/local/src
rm -f -v ./AWSHelper-linux-x64.zip
wget https://github.com/asmodat/AWSHelper/releases/download/$VERSION/AWSHelper-linux-x64.zip
rm -rfv /usr/local/bin/AWSHelper
unzip AWSHelper-linux-x64.zip -d /usr/local/bin/AWSHelper
chmod -Rv 777 /usr/local/bin/AWSHelper

AWSHelper version

echo "------------------------------------------------"
echo " FINISHED: AWSHELPER UPDATE v0.0.1"
echo "------------------------------------------------"
