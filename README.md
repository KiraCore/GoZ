# GoZ
Game of Zones

## Phase 1b

* START: `18.05.2020 07:00 AM` 
* END:   `21.05.2020 07:00 AM` 
* DURATION: `72h`
* RLY Public Key: `cosmos1efzs6x9244z9hjz6pcrsam4muxxms74wz98h7c`
* Tokens In Genesis: `1200000`
* Gas Price: `0.0025`
* Estimated Tx Cost Min: `200000*0.0025=500`
* Estimated Tx Cost Max: `1000000*0.0025=2500`
* Transactions Max: `1200000/500=2400`
* Transactions Min: `1200000/2500=480`
* Update Span Min: `(3600*72)/2400=108s` or `1.8m`
* Update Span Max: `(3600*72)/480=540s` or `9m`

* Actual Tx Gas: `111247`
* Balance Remaining: `1194500`
* Actual Tx Cost: `111247*0.0025=~300`
* Transactions Max: `1194500/300=3981`
* Update Span Min: `(3600*79)/3981=71s` or `1.18m`

* Tokens In Genesis: `1200000`
* Cost To Connect: `2500`
* Average Update Cost: `84500`
* Gas Price: `0.0025`
* Tx Cost: `84500*0.0025=212`
* Max Number Of Updates: `(1200000-2500)/212=5648`
* Shortest Trust Possible: `255600/5648=46`

## Phase 2b

* START: `25.05.2020 07:00 AM` 
* END:   `28.05.2020 07:00 AM` 
* DURATION: `72h`
* RLY Public Key: `cosmos1efzs6x9244z9hjz6pcrsam4muxxms74wz98h7c`
* Tokens In Genesis: `10000000000`
* Gas Price: `0.0025`
* Estimated Tx Cost Min: `200000*0.0025=500`
* Estimated Tx Cost Max: `1000000*0.05=50000`
* Transactions Max: `10000000000/500=20000000`
* Transactions Min: `10000000000/50000=200000`
* Update Span Min: `(3600*72)/20000000=0.013s` or `77 TPS`
* Update Span Max: `(3600*80)/200000=1.44s`



Validator Address: `goz.kiraex.com` 
Node Info: 
 * External: `curl goz.kiraex.com:10002/node_info`
 * Internal: `curl internal-goz.kiraex.com:10002/node_info`
Status: 
 * External: `curl goz.kiraex.com:10001/status`
 * Internal: `curl internal-goz.kiraex.com:10001/status`
Transactions:
 * Internal: `curl internal-goz.kiraex.com:10002/txs/<hash>`

IP Address Whitelist:
 * `35.230.14.56`
 * `34.82.233.123`
 * `34.83.182.199`

# Kira Alpha 

Validator Address: `alpha.kiraex.com` 
Node Info: `curl alpha.kiraex.com:10002/node_info`
Status: `curl alpha.kiraex.com:10001/status`
Txs: `curl internal-alpha.kiraex.com:10002/txs/<hash>`

# Registry Images

## Latest Images
> Base: `kiracore/goz:base-image-v0.0.1`
> Gaia: `kiracore/goz:gaia-ibc-alpha`
> Relayer: `kiracore/goz:relayer-alpha`
> Validator: `kiracore/goz:kira-1-validator`

# GoZ Hub 

RPC Address: `http://35.233.155.199:26657`
A Record: `goz-trust-ip.kiraex.com -> 35.233.155.199`
CNAME Record: `goz-trust-alias.kiraex.com -> goz-trust-ip.kiraex.com`

Node Address: `tcp://6e4e0fad3d152b4086e24fd84602f71c6815832d@goz-trust-alias.kiraex.com:26656`
Wallet: `cosmos1efzs6x9244z9hjz6pcrsam4muxxms74wz98h7c`
  * Tokens: `doubloons`
  * Amount: `10000000000`
  * Genesis:`http://goz-trust-alias.kiraex.com:26657/genesis`
Staking Token: `stake`

Private Sentry:
  * Node Address (P2P seed): `tcp://c5a16d35506b3052d9d6f684881ced8016d42e76@goz-sentry-private.kiraex.com:10000`
  * Node Info: `curl goz-sentry-private.kiraex.com:10002/node_info`
  * Node Status: `curl goz-sentry-private.kiraex.com:10001/status`

SEEDS: 
```
d95a9f97e31f36d0a467e6855c71f5e5b8eccf65@34.83.90.172:26656,6ed008bf3a2ad341d84391bf47ea46e75a87e35e@35.233.155.199:26656,7cb9cbba21fdc3b004f098c116e5e2c2ac77ddfb@34.83.218.4:26656,ef36b3167b8599c46b0daf799f089068360c3911@34.83.0.237:26656,tcp://c65d517ed3784605c96fb6be5a16c4d577e35bb3@internal-goz-sentry-public.kiraex.com:10000
```

Public Sentry:
  * Node Address (P2P seed): `tcp://c65d517ed3784605c96fb6be5a16c4d577e35bb3@goz-sentry-public.kiraex.com:10000`
  * Node Info: `curl goz-sentry-public.kiraex.com:10002/node_info`
  * Node Status: `curl goz-sentry-public.kiraex.com:10001/status`

SEEDS: 
```
d95a9f97e31f36d0a467e6855c71f5e5b8eccf65@34.83.90.172:26656,6ed008bf3a2ad341d84391bf47ea46e75a87e35e@35.233.155.199:26656,7cb9cbba21fdc3b004f098c116e5e2c2ac77ddfb@34.83.218.4:26656,ef36b3167b8599c46b0daf799f089068360c3911@34.83.0.237:26656
```

# Localhost
 * Node Info: `curl 127.0.0.1:10002/node_info`
 * Node Status: `curl 127.0.0.1:10001/status`

## Accessing Images with SSH console

> Base container: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:base-image-v0.0.1) bash`
> Base Gaia container: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:gaia-ibc-alpha) bash`
> Base Relayer container: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:relayer-alpha) bash`

> Kira Validator container: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-validator) bash`
> Kira Relayer container: `docker exec -it $(docker ps -a -q --filter ancestor=kiracore/goz:kira-goz-relayer) bash`
  * Check Output Log: `cat $SELF_LOGS/relayer.txt`
> Kira Sentry container: `docker exec -it $(docker ps -a -q --filter ancestor=kiracore/goz:goz-hub-sentry) bash`

## Checking container error logs

> Kira Validator container (HEAD): `docker logs --follow $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-validator)`
> Kira Validator container (TAIL): `docker logs --tail 50 --follow --timestamps $(docker ps -a -q --filter ancestor=kiracore/goz:kira-goz-validator)`

> Kira Relayer container (HEAD): `docker logs --follow $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-relayer)`
> Kira Relayer container (TAIL): `docker logs --tail 50 --follow --timestamps $(docker ps -a -q  --filter ancestor=kiracore/goz:goz-alpha-relayer)`

> Kira Sentry container  (HEAD): `docker logs --follow $(docker ps -a -q  --filter ancestor=kiracore/goz:goz-hub-sentry)`
> Kira Sentry container  (TAIL): `docker logs --tail 50 --follow --timestamps $(docker ps -a -q --filter ancestor=kiracore/goz:goz-hub-sentry)`
  
## If container is NOT running

> Kira Validator container: `docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-validator) /bin/bash`
> Kira Relayer container: `docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-relayer) /bin/bash`
> Kira Sentry container: `docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:goz-hub-sentry) /bin/bash`
  
# Relayer Commands

> Address Lookup: `rly ch addr kira-alpha`
> Show All Connections: `rly pth list`
> Relay Failed Tx:  `rly tx rly kira-alpha_kira-1`
> Delete Path: `rly pth delete kira-alpha_hashquarkchain`
> Show Path: `rly pth show kira-alpha_hashquarkchain -j`
  
rly pth show kira-1_gameofzoneshub-1a -j

  Example Output:
```
{"chains":{"src":{"chain-id":"kira-alpha","client-id":"wyrwjrphee","connection-id":"fggmltnqgu","channel-id":"rxkhmzzlea","port-id":"transfer","order":"ORDERED"},"dst":{"chain-id":"hashquarkchain","client-id":"dahykiltwr","connection-id":"qkrjxeqgus","channel-id":"mryfsrxoit","port-id":"transfer","order":"ORDERED"},"strategy":{"type":"naive"}},"status":{"chains":true,"clients":true,"connection":true,"channel":true}}
```

> Token Transfer
 * Generate Path:  `rly pth gen kira-1 transfer hashquarkchain transfer kira-1_hashquarkchain`
 * Link Chains (all in one): `rly tx link kira-1_gameofzoneshub-1a`**rly pth show  -j**
 * Transfer Tokens: `rly tx transfer hashquarkchain kira-1 1quark true $(rly ch addr kira-1)`
 * Transfer Hanging Packets: `rly tx rly kira-1_hashquarkchain`

> Chain Linking (step by step):
 * Transact Clients: `rly transact clients kira-1_gameofzoneshub-1a --debug`
 * Transact Connection: `rly transact connection kira-1_gameofzoneshub-1a --debug`
 * Transact Channel: `rly transact channel kira-1_gameofzoneshub-1a --debug`
  
> Check Balances: `rly q bal kira-1 -j`
> Update Connection: `rly tx raw update-client {src_chain_id} {dst_chain_id} {client-id}`

# Gaia Commands

> Default Node Key Location: `$HOME/.gaiad/config/node_key.json`
> Node Key ID Lookup: `gaiad tendermint show-node-id`

# Docker Commands

> List containers: `docker ps`

# Google Cloud

> Agent Logs: `sudo journalctl -u konlet-startup`
> Instance Metadata: `curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/`


# Wipe Connection
> rly lite delete kira-1
> rly lite delete gameofzoneshub-1a
> rly pth delete kira-1_gameofzoneshub-1a

# Re-init Connection
* Initialize LIte Clients
    > rly lite init kira-1 -f 
    > rly lite init gameofzoneshub-1a -f 
* Generate new path
    > rly pth gen kira-1 transfer gameofzoneshub-1a transfer kira-1_gameofzoneshub-1a -f
* Link: NOTE - DO NOT USE THE `rly tx link kira-1_gameofzoneshub-1a --debug` 
  > set fees if needed `rly ch edit gameofzoneshub-1a gas-prices 0.025doubloons`
    > rly transact clients kira-1_gameofzoneshub-1a --debug
    > rly transact connection kira-1_gameofzoneshub-1a --debug
    > rly transact channel kira-1_gameofzoneshub-1a --debug
* Query Status
    > rly pth show kira-1_gameofzoneshub-1a
    > rly query full-path kira-1_gameofzoneshub-1a --debug
    > rly q client kira-1 jttozounos
    > rly q client gameofzoneshub-1a znmvqkvtub

* Transfer Tokens
    > Src -> Dst: `rly tx transfer kira-1 gameofzoneshub-1a 2ukex true $(rly ch addr gameofzoneshub-1a) --path=kira-1_gameofzoneshub-1a --debug`
    > Dst -> Src: `rly tx transfer gameofzoneshub-1a kira-1 2doubloons true $(rly ch addr kira-1) --path=kira-1_gameofzoneshub-1a --debug`
    > Push pending tx: `rly transact relay kira-1_gameofzoneshub-1a --debug`


## Re-connection steps:
1. Delete Chain
2. Force Re-Add Chain (updates info from files)
3. Delete rly key's
4. Restore rly key's
5. Set key as default of the chain
6. Delete lite client (as it is used in the path creation)
7. Delete Path
8. Create new path
9. Lite client init
10. Lite client update
11. Request Test Tokens
12. Establish clients, connection and channel