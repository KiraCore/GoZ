#!/bin/bash

exec 2>&1
set -e
set -x

echo "Testing health status"

if [ "${MAINTENANCE_MODE}" = "true"  ] || [ -f "$MAINTENANCE_FILE" ] ; then
     echo "Entering maitenance mode!"
     exit 0
fi

STATUS_GAIA="$(systemctl2 is-active gaiad.service)"
STATUS_LCD="$(systemctl2 is-active lcd.service)"
STATUS_NGINX="$(systemctl2 is-active nginx.service)"

if [ "${STATUS_GAIA}" = "active" ] && [ "${STATUS_LCD}" = "active" ] && [ "${STATUS_NGINX}" = "active" ] ; then
    echo "Logs lookup..."
    tail -n 2 /var/log/journal/gaiad.service.log
    tail -n 1 /var/log/journal/lcd.service.log
    tail -n 1 /var/log/journal/nginx.service.log
else 
    echo "Gaia Service ($STATUS_GAIA), LCD Service ($STATUS_LCD) or NGINX Service ($STATUS_NGINX) is not active."
    echo ">> Gaia log:"
    tail -n 100 /var/log/journal/gaiad.service.log
    echo ">> LCD log:"
    tail -n 100 /var/log/journal/lcd.service.log
    echo ">> NGINX log:"
    tail -n 100 /var/log/journal/nginx.service.log
    echo ">> Stopping services..."
    exit 1  
fi