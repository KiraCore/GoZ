#!/bin/bash

exec 2>&1
set -e
set -x

echo "Node init start."
NODE_KEY_PATH=$HOME/.gaiad/config/node_key.json
VALIDATOR_KEY_PATH=$HOME/.gaiad/config/priv_validator_key.json
APP_TOML_PATH=$HOME/.gaiad/config/app.toml
GENESIS_JSON_PATH=$HOME/.gaiad/config/genesis.json
CONFIG_TOML_PATH=$HOME/.gaiad/config/config.toml

####################

CHAIN_ID=$(cat $BASECHAIN_JSON_PATH | jq -r '."chain-id"')

#rly cfg init
#rly ch add -f $BASECHAIN_JSON_PATH
#
## create a local rly key for the chain
#rly keys add $CHAIN_ID testkey
#
## confiure the chain to use that key by default
#rly ch edit $CHAIN_ID key testkey
#
## initialize the lite client for {{chain_id}}
#rly lite init $CHAIN_ID -f
#
## request funds from the faucet to test it
#rly tst request $CHAIN_ID testkey
#
## lookup balance for the rly key now
#rly q bal $CHAIN_ID
#
#############################################################################
echo "Downloading $REPO from $RELAYER, branch $BRANCH, checkout $CHECKOUT..."

REPO="https://github.com/iqlusioninc/relayer"
BRANCH="master"
CHECKOUT=""
REPO_DIR=/tmp/rly
SOURCE_RLYS_DIR=$REPO_DIR/testnets/relayer-alpha-2
DESTINATION_RLYS_DIR=$HOME/relayers

mkdir -p $(dirname $REPO_DIR)

if [ ! -z "$BRANCH" ]
then
    git clone --branch $BRANCH $REPO $REPO_DIR
else
    git clone $REPO $REPO_DIR
fi

cd $REPO_DIR

if [ ! -z "$CHECKOUT" ]
then
    git checkout $CHECKOUT
fi   

git describe --tags

rm -rfv $DESTINATION_RLYS_DIR
cp -avr $SOURCE_RLYS_DIR $DESTINATION_RLYS_DIR

# do not import already imported base-chain
rm -fv $DESTINATION_RLYS_DIR/$CHAIN_ID.json
chmod 777 -R $DESTINATION_RLYS_DIR
#############################################################################


#python3 $RELAY_SCRIPS/relay.py "$DESTINATION_RLYS_DIR"




#############################################################################
#cd $DESTINATION_RLYS_DIR
#
#
#
#
#
## add all the chain configurations for the testnet (note for some reson if you sprcify path command will fail, you have directly enter the directory)
#rly chains add-dir ./
#
#cd $DESTINATION_RLYS_DIR
#declare -A EXT_CHAINS_ID
#for file in *
#do
#  EXT_CHAIN_ID=$(cat $file | jq -r '."chain-id"')
#  EXT_CHAINS_ID+=("$EXT_CHAINS_ID")
#  EXT_CHAIN_PREFIX=$(cat $file | jq -r '."account-prefix"')
#  EXT_CHAIN_DENOM=$(cat $file | jq -r '."default-denom"')
#  EXT_CHAIN_RPC=$(cat $file | jq -r '."rpc-addr"')
#  EXT_CHAIN_GAS=$(cat $file | jq -r '."gas"')
#  EXT_CHAIN_GAS_PRICES=$(cat $file | jq -r '."gas-prices"')
#  EXT_CHAIN_KEY=$(cat $file | jq -r '."key"')
#  rly ch a -f ./$file
#
#  rly lite init $EXT_CHAIN_ID -f 
#
#  # ensure each chain has its appropriate key...
#  rly keys add $EXT_CHAIN_ID
#
#
#  echo $file
#done






echo "Node init stop."
/bin/bash
exit 0