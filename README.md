# GoZ
Game of Zones

Validator Address: `goz.kiraex.com` 
Node Info: `curl goz.kiraex.com:10002/node_info`
Status: `curl goz.kiraex.com:10001/status`

IP Address Whitelist:
 * `35.230.14.56`
 * `34.82.233.123`
 * `34.83.182.199`

# Kira Alpha 

Validator Address: `alpha.kiraex.com` 
Node Info: `curl alpha.kiraex.com:10002/node_info`
Status: `curl alpha.kiraex.com:10001/status`

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
tcp://6e4e0fad3d152b4086e24fd84602f71c6815832d@goz-trust-alias.kiraex.com:26656,tcp://c65d517ed3784605c96fb6be5a16c4d577e35bb3@internal-goz-sentry-public.kiraex.com:10000
```

Public Sentry:
  * Node Address (P2P seed): `tcp://c65d517ed3784605c96fb6be5a16c4d577e35bb3@goz-sentry-public.kiraex.com:10000`
  * Node Info: `curl goz-sentry-public.kiraex.com:10002/node_info`
  * Node Status: `curl goz-sentry-public.kiraex.com:10001/status`

SEEDS: 
```
tcp://6e4e0fad3d152b4086e24fd84602f71c6815832d@goz-trust-alias.kiraex.com:26656,tcp://c5a16d35506b3052d9d6f684881ced8016d42e76@internal-goz-sentry-private.kiraex.com:10000
```

# Localhost
 * Node Info: `curl 127.0.0.1:10002/node_info`
 * Node Status: `curl 127.0.0.1:10001/status`

## Accessing Images with SSH console

> Base container: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:base-image-v0.0.1) bash`
> Base Gaia container: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:gaia-ibc-alpha) bash`
> Base Relayer container: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:relayer-alpha) bash`

> Kira Validator container: 
 * Alpha: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-alpha-validator) bash`
 * GoZ: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-validator) bash`

> Kira Relayer container: 
 * Alpha: `docker exec -it $(docker ps -a -q --filter ancestor=kiracore/goz:kira-alpha-relayer) bash`
 * GoZ: `docker exec -it $(docker ps -a -q --filter ancestor=kiracore/goz:kira-goz-relayer) bash`

> Kira Sentry container: 
 * GoZ: `docker exec -it $(docker ps -a -q --filter ancestor=kiracore/goz:goz-hub-sentry) bash`

## Checking container error logs

> Kira Validator container (HEAD): 
 * Alpha: `docker logs --follow $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-alpha-validator)`
 * GoZ: `docker logs --follow $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-validator)`
> Kira Validator container (TAIL): 
 * Alpha: `docker logs --tail 50 --follow --timestamps $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-alpha-validator)`
 * GoZ: `docker logs --tail 50 --follow --timestamps $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-validator)`

> Kira Relayer container (HEAD): 
 * Alpha: `docker logs --follow $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-alpha-relayer)`
 * GoZ: `docker logs --follow $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-relayer)`
> Kira Relayer container (TAIL): 
 * Alpha: `docker logs --tail 50 --follow --timestamps $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-alpha-relayer)`
 * GoZ: `docker logs --tail 50 --follow --timestamps $(docker ps -a -q  --filter ancestor=kiracore/goz:goz-alpha-relayer)`

> Kira Sentry container  (HEAD): 
 * GoZ: `docker logs --follow $(docker ps -a -q  --filter ancestor=kiracore/goz:goz-hub-sentry)`
> Kira Sentry container  (TAIL): 
 * GoZ:  `docker logs --tail 50 --follow --timestamps $(docker ps -a -q --filter ancestor=kiracore/goz:goz-hub-sentry)`
  
## If container is NOT running

> Kira Validator container:
 * Alpha: `docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-alpha-validator) /bin/bash`
 * GoZ:`docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-validator) /bin/bash`

> Kira Relayer container:
 * Alpha: `docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-alpha-relayer) /bin/bash`
 * GoZ: `docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-relayer) /bin/bash`

> Kira Sentry container: 
 * GoZ: `docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:goz-hub-sentry) /bin/bash`
  
# Relayer Commands

> Address Lookup: `rly ch addr kira-alpha`
> Show All Connections: `rly pth list`
> Relay Failed Tx:  `rly tx rly kira-alpha_kira-1`
> Delete Path: `rly pth delete kira-alpha_hashquarkchain`
> Show Path: `rly pth show kira-alpha_hashquarkchain -j`
  
  Example Output:
```
{"chains":{"src":{"chain-id":"kira-alpha","client-id":"wyrwjrphee","connection-id":"fggmltnqgu","channel-id":"rxkhmzzlea","port-id":"transfer","order":"ORDERED"},"dst":{"chain-id":"hashquarkchain","client-id":"dahykiltwr","connection-id":"qkrjxeqgus","channel-id":"mryfsrxoit","port-id":"transfer","order":"ORDERED"},"strategy":{"type":"naive"}},"status":{"chains":true,"clients":true,"connection":true,"channel":true}}
```

> Token Transfer
 * Generate Path:  `rly pth gen kira-1 transfer hashquarkchain transfer kira-1_hashquarkchain`
 * Link Chains (all in one): `rly tx link kira-1_hashquarkchain`
 * Transfer Tokens: `rly tx transfer hashquarkchain kira-1 1quark true $(rly ch addr kira-1)`
 * Transfer Hanging Packets: `rly tx rly kira-1_hashquarkchain`

> Chain Linking (step by step):
 * Transact Clients: `rly transact clients kira-alpha_hashquarkchain --debug`
 * Transact Connection: `rly transact connection kira-alpha_hashquarkchain --debug`
 * Transact Channel: `rly transact channel kira-alpha_hashquarkchain --debug`
  
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

