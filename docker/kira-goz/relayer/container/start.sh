#!/bin/bash

exec 2>&1
set -e
set -x

echo "Container STARTED"

[ -z "$UPDATE_REPO" ] && UPDATE_REPO="https://github.com/KiraCore/GoZ"
[ -z "$UPDATE_BRANCH" ] && UPDATE_BRANCH="master"
[ -z "$UPDATE_CHECKOUT" ] && UPDATE_CHECKOUT=""

echo "Updating automated execution repo..."
rm -r -f $SELF_UPDATE/tmp
${SELF_SCRIPS}/git-pull-v0.0.1.sh "${UPDATE_REPO}" "${UPDATE_BRANCH}" "${UPDATE_CHECKOUT}" "${SELF_UPDATE}/tmp"
mv $SELF_UPDATE/tmp/* $SELF_UPDATE
chmod -R 777 $SELF_UPDATE

# Rate Limit
sleep 5

if [ "${MAINTENANCE_MODE}" = "true"  ] || [ -f "$MAINTENANCE_FILE" ] ; then
     echo "Entering maitenance mode!"
     /bin/bash # enable user to inspect container while maitenance mode is on
     exit 0
fi

if [ -f "$INIT_END_FILE" ]; then
   echo "on_success() => START" && touch $SUCCESS_START_FILE
   $ON_SUCCESS_SCRIPT $> $SELF_LOGS/success_script_output.log
   echo "on_success() => END" && touch $SUCCESS_END_FILE
   /bin/bash # enable user to inspect container insides after successfull startup
   exit 0
elif [ -f "$INIT_START_FILE" ]; then
   echo "on_failure() => START" && touch $FAILURE_START_FILE
   $ON_FAILURE_SCRIPT $> $SELF_LOGS/failure_script_output.log
   echo "on_failure() => STOP" && touch $FAILURE_END_FILE
   /bin/bash # enable user to inspect container insides after failure
   exit 1
else
   echo "on_init() => START" && touch $INIT_START_FILE
   $ON_INIT_SCRIPT $> $SELF_LOGS/init_script_output.log
   echo "on_init() => STOP" && touch $INIT_END_FILE
fi


#####################################################################









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

chmod 777 -R $RLYS_HOME

rly cfg init || true

# python3 $RELAY_SCRIPS/relay.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $RLYS_HOME "$RLYKEY_MNEMONIC" $BUCKET
# python3 $RELAY_SCRIPS/phase1.py $TESTCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $GOZCHAIN_JSON_PATH "$RLYKEY_MNEMONIC" $BUCKET

echo "Relayer Node init STOP"
/bin/bash
exit 0