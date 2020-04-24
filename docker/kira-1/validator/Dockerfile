FROM kiracore/goz:relayer-alpha
COPY ./deployment.sh /tmp/build.sh

ENV DENOM=ukex
ENV CHAINID=kira-1
ENV DOMAIN=kiraex.com
ENV RLYKEY=faucet

RUN chmod +x /tmp/build.sh

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh
