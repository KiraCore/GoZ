#!/bin/bash

exec 2>&1
set -e
set -x

touch $MAINTENANCE_FILE # notify entire environment to halt

systemctl2 stop gaiad
systemctl2 stop lcd
systemctl2 stop nginx

# TODO: send email fail to init notification


#AWSHelper email send --from "noreply@kiracore.com" --to="asmodat@gmail.com"

