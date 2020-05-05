#!/bin/bash

exec 2>&1
set -e
set -x

EMAIL_SENT=$HOME/email_sent

echo "INFO: Healthcheck => START"
sleep 30 # rate limit

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

STATUS_NGINX="$(systemctl2 is-active nginx.service)" || STATUS_RELAYER="unknown"
STATUS_GAIA="$(systemctl2 is-active gaiad.service)" || STATUS_GAIA="unknown"
STATUS_LCD="$(systemctl2 is-active lcd.service)" || STATUS_LCD="unknown"
STATUS_FAUCET="$(systemctl2 is-active faucet.service)" || STATUS_FAUCET="unknown"

if [ "${STATUS_GAIA}" != "active" ] || [ "${STATUS_LCD}" != "active" ] || [ "${STATUS_NGINX}" != "active" ] ; then
    echo "ERROR: One of the services is NOT active: Gaia($STATUS_GAIA), LCD($STATUS_LCD), Faucet($STATUS_FAUCET) or NGINX($STATUS_NGINX)"

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

    if [ "${STATUS_FAUCET}" != "active" ]  ; then
        echo ">> Faucet log:"
        tail -n 100 /var/log/journal/faucet.nginx.log || true
        systemctl2 restart faucet || systemctl2 status faucet.service || echo "Failed to re-start faucet service" || true
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
    sleep 60 # allow user to grab log output
    rm -f ${SELF_LOGS}/healthcheck_script_output.txt # remove old log to save space
fi

echo "INFO: Healthcheck => STOP"