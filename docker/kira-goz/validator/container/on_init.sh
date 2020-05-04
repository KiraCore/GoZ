#!/bin/bash

exec 2>&1
set -e
set -x

echo "Staring on-init script..."
NODE_KEY_PATH=$HOME/.gaiad/config/node_key.json
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

[ -z "$IMPORT_VALIDATOR_KEY" ] && IMPORT_VALIDATOR_KEY="False"
[ -z "$VALIDATOR_KEY_PATH" ] && VALIDATOR_KEY_PATH=$HOME/.gaiad/config/priv_validator_key.json
[ -z "$VALIDATOR_SIGNING_KEY_PATH" ] && VALIDATOR_SIGNING_KEY_PATH=$HOME/.gaiad/config/priv_validator_key.json
[ -z "$NODE_ADDESS" ] && NODE_ADDESS="tcp://localhost:$RPC_LOCAL_PORT"

[ -z "$CHAIN_JSON_FULL_PATH" ] && CHAIN_JSON_FULL_PATH="$SELF_UPDATE/$CHAIN_JSON_PATH"

if [ -f "$CHAIN_JSON_PATH" ] ; then
    echo "Chain configuration file was defined, loading JSON"
    cat $CHAIN_JSON_FULL_PATH > $CHAINID.json
    CHAINID=$(cat $CHAIN_JSON_FULL_PATH | jq -r '.chain-id')
    RLYKEY=$(cat $CHAIN_JSON_FULL_PATH | jq -r '.key')
else
    echo "Chain configuration file was NOT defined, loading ENV's"
    [ -z "$DENOM" ] && DENOM="ukex"
    [ -z "$CHAINID" ] && CHAINID="kira-0"
    [ -z "$RPC_ADDR" ] && RPC_ADDR="http://${ROUTE53_RECORD_NAME}.kiraex.com:${RPC_PROXY_PORT}"
    [ -z "$RLYKEY" ] && RLYKEY="faucet"
    [ -z "$RLYTRUSTING" ] && RLYTRUSTING="90m"
    echo "{\"key\":\"$RLYKEY\",\"chain-id\":\"$CHAINID\",\"rpc-addr\":\"$RPC_ADDR\",\"account-prefix\":\"cosmos\",\"gas\":200000,\"gas-prices\":\"0.025$DENOM\",\"default-denom\":\"$DENOM\",\"trusting-period\":\"$RLYTRUSTING\"}" > $CHAINID.json
fi

#  NOTE: external variables RLYKEY_ADDRESS, RLYKEY_MNEMONIC
rly config init

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
gaiacli keys import validator $VALIDATOR_SIGNING_KEY_PATH << EOF
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
RestartSec=5
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






