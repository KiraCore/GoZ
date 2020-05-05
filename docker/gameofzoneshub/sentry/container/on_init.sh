#!/bin/bash

exec 2>&1
set -e
set -x

echo "Staring on-init script..."

GAIAD_HOME=$HOME/.gaiad
GAIAD_CONFIG=$GAIAD_HOME/config
GAIAD_APP_TOML=$GAIAD_CONFIG/app.toml
GAIAD_CONFIG_TOML=$GAIAD_CONFIG/config.toml

GAIAD_CONFIG_GENESIS=$GAIAD_CONFIG/genesis.json
NODE_KEY_PATH=$GAIAD_CONFIG/node_key.json

INIT_START_FILE=$HOME/init_started
INIT_END_FILE=$HOME/init_ended
MAINTENANCE_FILE=$HOME/maintenence
GAIACLI_HOME=$HOME/.gaiacli

# external variables: P2P_PROXY_PORT, RPC_PROXY_PORT, LCD_PROXY_PORT, RLY_PROXY_PORT
P2P_LOCAL_PORT=26656
RPC_LOCAL_PORT=26657
LCD_LOCAL_PORT=1317

# set default parameters if not specified
[ -z "$SEEDS" ] && SEEDS="tcp://ef71392a1658182a9207985807100bb3d106dce6@35.233.155.199:26656"
[ -z "$MIN_GAS_VALUE" ] && MIN_GAS_VALUE="0.10"
[ -z "$MONIKER" ] && MONIKER="Kira Core | Asmodat | Cosmos | Sentry"
[ -z "$PEX" ] && PEX="true"
[ -z "$GENESIS_PATH" ] && GENESIS_PATH="$SELF_UPDATE/common/configs/genesis.json"
[ -z "$NODE_ADDESS" ] && NODE_ADDESS="tcp://localhost:$RPC_LOCAL_PORT"

gaiad init "$MONIKER" --home $GAIAD_HOME

mkdir -p $GAIAD_CONFIG
chmod -v -R 777 $GAIAD_HOME

cat $GENESIS_PATH > $GAIAD_CONFIG_GENESIS

# WARNING/TODO: Fee token might be diffrent than staking token
# DENOM=$(python -c "import sys, json; print(json.load(open('$GAIAD_CONFIG_GENESIS'))['app_state']['mint']['params']['mint_denom'])")
# MIN_GAS="${MIN_GAS_VALUE}${DENOM}"

# WARNING $(cat $GAIAD_CONFIG_GENESIS | jq -r '.chain_id') - does not work in case of large json files
CHAIN_ID=$(python3 -c "import sys, json; print(json.load(open('$GAIAD_CONFIG_GENESIS'))['chain_id'])")

echo "Genesis file Chain ID: ${CHAIN_ID}"

# NOTE: ensure that the gaia rpc is open to all connections
sed -i 's#tcp://127.0.0.1:26657#tcp://0.0.0.0:26657#g' $GAIAD_CONFIG_TOML
#sed -i 's/pruning = "syncable"/pruning = "nothing"/g' $GAIAD_APP_TOML
CDHelper text replace --old="seeds = \"\"" --new="seeds = \"$SEEDS\"" --input=$GAIAD_CONFIG_TOML
CDHelper text replace --old="pex = false" --new="pex = $PEX" --input=$GAIAD_CONFIG_TOML
CDHelper text replace --old="addr_book_strict = true" --new="addr_book_strict = false" --input=$GAIAD_CONFIG_TOML

[ -n "$PEERS" ] && CDHelper text replace --old="persistent_peers = \"\"" --new="persistent_peers = \"$PEERS\"" --input=$GAIAD_CONFIG_TOML
[ -n "$VALIDATORS" ] && CDHelper text replace --old="private_peer_ids = \"\"" --new="private_peer_ids = \"$VALIDATORS\"" --input=$GAIAD_CONFIG_TOML
# CDHelper text replace --old="minimum-gas-prices = \"\"" --new="minimum-gas-prices = \"$MIN_GAS\"" --input=$GAIAD_APP_TOML

gaiacli config trust-node true --home $GAIAD_HOME
gaiacli config chain-id $CHAIN_ID --home $GAIAD_HOME
gaiacli config node $NODE_ADDESS --home $GAIAD_HOME

# TODO: SETUP CUSTOM NODE KEY - FROM ENV
# NOTE: external variables: NODE_ID, NODE_KEY, VALIDATOR_KEY
# setup node key and unescape
# NOTE: to create new key delete $NODE_KEY_PATH and run gaiad start 
 rm -f -v $NODE_KEY_PATH && \
 echo $NODE_KEY > $NODE_KEY_PATH && \
 sed -i 's/\\\"/\"/g' $NODE_KEY_PATH

echo ${PASSPHRASE} | gaiacli keys list

# TODO: SETUP SOME DEFAULT TEST ACCOUNT

cat > /etc/systemd/system/gaiad.service << EOL
[Unit]
Description=gaiad
After=network.target
[Service]
Type=simple
User=root
WorkingDirectory=/usr/local
ExecStart=$GAIAD_BIN start --pruning=nothing
Restart=always
RestartSec=5
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
ExecStart=$GAIACLI_BIN rest-server --chain-id=$CHAIN_ID --home=$GAIACLI_HOME --node=$NODE_ADDESS 
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

${SELF_SCRIPS}/local-cors-proxy-v0.0.1.sh $RPC_PROXY_PORT http://127.0.0.1:$RPC_LOCAL_PORT; wait
${SELF_SCRIPS}/local-cors-proxy-v0.0.1.sh $LCD_PROXY_PORT http://127.0.0.1:$LCD_LOCAL_PORT; wait
${SELF_SCRIPS}/local-cors-proxy-v0.0.1.sh $P2P_PROXY_PORT http://127.0.0.1:$P2P_LOCAL_PORT; wait

echo "AWS Account Setup..."
aws configure set output $AWS_OUTPUT
aws configure set region $AWS_REGION
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure list

echo "Starting services..."
systemctl2 restart gaiad || systemctl2 status gaiad.service || echo "Failed to re-start gaiad service" && echo "$(cat /etc/systemd/system/gaiad.service)"
systemctl2 restart lcd || systemctl2 status lcd.service || echo "Failed to re-start lcd service" && echo "$(cat /etc/systemd/system/lcd.service)"
systemctl2 restart nginx || echo "Failed to re-start nginx service"

CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) Was Initalized Sucessfully" \
 --body="[$(date)] Attached $(find $SELF_LOGS -type f | wc -l) Log Files" \
 --html="false" \
 --recursive="true" \
 --attachments="$SELF_LOGS,/var/log/journal"







