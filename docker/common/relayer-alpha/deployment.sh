#!/bin/bash

exec 2>&1
set -e
set -x

PROFILE_PATH="/etc/profile"
echo "Adding variables to PATH in $PROFILE_PATH..."

echo "RELAYER=\$GOPATH/src/github.com/iqlusioninc/relayer" >> $PROFILE_PATH

$PROFILE_PATH

BRANCH="master"
echo "Downloading and installing relayer in $RELAYER, branch $BRANCH..."
mkdir -p $(dirname $RELAYER) && \
 git clone --branch $BRANCH https://github.com/iqlusioninc/relayer $RELAYER && \
 cd $RELAYER && \
 make install

DENOM=ukex
CHAINID=kira-1
DOMAIN=kiraex.com
RLYKEY=faucet
