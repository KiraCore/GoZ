#!/bin/bash

exec 2>&1
set -e
set -x

echo "Staring node..."
GAIAD_HOME=$HOME/.gaiad
GAIAD_CONFIG=$GAIAD_HOME/config
GAIAD_APP_TOML=$GAIAD_CONFIG/app.toml
GAIAD_CONFIG_TOML=$GAIAD_CONFIG/config.toml

GAIAD_CONFIG_GENESIS=$GAIAD_CONFIG/genesis.json
NODE_KEY_PATH=$GAIAD_CONFIG/node_key.json

INIT_START_FILE=$HOME/init_started
INIT_END_FILE=$HOME/init_ended
GAIACLI_HOME=$HOME/.gaiacli

# external variables: P2P_PROXY_PORT, RPC_PROXY_PORT, LCD_PROXY_PORT, RLY_PROXY_PORT
P2P_LOCAL_PORT=26656
RPC_LOCAL_PORT=26657
LCD_LOCAL_PORT=1317
NODE_ADDESS="tcp://localhost:$RPC_LOCAL_PORT"

SEEDS="tcp://ef71392a1658182a9207985807100bb3d106dce6@35.233.155.199:26656"

cd

if [ -f "$INIT_END_FILE" ]; then
   echo "Sentry node was setup successfully, starting services..."

   systemctl2 restart gaiad

   # setup external ip in the AWSRoute53 registry
   INSTANCE_NAME=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/name 2>/dev/null)
   INTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/ip 2>/dev/null)
   EXTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip 2>/dev/null)
   
   # external variables: ROUTE53_RECORD_NAME, ROUTE53_ZONE, EXTERNAL_IP, ROUTE53_TTY
   AWSHelper route53 upsert-a-record --name="$ROUTE53_RECORD_NAME" --zone=$ROUTE53_ZONE --value="$EXTERNAL_IP" --ttl=$ROUTE53_TTY

   sleep 30
   
   systemctl2 restart gaiad
   systemctl2 restart lcd
   systemctl2 restart nginx

   sleep 10
   
   STATUS_GAIA="$(systemctl2 is-active gaiad.service)"
   STATUS_LCD="$(systemctl2 is-active lcd.service)"
   STATUS_NGINX="$(systemctl2 is-active nginx.service)"
   
   while true
   do
       if [ "${STATUS_GAIA}" = "active" ] && [ "${STATUS_LCD}" = "active" ] && [ "${STATUS_NGINX}" = "active" ] ; then
           echo "Logs lookup..."
           tail -n 2 /var/log/journal/gaiad.service.log
           tail -n 1 /var/log/journal/lcd.service.log
           tail -n 1 /var/log/journal/nginx.service.log
           sleep 7
       else 
           echo "Gaia Service ($STATUS_GAIA), LCD Service ($STATUS_LCD) or NGINX Service ($STATUS_NGINX) is not active."
           echo ">> Gaia log:"
           tail -n 100 /var/log/journal/gaiad.service.log
           echo ">> LCD log:"
           tail -n 100 /var/log/journal/lcd.service.log
           echo ">> NGINX log:"
           tail -n 100 /var/log/journal/nginx.service.log
           echo ">> Stopping services..."
           systemctl2 stop gaiad
           systemctl2 stop lcd
           systemctl2 stop nginx
           exit 1  
       fi
   done
elif [ -f "$INIT_START_FILE" ]; then
   echo "Node setup failed :("
   /bin/bash
   exit 0
else
   echo "Starting node setup..."
   touch $INIT_START_FILE
fi

cat $SENTRY_CONFIGS/genesis.json > $GAIAD_CONFIG_GENESIS

chmod -v -R 777 $GAIAD_HOME
DENOM=$(python -c "import sys, json; print(json.load(open('$GAIAD_CONFIG_GENESIS'))['app_state']['mint']['params']['mint_denom'])")
MIN_GAS="0.10$DENOM"
CHAIN_ID=$(python -c "import sys, json; print(json.load(open('$GAIAD_CONFIG_GENESIS'))['chain_id'])")

gaiad init "Kira Core | Asmodat | Cosmos | Sentry" --home $GAIAD_HOME

# NOTE: ensure that the gaia rpc is open to all connections
sed -i 's#tcp://127.0.0.1:26657#tcp://0.0.0.0:26657#g' $GAIAD_CONFIG_TOML
#sed -i 's/pruning = "syncable"/pruning = "nothing"/g' $GAIAD_APP_TOML
CDHelper text replace --old="seeds = \"\"" --new="seeds = \"$SEEDS\"" --input=$GAIAD_CONFIG
CDHelper text replace --old="pex = false" --new="pex = true" --input=$GAIAD_CONFIG
CDHelper text replace --old="addr_book_strict = true" --new="addr_book_strict = false" --input=$GAIAD_CONFIG
# CDHelper text replace --old="persistent_peers = \"\"" --new="persistent_peers = \"$PEERS\"" --input=$GAIAD_CONFIG
# CDHelper text replace --old="private_peer_ids = \"\"" --new="private_peer_ids = \"$VALIDATORS\"" --input=$GAIAD_CONFIG
CDHelper text replace --old="minimum-gas-prices = \"\"" --new="minimum-gas-prices = \"$MIN_GAS\"" --input=$GAIAD_APP_CONFIG


gaiacli config trust-node true --home $GAIAD_HOME
gaiacli config chain-id $(cat $GAIAD_CONFIG_GENESIS | jq -r '.chain_id') --home $GAIAD_HOME
gaiacli config node $NODE_ADDESS --home $GAIAD_HOME

# TODO: SETUP CUSTOM NODE KEY - FROM ENV
# NOTE: external variables: NODE_ID, NODE_KEY, VALIDATOR_KEY
# setup node key and unescape
# NOTE: to create new key delete $NODE_KEY_PATH and run gaiad start 
# rm -f -v $NODE_KEY_PATH && \
# echo $NODE_KEY > $NODE_KEY_PATH && \
# sed -i 's/\\\"/\"/g' $NODE_KEY_PATH

# OR

# TODO: SETUP CUSTOM NODE KEY - FROM SECRETS
#echo "Updating node_key..."
#echo $(gaiacli status | jq -r '.node_info.id')
#AWSHelper sm get-secret --name=$SECRET_KEY_NAME --key="sentry_node_key" --force=true --output=$NODE_KEY_PATH --silent=true
#echo $(gaiacli status | jq -r '.node_info.id')


echo ${PASSPHRASE} | gaiacli keys list

# TODO: SETUP SOME DEFAULT TEST ACCOUNT


# rly dev gaia "root" "/usr/local" > gaiad.service && mv -v gaiad.service /etc/systemd/system/gaiad.service
cat > /etc/systemd/system/gaiad.service << EOL
[Unit]
Description=gaiad
After=network.target
[Service]
Type=simple
User=root
WorkingDirectory=/usr/local
ExecStart=$GAIAD_BIN start --pruning=nothing
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

systemctl2 enable gaiad.service
systemctl2 enable lcd.service
systemctl2 enable nginx.service

systemctl2 status gaiad.service || true
systemctl2 status lcd.service || true
systemctl2 status nginx.service || true

${SCRIPTS_DIR}/local-cors-proxy-v0.0.1.sh $RPC_PROXY_PORT http://127.0.0.1:$RPC_LOCAL_PORT; wait
${SCRIPTS_DIR}/local-cors-proxy-v0.0.1.sh $LCD_PROXY_PORT http://127.0.0.1:$LCD_LOCAL_PORT; wait
${SCRIPTS_DIR}/local-cors-proxy-v0.0.1.sh $P2P_PROXY_PORT http://127.0.0.1:$P2P_LOCAL_PORT; wait

echo "AWS Account Setup..."

aws configure set output $AWS_OUTPUT
aws configure set region $AWS_REGION
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"

aws configure list

touch $INIT_END_FILE
echo "Sentry node setup setup ended."

