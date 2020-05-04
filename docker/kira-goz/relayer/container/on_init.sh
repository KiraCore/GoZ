#!/bin/bash

exec 2>&1
set -e
set -x

echo "Staring on-init script..."

# setup external ip in the AWSRoute53 registry
INSTANCE_NAME=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/name 2>/dev/null)
INTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/ip 2>/dev/null)
EXTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip 2>/dev/null)

# external variables: ROUTE53_RECORD_NAME, ROUTE53_ZONE, EXTERNAL_IP, ROUTE53_TTY
AWSHelper route53 upsert-a-record --name="$ROUTE53_RECORD_NAME" --zone=$ROUTE53_ZONE --value="$EXTERNAL_IP" --ttl=$ROUTE53_TTY

chmod 777 -R $RLYS_HOME

rly cfg init || true


# rly dev gaia "root" "/usr/local" > gaiad.service && mv -v gaiad.service /etc/systemd/system/gaiad.service
cat > /etc/systemd/system/relayer.service << EOL
[Unit]
Description=gaiad
After=network.target
[Service]
Type=simple
User=root
WorkingDirectory=/root/
ExecStart=$SELF_CONTAINER/relayer.sh
Restart=on-failure
RestartSec=3
LimitNOFILE=4096
[Install]
WantedBy=multi-user.target
EOL

cat > /etc/systemd/system/lcd.service << EOL
[Unit]
Description=Light Client Daemon Service
After=network.target
[Service]
Type=simple
EnvironmentFile=/etc/environment
ExecStart=$GAIACLI_BIN rest-server --chain-id=$CHAINID --home=$GAIACLI_HOME --node=$NODE_ADDESS 
Restart=always
RestartSec=5
LimitNOFILE=4096
[Install]
WantedBy=default.target
EOL

# rly dev faucet "root" "/usr/local" $CHAINID $RLYKEY 100000$DENOM > faucet.service && mv -v faucet.service /etc/systemd/system/faucet.service
cat > /etc/systemd/system/faucet.service << EOL
[Unit]
Description=faucet
After=network.target
[Service]
Type=simple
User=root
WorkingDirectory=/usr/local
ExecStart=$RLY_BIN testnets faucet $CHAINID $RLYKEY 100000$DENOM
Restart=always
RestartSec=3
LimitNOFILE=4096
[Install]
WantedBy=multi-user.target
EOL

systemctl2 enable faucet.service
systemctl2 enable gaiad.service
systemctl2 enable lcd.service
systemctl2 enable nginx.service

systemctl2 status faucet.service || true
systemctl2 status gaiad.service || true
systemctl2 status lcd.service || true
systemctl2 status nginx.service || true

${SELF_SCRIPS}/local-cors-proxy-v0.0.1.sh $RPC_PROXY_PORT http://127.0.0.1:$RPC_LOCAL_PORT; wait
${SELF_SCRIPS}/local-cors-proxy-v0.0.1.sh $LCD_PROXY_PORT http://127.0.0.1:$LCD_LOCAL_PORT; wait
${SELF_SCRIPS}/local-cors-proxy-v0.0.1.sh $P2P_PROXY_PORT http://127.0.0.1:$P2P_LOCAL_PORT; wait
${SELF_SCRIPS}/local-cors-proxy-v0.0.1.sh $RLY_PROXY_PORT http://127.0.0.1:$RLY_LOCAL_PORT; wait

echo "AWS Account Setup..."

aws configure set output $AWS_OUTPUT
aws configure set region $AWS_REGION
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"

aws configure list

echo "Starting services..."
systemctl2 restart gaiad
systemctl2 restart lcd
systemctl2 restart nginx
systemctl2 restart faucet

CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) Was Initalized Sucessfully" \
 --body="[$(date)] Attached $(find $SELF_LOGS -type f | wc -l) Log Files" \
 --html="false" \
 --recursive="true" \
 --attachments="$SELF_LOGS,/var/log/journal"







