#!/bin/bash

exec 2>&1
set -e
set -x

touch $MAINTENANCE_FILE # notify entire environment to halt

systemctl2 stop gaiad
systemctl2 stop lcd
systemctl2 stop nginx

# TODO: send email fail to init notification

INSTANCE_NAME=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/name 2>/dev/null)

CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $INSTANCE_NAME Failed to Initalize" \
 --body="Log files in the attachement" \
 --html="false" \
 --recursive="true" \
 --attachments="$SELF_LOGS"

