#!/bin/bash

exec 2>&1
set -e
set -x

EMAIL_SENT=$HOME/email_sent

echo "INFO: Healthcheck => START"
sleep 60 # rate limit

if [ "${MAINTENANCE_MODE}" == "true"  ] || [ -f "$MAINTENANCE_FILE" ] ; then
     echo "INFO: Entering maitenance mode!"
     exit 0
fi

# cleanup large files
find "/var/log/journal" -type f -size +256k -exec truncate --size=128k "{}" ";"
find "$SELF_LOGS" -type f -size +256k -exec truncate --size=128k "{}" ";"

if [ -f "$INIT_END_FILE" ]; then
   echo "INFO: Initialization was successfull"
else
   echo "INFO: Pending initialization"
   exit 0
fi

STATUS_RELAYER="$(systemctl2 is-active relayer.service)" || STATUS_RELAYER="unknown"

if [ "${STATUS_RELAYER}" != "active" ] ; then
    echo "ERROR: Relayer service is NOT active: Relayer($STATUS_RELAYER)"

    if [ "${STATUS_RELAYER}" != "active" ] ; then
        echo ">> Relayer log:"
        tail -n 100 /var/log/journal/relayer.service.log || true
        systemctl2 restart relayer || systemctl2 status relayer || echo "Failed to re-start relayer service" || true
    fi

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
    exit 1  
else 
    echo "SUCCESS: Healthcheck PASSED"
    if [ -f "$EMAIL_SENT" ]; then
        echo "INFO: Sending confirmation email, that service recovered!"
        rm -f $EMAIL_SENT # if email was sent then remove and send new one
CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) Healthcheck Rerovered" \
 --body="[$(date)] Relayer($STATUS_RELAYER) suceeded" \
 --html="false" || true
    fi
fi

echo "INFO: Healthcheck => STOP"