#!/bin/bash

exec 2>&1
set -e
set -x

echo "Container STARTED"

[ -z "$UPDATE_REPO" ] && UPDATE_REPO="https://github.com/KiraCore/GoZ"
[ -z "$UPDATE_BRANCH" ] && UPDATE_BRANCH="master"
[ -z "$UPDATE_CHECKOUT" ] && UPDATE_CHECKOUT=""

echo "Updating automated execution repo..."
rm -r -f $SELF_UPDATE_TMP
${SELF_SCRIPTS}/git-pull-v0.0.1.sh "${UPDATE_REPO}" "${UPDATE_BRANCH}" "${UPDATE_CHECKOUT}" "${SELF_UPDATE_TMP}"
rsync -ra $SELF_UPDATE_TMP/* $SELF_UPDATE
chmod -R 777 $SELF_UPDATE

# Rate Limit
sleep 5

if [ "${MAINTENANCE_MODE}" == "true"  ] || [ -f "$MAINTENANCE_FILE" ] ; then
     echo "Entering maitenance mode!"
     /bin/bash # enable user to inspect container while maitenance mode is on
     exit 0
fi

if [ -f "$INIT_END_FILE" ]; then
   echo "on_success() => START" && touch $SUCCESS_START_FILE
   $ON_SUCCESS_SCRIPT $> $SELF_LOGS/success_script_output.txt
   echo "on_success() => END" && touch $SUCCESS_END_FILE
   /bin/bash # enable user to inspect container insides after successfull startup
   exit 0
elif [ -f "$INIT_START_FILE" ]; then
   echo "on_failure() => START" && touch $FAILURE_START_FILE
   $ON_FAILURE_SCRIPT $> $SELF_LOGS/failure_script_output.txt
   echo "on_failure() => STOP" && touch $FAILURE_END_FILE
   /bin/bash # enable user to inspect container insides after failure
   exit 1
else
   echo "on_init() => START" && touch $INIT_START_FILE
   $ON_INIT_SCRIPT $> $SELF_LOGS/init_script_output.txt
   echo "on_init() => STOP" && touch $INIT_END_FILE
fi
