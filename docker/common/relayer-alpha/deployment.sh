#!/bin/bash

exec 2>&1
set -e
set -x

echo "Downloading and installing $REPO in $RELAYER, branch $BRANCH, checkout $CHECKOUT..."

mkdir -p $(dirname $RELAYER)

if [ ! -z "$BRANCH" ]
then
    git clone --branch $BRANCH $REPO $RELAYER
else
    git clone $REPO $RELAYER
fi

cd $RELAYER

if [ ! -z "$CHECKOUT" ]
then
    git checkout $CHECKOUT
fi   

git describe --tags
make install
