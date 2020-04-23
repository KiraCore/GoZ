FROM kiracore/goz:gaia-ibc-alpha
COPY ./deployment.sh /tmp/build.sh

ENV RELAYER="${GOPATH}/src/github.com/iqlusioninc/relayer"

RUN chmod +x /tmp/build.sh

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh

