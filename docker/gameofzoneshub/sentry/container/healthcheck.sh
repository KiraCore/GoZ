#!/bin/bash

exec 2>&1
set -e
set -x

INIT_START_FILE=$HOME/init_started
INIT_END_FILE=$HOME/init_ended
MAINTENANCE_FILE=$HOME/maintenence

echo "INFO: Healthcheck => START"

if [ "${MAINTENANCE_MODE}" = "true"  ] || [ -f "$MAINTENANCE_FILE" ] ; then
     echo "INFO: Entering maitenance mode!"
     exit 0
fi

if [ -f "$INIT_END_FILE" ]; then
   echo "INFO: Initialization was successfull"
else
   echo "INFO: Pending initialization"
   exit 0
fi

STATUS_GAIA="$(systemctl2 is-active gaiad.service)"
STATUS_LCD="$(systemctl2 is-active lcd.service)"
STATUS_NGINX="$(systemctl2 is-active nginx.service)"

if [ "${STATUS_GAIA}" != "active" ] || [ "${STATUS_LCD}" != "active" ] || [ "${STATUS_NGINX}" != "active" ] ; then
    echo "ERROR: One of the services is NOT active: Gaia($STATUS_GAIA), LCD($STATUS_LCD) or NGINX($STATUS_NGINX)"
    echo ">> Gaia log:"
    tail -n 100 /var/log/journal/gaiad.service.log
    echo ">> LCD log:"
    tail -n 100 /var/log/journal/lcd.service.log
    echo ">> NGINX log:"
    tail -n 100 /var/log/journal/nginx.service.log

CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $INSTANCE_NAME Healthcheck Failure" \
 --body="Attached $(find $SELF_LOGS -type f | wc -l) Log Files" \
 --html="false" \
 --recursive="true" \
 --attachments="$SELF_LOGS,/var/log/journal"
 sleep 150

    exit 1  
else 
    echo "SUCCESS: All services are up and running!"
fi

echo "INFO: Healthcheck => STOP"