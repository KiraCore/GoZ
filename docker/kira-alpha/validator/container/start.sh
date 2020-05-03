#!/bin/bash

exec 2>&1
set -e
set -x

echo "Staring node..."
NODE_KEY_PATH=$HOME/.gaiad/config/node_key.json
VALIDATOR_KEY_PATH=$HOME/.gaiad/config/priv_validator_key.json
APP_TOML_PATH=$HOME/.gaiad/config/app.toml
GENESIS_JSON_PATH=$HOME/.gaiad/config/genesis.json
CONFIG_TOML_PATH=$HOME/.gaiad/config/config.toml
INIT_START_FILE=$HOME/init_started
INIT_END_FILE=$HOME/init_ended
GAIACLI_HOME=$HOME/.gaiacli

# external variables: P2P_PROXY_PORT, RPC_PROXY_PORT, LCD_PROXY_PORT, RLY_PROXY_PORT
P2P_LOCAL_PORT=26656
RPC_LOCAL_PORT=26657
LCD_LOCAL_PORT=1317
RLY_LOCAL_PORT=8000
NODE_ADDESS="tcp://localhost:$RPC_LOCAL_PORT"

[ -z "$IMPORT_VALIDATOR_KEY" ] && IMPORT_VALIDATOR_KEY="False"

cd

if [ -f "$INIT_END_FILE" ]; then
   echo "Validator node was completed successfully, starting services..."

   systemctl2 restart gaiad

   # setup external ip in the AWSRoute53 registry
   INSTANCE_NAME=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/name 2>/dev/null)
   INTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/ip 2>/dev/null)
   EXTERNAL_IP=$(curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip 2>/dev/null)
   
   # external variables: ROUTE53_RECORD_NAME, ROUTE53_ZONE, EXTERNAL_IP, ROUTE53_TTY
   AWSHelper route53 upsert-a-record --name="$ROUTE53_RECORD_NAME" --zone=$ROUTE53_ZONE --value="$EXTERNAL_IP" --ttl=$ROUTE53_TTY

   sleep 30
   
   systemctl2 restart faucet
   systemctl2 restart lcd
   systemctl2 restart nginx

   sleep 10
   
   STATUS_FAUCET="$(systemctl2 is-active faucet.service)"
   STATUS_GAIA="$(systemctl2 is-active gaiad.service)"
   STATUS_LCD="$(systemctl2 is-active lcd.service)"
   STATUS_NGINX="$(systemctl2 is-active nginx.service)"
   
   while true
   do
       if [ "${STATUS_GAIA}" = "active" ] && [ "${STATUS_FAUCET}" = "active" ] && [ "${STATUS_LCD}" = "active" ] && [ "${STATUS_NGINX}" = "active" ] ; then
           echo "Logs lookup..."
           tail -n 1 /var/log/journal/faucet.service.log
           tail -n 2 /var/log/journal/gaiad.service.log
           tail -n 1 /var/log/journal/lcd.service.log
           tail -n 1 /var/log/journal/nginx.service.log
           sleep 7
       else 
           echo "Faucet Service ($STATUS_FAUCET), Gaia Service ($STATUS_GAIA), LCD Service ($STATUS_LCD) or NGINX Service ($STATUS_NGINX) is not active."
           echo ">> Faucet log:"
           tail -n 100 /var/log/journal/faucet.service.log
           echo ">> Gaia log:"
           tail -n 100 /var/log/journal/gaiad.service.log
           echo ">> LCD log:"
           tail -n 100 /var/log/journal/lcd.service.log
           echo ">> NGINX log:"
           tail -n 100 /var/log/journal/nginx.service.log
           echo ">> Stopping services..."
           systemctl2 stop gaiad
           systemctl2 stop faucet
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

#  NOTE: external variables RLYKEY_ADDRESS, RLYKEY_MNEMONIC
rly config init
echo "{\"key\":\"$RLYKEY\",\"chain-id\":\"$CHAINID\",\"rpc-addr\":\"http://$DOMAIN:$RPC_LOCAL_PORT\",\"account-prefix\":\"cosmos\",\"gas\":200000,\"gas-prices\":\"0.025$DENOM\",\"default-denom\":\"$DENOM\",\"trusting-period\":\"$RLYTRUSTING\"}" > $CHAINID.json
# NOTE: you will want to save the content from this JSON file
rly chains add -f $CHAINID.json
rly keys restore $CHAINID $RLYKEY "$RLYKEY_MNEMONIC"
rly keys list $CHAINID

gaiad init --chain-id $CHAINID $CHAINID

# NOTE: external variables: NODE_ID, NODE_KEY, VALIDATOR_KEY
# setup node key and unescape
# NOTE: to create new key delete $NODE_KEY_PATH and run gaiad start 
rm -f -v $NODE_KEY_PATH && \
 echo $NODE_KEY > $NODE_KEY_PATH && \
 sed -i 's/\\\"/\"/g' $NODE_KEY_PATH

# setup validator signing key and unescape
# NOTE: to create new key delete $VALIDATOR_KEY_PATH and run gaiad start 
if [ "$IMPORT_VALIDATOR_KEY" == "True" ]; then
   echo "Validator key will be imported"
   rm -f -v $VALIDATOR_KEY_PATH 
   echo $VALIDATOR_KEY > $VALIDATOR_KEY_PATH
   sed -i 's/\\\"/\"/g' $VALIDATOR_KEY_PATH
else
   echo "Validator key will NOT be imported"
fi

# NOTE: ensure that the gaia rpc is open to all connections
sed -i 's#tcp://127.0.0.1:26657#tcp://0.0.0.0:26657#g' $CONFIG_TOML_PATH
sed -i "s/stake/$DENOM/g" $GENESIS_JSON_PATH
sed -i 's/pruning = "syncable"/pruning = "nothing"/g' $APP_TOML_PATH

#  NOTE: external variables: KEYRINGPASS, PASSPHRASE
#  NOTE: Exporting: gaiacli keys export validator -o text
#  NOTE: Deleting: gaiacli keys delete validator
#  NOTE: Importing (first time requires to input keyring password twice):
gaiacli keys import validator $VALIDATOR_SELF_KEY_PATH << EOF
$PASSPHRASE
$KEYRINGPASS
$KEYRINGPASS
EOF

echo ${PASSPHRASE} | gaiacli keys list

echo "Creating genesis file..."
echo ${KEYRINGPASS} | gaiad add-genesis-account $(gaiacli keys show validator -a) 100000000000$DENOM,10000000samoleans
gaiad add-genesis-account $(rly chains addr $CHAINID) 10000000000000$DENOM,10000000samoleans

gaiad gentx --name validator --amount 90000000000$DENOM << EOF
$KEYRINGPASS
$KEYRINGPASS
$KEYRINGPASS
EOF

gaiad collect-gentxs

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

${SCRIPTS_DIR}/local-cors-proxy-v0.0.1.sh $RPC_PROXY_PORT http://127.0.0.1:$RPC_LOCAL_PORT; wait
${SCRIPTS_DIR}/local-cors-proxy-v0.0.1.sh $LCD_PROXY_PORT http://127.0.0.1:$LCD_LOCAL_PORT; wait
${SCRIPTS_DIR}/local-cors-proxy-v0.0.1.sh $P2P_PROXY_PORT http://127.0.0.1:$P2P_LOCAL_PORT; wait
${SCRIPTS_DIR}/local-cors-proxy-v0.0.1.sh $RLY_PROXY_PORT http://127.0.0.1:$RLY_LOCAL_PORT; wait

echo "AWS Account Setup..."

aws configure set output $AWS_OUTPUT
aws configure set region $AWS_REGION
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"

aws configure list

touch $INIT_END_FILE
echo "Node setup setup ended."

