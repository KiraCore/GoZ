#!/bin/bash

exec 2>&1
set -e
set -x

[ -z "$SRC_CHAIN_FULL_PATH" ] && SRC_CHAIN_FULL_PATH="$SELF_UPDATE/$SRC_CHAIN_PATH"
[ -z "$DST_CHAIN_FULL_PATH" ] && DST_CHAIN_FULL_PATH="$SELF_UPDATE/$DST_CHAIN_PATH"

SRC_CHAIN_ID=$(cat $SRC_CHAIN_FULL_PATH | jq -r '.["chain-id"]')
DST_CHAIN_ID=$(cat $DST_CHAIN_FULL_PATH | jq -r '.["chain-id"]')

[ -z "$RLY_PATH" ] && RLY_PATH="${SRC_CHAIN_ID}_${DST_CHAIN_ID}"
[ -z "$RLY_KEY_PREFIX" ] && RLY_KEY_PREFIX="default"

echo "Starting relayer service..."
echo "BUCKET: $BUCKET" # kira-core-goz
echo "SRC CHAIN PATH: $SRC_CHAIN_FULL_PATH" # common/configs/kira-1.json
echo "DST CHAIN PATH: $DST_CHAIN_FULL_PATH" # common/configs/goz-hub.json
echo "SRC CHAIN ID: $SRC_CHAIN_ID"
echo "DST CHAIN ID: $DST_CHAIN_ID" 
echo "RLY PATH: $RLY_PATH" # kira-1_goz-hub_phase1
echo "KEY PREFIX: $RLY_KEY_PREFIX" # rly_key_goz
echo "TRUST UPDATE PERIOD: $TRUST_UPDATE_PERIOD" # rly_key_goz

if [ "${MAINTENANCE_MODE}" = "true"  ] || [ -f "$MAINTENANCE_FILE" ] ; then
     echo "Entering maitenance mode!"
     exit 0
fi

# SRC_JSON_DIR=sys.argv[1]
# SRC_MNEMONIC=sys.argv[2]
# DST_JSON_DIR=sys.argv[3]
# DST_MNEMONIC=sys.argv[4]
# BUCKET=sys.argv[5]
# SHUTDOWN=sys.argv[6]
# PATH=sys.argv[7]
# KEY_PREFIX=sys.argv[8]
# TRUST_UPDATE_PERIOD=sys.argv[9]

python3 $SELF_SCRIPS/test.py &> $SELF_LOGS/relayer.txt

# # python3 $SELF_SCRIPS/phase1.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $HUBCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET False "test-goz" "test_key" 10
# python3 $SELF_UPDATE/common/configs/kira-1.json "$RLYKEY_MNEMONIC" $SELF_UPDATE/common/configs/kira-alpha.json "$RLYKEY_MNEMONIC" $BUCKET "goz-alpha" "test_key" 10


#CDHelper email send \
# --from="noreply@kiracore.com" \
# --to="asmodat@gmail.com" \
# --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) SUCCESS" \
# --body="[$(date)] SUCCESS: Relayer script was executed without errors. Attached you will find relayer log file" \
# --html="false" \
# --recursive="true" \
# --attachments="$SELF_LOGS/relayer.txt"

sleep 100

