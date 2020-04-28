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


#curl localhost:26657/node_info
#
#rly cfg init
#rly ch add -f {{CHAINID}}.json
#
## create a local rly key for the chain
#rly keys add {{chain_id}} testkey
#
## confiure the chain to use that key by default
#rly ch edit {{chain_id}} key testkey
#
## initialize the lite client for {{chain_id}}
#rly lite init {{chain_id}} -f
#
## request funds from the faucet to test it
#rly tst request {{chain_id}} testkey
#
## you should see a balance for the rly key now
#rly q bal {{chain_id}}


/bin/bash
exit 0