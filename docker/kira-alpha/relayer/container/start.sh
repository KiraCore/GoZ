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

CHAIN_ID=$(cat $TESTCHAIN_JSON_PATH | jq -r '."chain-id"')
# do not import already imported base-chain
rm -fv $RLYS_HOME/$CHAIN_ID.json
chmod 777 -R $RLYS_HOME

# default cfg dir: $HOME/.relayer/config/config.yml
rly cfg init || true 

# python3 $RELAY_SCRIPS/relay.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $RLYS_HOME "$RLYKEY_MNEMONIC" $BUCKET
# python3 $RELAY_SCRIPS/phase1.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $GOZCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET

# rly pth list
# python3 $RELAY_SCRIPS/phase1.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $HUBCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET

#GOZCHAIN_ID=$(cat $GOZCHAIN_JSON_PATH | jq -r '."chain-id"')
## connect directly and claim goz tokens
#rly ch add -f $GOZCHAIN_JSON_PATH
#rly keys restore $GOZCHAIN_ID prefix_$GOZCHAIN_ID "$RLYKEY_MNEMONIC"
#rly lite init $GOZCHAIN_ID -f
#rly tst request $GOZCHAIN_ID prefix_$GOZCHAIN_ID
#rly q bal $CHAIN_ID
#rly q bal $GOZCHAIN_ID
## connect 2 chains
#rly pth gen $CHAIN_ID transfer $GOZCHAIN_ID transfer ${CHAIN_ID}_${GOZCHAIN_ID}
#rly pth show ${CHAIN_ID}_${GOZCHAIN_ID} -j
#rly tx link ${CHAIN_ID}_${GOZCHAIN_ID}
## send 2kex from alpha to goz
#rly tx transfer $CHAIN_ID $GOZCHAIN_ID 2kex true $(rly ch addr $GOZCHAIN_ID)
## send 1kex from goz to alpha
#rly tx transfer $GOZCHAIN_ID $CHAIN_ID  1kex true $(rly ch addr $CHAIN_ID)
#rly q bal $CHAIN_ID
#rly q bal $GOZCHAIN_ID


echo "Relayer Node init STOP"
/bin/bash
exit 0