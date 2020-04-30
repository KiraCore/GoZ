# GoZ
Game of Zones

Node Address: `goz.kiraex.com` 
Node Info: `curl goz.kiraex.com:10002/node_info`
Status: `curl goz.kiraex.com:10001/status`

IP Address Whitelist:
 * `35.230.14.56`
 * `34.82.233.123`
 * `34.83.182.199`

# Cosmos Alpha 

Node Address: `alpha.kiraex.com` 
Node Info: `curl alpha.kiraex.com:10002/node_info`
Status: `curl alpha.kiraex.com:10001/status`

# Registry Images

## Latest Images
> Base: `kiracore/goz:base-image-v0.0.1`
> Gaia: `kiracore/goz:gaia-ibc-alpha`
> Relayer: `kiracore/goz:relayer-alpha`
> Validator: `kiracore/goz:kira-1-validator`

## Accessing Images with SSH console

> Base container: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:base-image-v0.0.1) bash`
> Base Gaia container: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:gaia-ibc-alpha) bash`
> Base Relayer container: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:relayer-alpha) bash`

> Kira Validator container: 
 * Alpha: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-alpha-validator) bash`
 * GoZ: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-validator) bash`

> Kira Relayer container: 
 * Alpha: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-alpha-relayer) bash`
 * GoZ: `docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-relayer) bash`
* 
## If container is not running

> Kira Validator container:
 * Alpha: `docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-alpha-validator) /bin/bash`
 * GoZ:`docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-validator) /bin/bash`

> Kira Relayer container:
 * Alpha: `docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-alpha-relayer) /bin/bash`
 * GoZ: `docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-goz-relayer) /bin/bash`

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

## Docker Commands

> List containers: `docker ps`

# Google Cloud

> Agent logs: `sudo journalctl -u konlet-startup`
> Instance Metadata: `curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/`



