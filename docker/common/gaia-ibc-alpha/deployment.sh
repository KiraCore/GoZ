#!/bin/bash

exec 2>&1
set -e
set -x

echo "Installing latest go version https://golang.org/doc/install ..."

GO_VERSION="1.14"
wget https://dl.google.com/go/go$GO_VERSION.linux-amd64.tar.gz
tar -C /usr/local -xzf go$GO_VERSION.linux-amd64.tar.gz

PROFILE_PATH="/etc/profile"
BASHRC_PATH=$HOME/.bashrc
echo "Adding GOPATH, GOROOT, GOBIN and both to PATH in $PROFILE_PATH and $BASHRC_PATH..."

echo "" >> $PROFILE_PATH
echo "GOROOT=/usr/local/go" >> $PROFILE_PATH
echo "GOPATH=$HOME/go" >> $PROFILE_PATH
echo "GOBIN=$GOPATH/bin" >> $PROFILE_PATH
echo "PATH=$PATH:/usr/local/go/bin:$GOBIN" >> $PROFILE_PATH
echo "GAIA=\$GOPATH/src/github.com/cosmos/gaia" >> $PROFILE_PATH
echo "RUSTFLAGS=-Ctarget-feature=+aes,+ssse3" >> $PROFILE_PATH

echo "source $PROFILE_PATH" >> $BASHRC_PATH
#echo "source /home/ubuntu/.cargo/env" >> $BASHRC_PATH

$PROFILE_PATH

BRANCH="ibc-alpha"
echo "Downloading and installing gaia in $GAIA, branch $BRANCH..."
mkdir -p $(dirname $GAIA) && \
 git clone --branch $BRANCH https://github.com/cosmos/gaia $GAIA && \
 cd $GAIA && \
 make install








