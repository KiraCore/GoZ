#!/bin/bash

exec 2>&1
set -e
set -x

EMAIL_SENT=$HOME/email_sent

echo "INFO: Healthcheck => START"
sleep 60 # rate limit

if [ "${MAINTENANCE_MODE}" = "true"  ] || [ -f "$MAINTENANCE_FILE" ] ; then
     echo "INFO: Entering maitenance mode!"
     exit 0
fi

# cleanup large files
find $SELF_LOGS -type f -size +128k -exec rm -vf {} +\
find "/var/log/journal" -type f -size +128k -exec rm -vf {} +\

if [ -f "$INIT_END_FILE" ]; then
   echo "INFO: Initialization was successfull"
else
   echo "INFO: Pending initialization"
   exit 0
fi

RPC_STATUS="$(curl 127.0.0.1:$RPC_PROXY_PORT/status 2>/dev/null)" || RPC_STATUS="{}"
RPC_CATCHING_UP="$(echo $RPC_STATUS | jq -r '.result.sync_info.catching_up')" || RPC_CATCHING_UP="true"
STATUS_NGINX="$(systemctl2 is-active nginx.service)" || STATUS_RELAYER="unknown"
STATUS_GAIA="$(systemctl2 is-active gaiad.service)" || STATUS_GAIA="unknown"
STATUS_LCD="$(systemctl2 is-active lcd.service)" || STATUS_LCD="unknown"

if [ "${STATUS_GAIA}" != "active" ] || [ "${STATUS_LCD}" != "active" ] || [ "${STATUS_NGINX}" != "active" ] ; then
    echo "ERROR: One of the services is NOT active or RPC is catching up: Gaia($STATUS_GAIA), RPC Catching Up ($RPC_CATCHING_UP), LCD($STATUS_LCD) or NGINX($STATUS_NGINX)"
    
    if [ "${STATUS_GAIA}" != "active" ] ; then
        echo ">> Gaia log:"
        tail -n 100 /var/log/journal/gaiad.service.log || true
        systemctl2 restart gaiad || systemctl2 status gaiad.service || echo "Failed to re-start gaiad service" || true
    fi

    if [ "${STATUS_LCD}" != "active" ]  ; then
        echo ">> LCD log:"
        tail -n 100 /var/log/journal/lcd.service.log || true
        systemctl2 restart lcd || systemctl2 status lcd.service || echo "Failed to re-start lcd service" || true
    fi

    if [ "${STATUS_NGINX}" != "active" ]  ; then
        echo ">> NGINX log:"
        tail -n 100 /var/log/journal/nginx.service.log || true
        systemctl2 restart nginx || systemctl2 status nginx.service || echo "Failed to re-start nginx service" || true
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
 --body="[$(date)] Gaia($STATUS_GAIA), RPC Catching Up ($RPC_CATCHING_UP), LCD($STATUS_LCD) or NGINX($STATUS_NGINX) Failed => Attached $(find $SELF_LOGS -type f | wc -l) Log Files => RPC Status: $RPC_STATUS" \
 --html="false" \
 --recursive="true" \
 --attachments="$SELF_LOGS,/var/log/journal"
        sleep 120 # rate limit
        rm -f ${SELF_LOGS}/healthcheck_script_output.txt # remove old log to save space
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
 --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) Healthcheck Passed" \
 --body="[$(date)] Gaia($STATUS_GAIA), LCD($STATUS_LCD) and NGINX($STATUS_NGINX) suceeded, RPC Status: $RPC_STATUS" \
 --html="false" || true
    fi
    sleep 120 # rate limit
    rm -f ${SELF_LOGS}/healthcheck_script_output.txt # remove old log to save space
fi

echo "INFO: Healthcheck => STOP"