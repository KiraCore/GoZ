#!/bin/bash

exec 2>&1
set -e
set -x



echo "Fetching external IP of the current instance"
EXTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip 2>/dev/null)
   
# external variables: ROUTE53_RECORD_NAME, ROUTE53_ZONE, EXTERNAL_IP, ROUTE53_TTY
echo "Assigning $ROUTE53_RECORD_NAME DNS in the zone $ROUTE53_ZONE to $EXTERNAL_IP with ${ROUTE53_TTY}s TTY"
AWSHelper route53 upsert-a-record --name="$ROUTE53_RECORD_NAME" --zone=$ROUTE53_ZONE --value="$EXTERNAL_IP" --ttl=$ROUTE53_TTY








