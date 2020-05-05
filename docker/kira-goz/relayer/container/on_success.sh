#!/bin/bash

exec 2>&1
set -e
set -x

echo "Fetching external IP of the current instance"
EXTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip 2>/dev/null)
echo "Assigning '$ROUTE53_RECORD_NAME' DNS name in the zone $ROUTE53_ZONE to $EXTERNAL_IP with ${ROUTE53_TTY}s TTY"
AWSHelper route53 upsert-a-record --name="$ROUTE53_RECORD_NAME" --zone=$ROUTE53_ZONE --value="$EXTERNAL_IP" --ttl=$ROUTE53_TTY

echo "Fetching internal IP of the current instance"
INTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/ip 2>/dev/null)
echo "Assigning 'internal-$ROUTE53_RECORD_NAME' DNS name in the zone $ROUTE53_ZONE to $EXTERNAL_IP with ${ROUTE53_TTY}s TTY"
AWSHelper route53 upsert-a-record --name="internal-$ROUTE53_RECORD_NAME" --zone=$ROUTE53_ZONE --value="$INTERNAL_IP" --ttl=$ROUTE53_TTY

echo "Restarting services..."
systemctl2 restart relayer || systemctl2 status relayer.service || echo "Failed to re-start relayer service" && echo "$(cat /etc/systemd/system/relayer.service)" || true



