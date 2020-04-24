# GoZ
Game of Zones

# Registry Images

## Latest Images
> Base: `kiracore/goz:base-image-v0.0.1`
> Gaia: `kiracore/goz:gaia-ibc-alpha`
> Relayer: `kiracore/goz:relayer-alpha`

## Accessing Images with SSH console

> Base container: 
`docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:base-image-v0.0.1) bash`

> Gaia container: 
`docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:gaia-ibc-alpha) bash`

> Relayer container: 
`docker exec -it $(docker ps -a -q  --filter ancestor=kiracore/goz:relayer-alpha) bash`

## Docker Commands

> List containers: `docker ps`

# Google Cloud

> Agent logs: `sudo journalctl -u konlet-startup`