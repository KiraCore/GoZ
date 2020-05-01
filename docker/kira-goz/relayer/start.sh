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

#python3 $RELAY_SCRIPS/relay.py "$RLYS_HOME"

echo "Relayer Node init STOP"
/bin/bash
exit 0