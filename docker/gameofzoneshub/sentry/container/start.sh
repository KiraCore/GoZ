#!/bin/bash

exec 2>&1
set -e
set -x

echo "Container STARTED"

INIT_START_FILE=$HOME/init_started
INIT_END_FILE=$HOME/init_ended

[ -z "$UPDATE_REPO" ] && SELF_REPO="https://github.com/KiraCore/GoZ"
[ -z "$UPDATE_BRANCH" ] && SELF_BRANCH="master"
[ -z "$UPDATE_CHECKOUT" ] && SELF_CHECKOUT=""

# Rate Limit
sleep 5

rm -r -f $SELF_UPDATE

${SCRIPTS_DIR}/git-pull-v0.0.1.sh "${UPDATE_REPO}" "${UPDATE_BRANCH}" "${UPDATE_CHECKOUT}" "${SELF_UPDATE}"

chmod -R 777 $SELF_UPDATE

if [ -f "$INIT_END_FILE" ]; then
   echo "on_success() => START"
   $SELF_CONTAINER/on_success.sh
   echo "on_success() => END"
   /bin/bash
elif [ -f "$INIT_START_FILE" ]; then
   echo "on_failure() => START"
   $SELF_CONTAINER/on_failure.sh
   echo "on_failure() => STOP"
   /bin/bash
else
   echo "on_init() => START"
   touch $INIT_START_FILE
   $SELF_CONTAINER/on_init.sh
   touch $INIT_END_FILE
   echo "on_init() => STOP"
fi

