#!/bin/bash

exec 2>&1
set -e
set -x

touch $MAINTENANCE_FILE # notify entire environment to halt

systemctl2 stop faucet || systemctl2 status faucet || true

# TODO: send email fail to init notification

CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) Failed to Initalize" \
 --body="[$(date)] Attached $(find $SELF_LOGS -type f | wc -l) Log Files" \
 --html="false" \
 --recursive="true" \
 --attachments="$SELF_LOGS,/var/log/journal"

