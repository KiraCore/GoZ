#!/bin/bash

exec 2>&1
set -e
set -x

echo "Relayer Node init START"

# setup external ip in the AWSRoute53 registry
INSTANCE_NAME=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/name 2>/dev/null)
INTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/ip 2>/dev/null)
EXTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip 2>/dev/null)

# external variables: ROUTE53_RECORD_NAME, ROUTE53_ZONE, EXTERNAL_IP, ROUTE53_TTY
AWSHelper route53 upsert-a-record --name="$ROUTE53_RECORD_NAME" --zone=$ROUTE53_ZONE --value="$EXTERNAL_IP" --ttl=$ROUTE53_TTY


CHAIN_ID=$(cat $BASECHAIN_JSON_PATH | jq -r '."chain-id"')
# do not import already imported base-chain
rm -fv $RLYS_HOME/$CHAIN_ID.json
chmod 777 -R $RLYS_HOME

# default cfg dir: $HOME/.relayer/config/config.yml
rly cfg init || true 

# python3 $RELAY_SCRIPS/phase1.py "$BASECHAIN_JSON_PATH" "$RLYKEY_MNEMONIC" "$GOZCHAIN_JSON_PATH" "$RLYKEY_MNEMONIC"

<< ////

GOZCHAIN_JSON_PATH=${RELAY_CONFIGS}/kira-1.json

cat > $GOZCHAIN_JSON_PATH << EOL
{
  "key": "faucet",
  "chain-id": "kira-1",
  "rpc-addr": "http://goz.kiraex.com:10001",
  "account-prefix": "cosmos",
  "gas": 200000,
  "gas-prices": "0.025ukex",
  "default-denom": "ukex",
  "trusting-period": "330h"
}
EOL

GOZCHAIN_ID=$(cat $GOZCHAIN_JSON_PATH | jq -r '."chain-id"')

# connect directly and claim goz tokens
rly ch add -f $GOZCHAIN_JSON_PATH
rly keys restore $GOZCHAIN_ID chain_key_$GOZCHAIN_ID "$RLYKEY_MNEMONIC"
rly lite init $GOZCHAIN_ID -f
rly tst request $GOZCHAIN_ID chain_key_$GOZCHAIN_ID

rly q bal $CHAIN_ID
rly q bal $GOZCHAIN_ID

# connect 2 chains
rly pth gen $CHAIN_ID transfer $GOZCHAIN_ID transfer ${CHAIN_ID}_${GOZCHAIN_ID}
rly pth show ${CHAIN_ID}_${GOZCHAIN_ID} -j
rly tx link ${CHAIN_ID}_${GOZCHAIN_ID}

# send 2kex from alpha to goz
rly tx transfer $CHAIN_ID $GOZCHAIN_ID 2kex true $(rly ch addr $GOZCHAIN_ID)
# send 1kex from goz to alpha
rly tx transfer $GOZCHAIN_ID $CHAIN_ID  1kex true $(rly ch addr $CHAIN_ID)

rly q bal $CHAIN_ID
rly q bal $GOZCHAIN_ID
////


rly pth gen $CHAIN_ID transfer $GOZCHAIN_ID transfer ${CHAIN_ID}_${GOZCHAIN_ID}
rly tx link ${CHAIN_ID}_${GOZCHAIN_ID}

rly q bal chainylira
rly pth gen $CHAIN_ID transfer chainylira transfer ${CHAIN_ID}_chainylira
rly tx link ${CHAIN_ID}_chainylira

Balance of chain_key_ 
[{'denom': 'nickel', 'amount': '1000000'}]
Connecting kira-alpha and chainylira...

rly pth gen kira-alpha transfer hashquarkchain transfer kira-alpha_hashquarkchain
rly tx link kira-alpha_hashquarkchain

rly transact link kira-alpha_chainylira -o=600s

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
#####################

#python3 $RELAY_SCRIPS/relay.py "$RLYS_HOME"



echo "Relayer Node init STOP"
/bin/bash
exit 0