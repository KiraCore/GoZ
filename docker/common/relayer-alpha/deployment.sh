#!/bin/bash

exec 2>&1
set -e
set -x

echo "Downloading and installing relayer in $RELAYER, branch $BRANCH..."
mkdir -p $(dirname $RELAYER) && \
 git clone --branch $BRANCH https://github.com/iqlusioninc/relayer $RELAYER && \
 cd $RELAYER && \
 make install
 
