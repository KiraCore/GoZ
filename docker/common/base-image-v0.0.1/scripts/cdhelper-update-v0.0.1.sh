#!/bin/bash

exec 2>&1
set -e
set -x

VERSION=$1

echo "------------------------------------------------"
echo " STARTED: CDHELPER UPDATE v0.0.1"
echo "------------------------------------------------"
echo "OLD-VERSION: $CDHelperVersion"
echo "NEW-VERSION: $VERSION"
echo "------------------------------------------------"

if [ "$VERSION" == "$CDHelperVersion" ]; then
    echo "CDHelper will not be updated, new and old versions are the same."
    exit 0
else
    echo "New version detected, installing..."
fi

cd /usr/local/src
rm -f -v ./CDHelper-linux-x64.zip
wget https://github.com/asmodat/CDHelper/releases/download/$VERSION/CDHelper-linux-x64.zip
rm -rfv /usr/local/bin/CDHelper
unzip CDHelper-linux-x64.zip -d /usr/local/bin/CDHelper
chmod -R -v 555 /usr/local/bin/CDHelper

SERVICE_FILE="/etc/systemd/system/scheduler.service"

rm -f -v $SERVICE_FILE

cat > $SERVICE_FILE << EOL
[Unit]
Description=Asmodat Deployment Scheduler
After=network.target
[Service]
Type=simple
User=root
EnvironmentFile=/etc/environment
ExecStart=/usr/local/bin/CDHelper/CDHelper scheduler github
WorkingDirectory=/root
Restart=on-failure
RestartSec=5
LimitNOFILE=4096
[Install]
WantedBy=multi-user.target
EOL

systemctl2 enable scheduler.service

CDHelper version

echo "------------------------------------------------"
echo " FINISHED: CDHELPER UPDATE v0.0.1"
echo "------------------------------------------------"
