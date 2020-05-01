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

rly cfg init || true


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