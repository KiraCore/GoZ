#!/bin/bash

exec 2>&1
set -e
set -x

echo "Starting on-failure script..."

MAINTENANCE_FILE=$HOME/maintenence

systemctl2 stop gaiad
systemctl2 stop lcd
systemctl2 stop nginx

# TODO: send email fail to init notification

touch $MAINTENANCE_FILE


