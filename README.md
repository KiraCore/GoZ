# GoZ
Game of Zones



# Registry Images


> Base Image: `kiracore/goz:base-image-v0.0.1`

docker inspect --format="{{.Id}}" kiracore/goz:base-image-v0.0.1
> docker exec -it $(docker inspect --format="{{.Id}}" kiracore/goz:base-image-v0.0.1) bash

# Docker Commands

> `docker container ls` //To list all the running containers.