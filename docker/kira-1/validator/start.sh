#!/bin/bash

exec 2>&1
set -e
set -x

echo "Staring node..."
NODE_KEY_PATH=$HOME/.gaiad/config/node_key.json
VALIDATOR_KEY_PATH=$HOME/.gaiad/config/priv_validator_key.json
APP_TOML_PATH=$HOME/.gaiad/config/app.toml
GENESIS_JSON_PATH=$HOME/.gaiad/config/genesis.json
CONFIG_TOML_PATH=$HOME/.gaiad/config/config.toml

##{
##    "key": "faucet",
##    "chain-id": "kira-1",
##    "rpc-addr": "http://goz.kiraex.com:26657",
##    "account-prefix": "cosmos",
##    "gas": 200000,
##    "gas-prices": "0.025ukex",
##    "default-denom": "ukex",
##    "trusting-period": "330h"
##}

# external variables RLYKEY_ADDRESS, RLYKEY_MNEMONIC

cd

if [ -f "$CHAINID.json" ]; then
   echo "Validator node was already initalized."
   exit 0
fi

rly config init
echo "{\"key\":\"$RLYKEY\",\"chain-id\":\"$CHAINID\",\"rpc-addr\":\"http://$DOMAIN:26657\",\"account-prefix\":\"cosmos\",\"gas\":200000,\"gas-prices\":\"0.025$DENOM\",\"default-denom\":\"$DENOM\",\"trusting-period\":\"330h\"}" > $CHAINID.json
# NOTE: you will want to save the content from this JSON file
rly chains add -f $CHAINID.json
rly keys restore $CHAINID $RLYKEY "$RLYKEY_MNEMONIC"
rly keys list $CHAINID

gaiad init --chain-id $CHAINID $CHAINID

# external variables: NODE_ID, NODE_KEY, VALIDATOR_KEY
# setup node key
rm -f -v $NODE_KEY_PATH && \
 echo $NODE_KEY >> $NODE_KEY_PATH
# setup validator signing key
rm -f -v $VALIDATOR_KEY_PATH && \
 echo $VALIDATOR_KEY >> $VALIDATOR_KEY_PATH

# NOTE: ensure that the gaia rpc is open to all connections
sed -i 's#tcp://127.0.0.1:26657#tcp://0.0.0.0:26657#g' $CONFIG_TOML_PATH
sed -i "s/stake/$DENOM/g" $GENESIS_JSON_PATH
sed -i 's/pruning = "syncable"/pruning = "nothing"/g' $APP_TOML_PATH

# external variables: KEYRINGPASS, PASSPHRASE
#gaiacli keys import validator $VALIDATOR_SELF_KEY_PATH << EOF
#$KEYRINGPASS
#$PASSPHRASE
#EOF

#echo ${PASSPHRASE} | gaiacli keys list

