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

STATUS_RELAYER="$(systemctl2 is-active relayer.service)" || STATUS_RELAYER="unknown"

if [ "${STATUS_RELAYER}" != "active" ] ; then
    echo "ERROR: Relayer services is NOT active: Relayer($STATUS_RELAYER)"
    echo ">> Gaia log:"
    tail -n 100 /var/log/journal/relayer.service.log || true

    if [ -f "$EMAIL_SENT" ]; then
        echo "Notification Email was already sent."
    else
        echo "Sending Healthcheck Notification Email..."
        touch $EMAIL_SENT
CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) Healthcheck Raised" \
 --body="[$(date)] Relayer($STATUS_RELAYER) Failed => Attached $(find $SELF_LOGS -type f | wc -l) Log Files" \
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
 --body="[$(date)] Relayer($STATUS_RELAYER) suceeded" \
 --html="false" || true
    fi
    sleep 60 # allow user to grab log output
    rm -f ${SELF_LOGS}/healthcheck_script_output.txt # remove old log to save space
fi

echo "INFO: Healthcheck => STOP"