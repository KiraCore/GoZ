#!/bin/bash

exec 2>&1
set -e
set -x

echo "Relayer Node init START"

CHAIN_ID=$(cat $BASECHAIN_JSON_PATH | jq -r '."chain-id"')
# do not import already imported base-chain
rm -fv $RLYS_HOME/$CHAIN_ID.json
chmod 777 -R $RLYS_HOME

rly cfg init



####################

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
# echo "Downloading $REPO from $RELAYER, branch $BRANCH, checkout $CHECKOUT..."
# 
# 
# SOURCE_RLYS_DIR=$RLY_OUTPUT/testnets/relayer-alpha-2
# DESTINATION_RLYS_DIR=$HOME/relayers
# 
# rm -rfv $DESTINATION_RLYS_DIR
# cp -avr $SOURCE_RLYS_DIR $DESTINATION_RLYS_DIR
# 
# # do not import already imported base-chain
# rm -fv $DESTINATION_RLYS_DIR/$CHAIN_ID.json
# chmod 777 -R $DESTINATION_RLYS_DIR
#############################################################################


#python3 $RELAY_SCRIPS/relay.py "$RLYS_HOME"




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






echo "Relayer Node init STOP"
/bin/bash
exit 0