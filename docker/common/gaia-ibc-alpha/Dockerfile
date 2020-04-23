FROM kiracore/goz:base-image-v0.0.1
COPY ./deployment.sh /tmp/build.sh

ENV GAIA="${GOPATH}/src/github.com/cosmos/gaia"

RUN chmod +x /tmp/build.sh

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh

