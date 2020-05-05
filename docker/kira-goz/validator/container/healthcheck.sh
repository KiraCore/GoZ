#!/bin/bash

exec 2>&1
set -e
set -x

EMAIL_SENT=$HOME/email_sent

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

STATUS_NGINX="$(systemctl2 is-active nginx.service && echo 'unknown')" || true
STATUS_GAIA="$(systemctl2 is-active gaiad.service && echo 'unknown')" || true
STATUS_LCD="$(systemctl2 is-active lcd.service && echo 'unknown')" || true
STATUS_FAUCET="$(systemctl2 is-active faucet.service && echo 'unknown')" || true

if [ "${STATUS_GAIA}" != "active" ] || [ "${STATUS_LCD}" != "active" ] || [ "${STATUS_NGINX}" != "active" ] ; then
    echo "ERROR: One of the services is NOT active: Gaia($STATUS_GAIA), LCD($STATUS_LCD) or NGINX($STATUS_NGINX)"
    echo ">> Gaia log:"
    tail -n 100 /var/log/journal/gaiad.service.log
    echo ">> LCD log:"
    tail -n 100 /var/log/journal/lcd.service.log
    echo ">> NGINX log:"
    tail -n 100 /var/log/journal/nginx.service.log
    echo ">> Faucet log:"
    tail -n 100 /var/log/journal/faucet.service.log

    if [ -f "$EMAIL_SENT" ]; then
        echo "Notification Email was already sent."
    else
        echo "Sending Healthcheck Notification Email..."
        touch $EMAIL_SENT
CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) Healthcheck Raised" \
 --body="[$(date)] Gaia($STATUS_GAIA), Faucet($STATUS_FAUCET) LCD($STATUS_LCD) or NGINX($STATUS_NGINX) Failed => Attached $(find $SELF_LOGS -type f | wc -l) Log Files" \
 --html="false" \
 --recursive="true" \
 --attachments="$SELF_LOGS,/var/log/journal"
        fi
    rm -f ${SELF_LOGS}/healthcheck_script_output.txt # remove old log to save space
    exit 1  
else 
    echo "SUCCESS: All services are up and running!"
    if [ -f "$EMAIL_SENT" ]; then
        # if email was sent then remove and send new one
        rm -f $EMAIL_SENT
CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) Healthcheck Rerovered" \
 --body="[$(date)] Gaia($STATUS_GAIA), Faucet($STATUS_FAUCET), LCD($STATUS_LCD) and NGINX($STATUS_NGINX) suceeded" \
 --html="false" || true
    fi
    rm -f ${SELF_LOGS}/healthcheck_script_output.txt # remove old log to save space
fi

echo "INFO: Healthcheck => STOP"