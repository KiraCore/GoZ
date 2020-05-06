#!/bin/bash

exec 2>&1
set -e
set -x

[ -z "$SRC_CHAIN_FULL_PATH" ] && SRC_CHAIN_FULL_PATH="$SELF_UPDATE/$SRC_CHAIN_PATH"
[ -z "$DST_CHAIN_FULL_PATH" ] && DST_CHAIN_FULL_PATH="$SELF_UPDATE/$DST_CHAIN_PATH"

SRC_CHAIN_ID=$(cat $SRC_CHAIN_FULL_PATH | jq -r '.["chain-id"]')
DST_CHAIN_ID=$(cat $DST_CHAIN_FULL_PATH | jq -r '.["chain-id"]')

[ -z "$RLY_PATH" ] && RLY_PATH="${SRC_CHAIN_ID}_${DST_CHAIN_ID}"
[ -z "$RLY_KEY_PREFIX" ] && RLY_KEY_PREFIX="default_key"
[ -z "$RLY_FORCE_SHUTDOWN" ] && RLY_FORCE_SHUTDOWN="False"
[ -z "$RLY_TEST" ] && RLY_TEST="true"

echo "Starting relayer service..."
echo "BUCKET: $BUCKET" # kira-core-goz
echo "SRC CHAIN PATH: $SRC_CHAIN_FULL_PATH" # common/configs/kira-1.json
echo "DST CHAIN PATH: $DST_CHAIN_FULL_PATH" # common/configs/goz-hub.json
echo "SRC CHAIN ID: $SRC_CHAIN_ID"
echo "DST CHAIN ID: $DST_CHAIN_ID" 
echo "RLY PATH: $RLY_PATH" # kira-1_goz-hub_phase1
echo "KEY PREFIX: $RLY_KEY_PREFIX" # rly_key_goz
echo "FORCE SHUTDOWN: $RLY_FORCE_SHUTDOWN" # forces shutdown if connection fails
echo "TRUST UPDATE PERIOD: $TRUST_UPDATE_PERIOD" # rly_key_goz

if [ "${MAINTENANCE_MODE}" == "true"  ] || [ -f "$MAINTENANCE_FILE" ] ; then
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

if [ "${RLY_TEST}" == "true"  ] ; then
     echo "INFO: Entering relayer TEST mode"
     python3 $SELF_SCRIPTS/test.py &> $SELF_LOGS/relayer.txt
     sleep 120
     exit 0
else
    echo "INFO: Entering relayer MAINNET mode"
python3 $SELF_SCRIPTS/phase1.py \
 $SRC_CHAIN_FULL_PATH \
 "$RLYKEY_MNEMONIC" \
 $DST_CHAIN_FULL_PATH \
 "$RLYKEY_MNEMONIC" \
 $BUCKET \
 $RLY_FORCE_SHUTDOWN \
 $RLY_PATH \
 $RLY_KEY_PREFIX \
 $TRUST_UPDATE_PERIOD &> $SELF_LOGS/relayer.txt ||  true

CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) FAILURE" \
 --body="[$(date)] ERROR: Phase1 relayer loop was terminated, see details in the attachment." \
 --html="false" \
 --recursive="false" \
 --attachments="$SELF_LOGS/relayer.txt"
    exit 1
fi


# python3 $SELF_SCRIPTS/phase1.py $SELF_UPDATE/common/configs/kira-alpha.json "$RLYKEY_MNEMONIC" $SELF_UPDATE/common/configs/kira-1.json "$RLYKEY_MNEMONIC" $BUCKET False "goz_alpha_1" "test_key_2" 10

