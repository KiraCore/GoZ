#!/bin/bash

exec 2>&1
set -e
set -x

echo "Staring on-init script..."

chmod 777 -R $RLYS_HOME

rly cfg init || true

cat > /etc/systemd/system/relayer.service << EOL
[Unit]
Description=relayer
After=network.target
[Service]
Type=simple
User=root
WorkingDirectory=$SELF_HOME
ExecStart=$SELF_CONTAINER/relayer.sh
Restart=always
RestartSec=3
LimitNOFILE=4096
[Install]
WantedBy=multi-user.target
EOL

systemctl2 enable relayer.service
systemctl2 status relayer.service || true

echo "AWS Account Setup..."
aws configure set output $AWS_OUTPUT
aws configure set region $AWS_REGION
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure list

echo "Starting services..."
systemctl2 restart relayer || systemctl2 status relayer.service || echo "Failed to re-start relayer service" && echo "$(cat /etc/systemd/system/relayer.service)"

CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) Was Initalized Sucessfully" \
 --body="[$(date)] Attached $(find $SELF_LOGS -type f | wc -l) Log Files" \
 --html="false" \
 --recursive="true" \
 --attachments="$SELF_LOGS,/var/log/journal"







