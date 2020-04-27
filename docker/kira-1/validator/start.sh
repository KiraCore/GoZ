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

cd

if [ -f "$INIT_END_FILE" ]; then
   echo "Validator node was completed successfully, starting services..."

   systemctl2 start gaiad
   systemctl2 start faucet

   sleep 10
   
   STATUS_FAUCET="$(systemctl2 is-active faucet.service)"
   STATUS_GAIA="$(systemctl2 is-active gaiad.service)"
   
   while true
   do
       if [ "${STATUS_GAIA}" = "active" ] && [ "${STATUS_FAUCET}" = "active" ] ; then
           echo "Logs lookup..."
           tail -n 1 /var/log/journal/faucet.service.log
           tail -n 1 /var/log/journal/gaiad.service.log
           sleep 5
       else 
           echo "Faucet Service ($STATUS_FAUCET) or Gaia Service ($STATUS_GAIA) is not active."
           echo ">> Faucet log:"
           tail -n 100 /var/log/journal/faucet.service.log
           echo ">> Gaia log:"
           tail -n 100 /var/log/journal/gaiad.service.log
           echo ">> Stopping services..."
           systemctl2 stop gaiad
           systemctl2 stop faucet
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

# external variables RLYKEY_ADDRESS, RLYKEY_MNEMONIC
rly config init
echo "{\"key\":\"$RLYKEY\",\"chain-id\":\"$CHAINID\",\"rpc-addr\":\"http://$DOMAIN:26657\",\"account-prefix\":\"cosmos\",\"gas\":200000,\"gas-prices\":\"0.025$DENOM\",\"default-denom\":\"$DENOM\",\"trusting-period\":\"330h\"}" > $CHAINID.json
# NOTE: you will want to save the content from this JSON file
rly chains add -f $CHAINID.json
rly keys restore $CHAINID $RLYKEY "$RLYKEY_MNEMONIC"
rly keys list $CHAINID

gaiad init --chain-id $CHAINID $CHAINID

# external variables: NODE_ID, NODE_KEY, VALIDATOR_KEY
# setup node key and unescape
rm -f -v $NODE_KEY_PATH && \
 echo $NODE_KEY > $NODE_KEY_PATH && \
 sed -i 's/\\\"/\"/g' $NODE_KEY_PATH

# setup validator signing key and unescape
rm -f -v $VALIDATOR_KEY_PATH && \
 echo $VALIDATOR_KEY > $VALIDATOR_KEY_PATH && \
 sed -i 's/\\\"/\"/g' $VALIDATOR_KEY_PATH

# NOTE: ensure that the gaia rpc is open to all connections
sed -i 's#tcp://127.0.0.1:26657#tcp://0.0.0.0:26657#g' $CONFIG_TOML_PATH
sed -i "s/stake/$DENOM/g" $GENESIS_JSON_PATH
sed -i 's/pruning = "syncable"/pruning = "nothing"/g' $APP_TOML_PATH

# external variables: KEYRINGPASS, PASSPHRASE
# Exporting: gaiacli keys export validator -o text
# Deleting: gaiacli keys delete validator
# Importing (first time requires to input keyring password twice):
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

rly dev gaia "root" "/usr/local" > gaiad.service
mv -v gaiad.service /etc/systemd/system/gaiad.service

rly dev faucet "root" "/usr/local" $CHAINID $RLYKEY 100000$DENOM > faucet.service
mv -v faucet.service /etc/systemd/system/faucet.service

systemctl2 status faucet.service
systemctl2 status gaiad.service

touch $INIT_END_FILE
echo "Node setup setup ended."

