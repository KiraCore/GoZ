# GoZ
Game of Zones

Node Address: `goz.kiraex.com` 
Node Info: `curl goz.kiraex.com:10002/node_info`

# Registry Images

## Latest Images
> Base: `kiracore/goz:base-image-v0.0.1`
> Gaia: `kiracore/goz:gaia-ibc-alpha`
> Relayer: `kiracore/goz:relayer-alpha`
> Validator: `kiracore/goz:kira-1-validator`

## Accessing Images with SSH console

> Base container: 
`docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:base-image-v0.0.1) bash`

> Gaia container: 
`docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:gaia-ibc-alpha) bash`

> Relayer container: 
`docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:relayer-alpha) bash`

> Validator container: 
`docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-1-validator) bash`

> Relay-Node container: 
`docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-1-relayer) bash`

## If container is not running

> Validator-Node container:
`docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-1-validator) /bin/bash`

> Relayer-Node container:
`docker run -it -d $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-1-relayer) /bin/bash`

## Checking container error logs

> Validator container (HEAD): 
`docker logs --follow $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-1-validator)`
> Validator container (TAIL): 
`docker logs --tail 50 --follow --timestamps $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-1-validator)`

> Relayer Node container (HEAD): 
`docker logs --follow $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-1-relayer)`
> Relayer Node container (TAIL): 
`docker logs --tail 50 --follow --timestamps $(docker ps -a -q  --filter ancestor=kiracore/goz:kira-1-relayer)`

## Docker Commands

> List containers: `docker ps`

# Google Cloud

> Agent logs: `sudo journalctl -u konlet-startup`
> Instance Metadata: `curl -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/`



