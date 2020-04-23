#!/bin/bash

exec 2>&1
set -e
set -x

BRANCH="ibc-alpha"
echo "Downloading and installing gaia in $GAIA, branch $BRANCH..."
mkdir -p $(dirname $GAIA) && \
 git clone --branch $BRANCH https://github.com/cosmos/gaia $GAIA && \
 cd $GAIA && \
 make install








