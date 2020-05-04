#!/bin/bash

exec 2>&1
set -e
set -x

SRC_PATH="$SELF_UPDATE/$SRC_CHAIN_PATH"
DST_PATH="$SELF_UPDATE/$DST_CHAIN_PATH"

echo "Starting relayer service..."
echo "BUCKET: $BUCKET" # kira-core-goz
echo "SRC CHAIN PATH: $SRC_PATH" # common/configs/kira-1.json
echo "DST CHAIN PATH: $DST_PATH" # common/configs/goz-hub.json
echo "RLY PATH: $RLY_PATH" # kira-1_goz-hub_phase1
echo "KEY PREFIX: $RLY_KEY_PREFIX" # rly_key_goz

if [ "${MAINTENANCE_MODE}" = "true"  ] || [ -f "$MAINTENANCE_FILE" ] ; then
     echo "Entering maitenance mode!"
     exit 0
fi

python3 $SELF_SCRIPS/test.py &> $SELF_LOGS/relayer.txt

#CDHelper email send \
# --from="noreply@kiracore.com" \
# --to="asmodat@gmail.com" \
# --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) SUCCESS" \
# --body="[$(date)] SUCCESS: Relayer script was executed without errors. Attached you will find relayer log file" \
# --html="false" \
# --recursive="true" \
# --attachments="$SELF_LOGS/relayer.txt"

sleep 100

