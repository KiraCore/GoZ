#!/bin/bash

exec 2>&1
set -e
set -x

echo "Downloading and installing $REPO in $GAIA, branch $BRANCH, checkout $CHECKOUT..."

mkdir -p $(dirname $GAIA)

if [ ! -z "$BRANCH" ]
then
    git clone --branch $BRANCH $REPO $GAIA
else
    git clone $REPO $GAIA
fi

cd $GAIA

if [ ! -z "$CHECKOUT" ]
then
    git checkout $CHECKOUT
fi   

git describe --tags
make install
