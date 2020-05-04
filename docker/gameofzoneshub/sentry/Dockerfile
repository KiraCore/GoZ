FROM kiracore/goz:gaia-ibc-alpha

ENV SELF_HOME=/root/self
ENV SELF_SCRIPS=${SELF_HOME}/scripts
ENV SELF_CONFIGS=${SELF_HOME}/configs
ENV SELF_UPDATE=${SELF_HOME}/update
ENV SELF_CONTAINER=${SELF_HOME}/container

ENV START_SCRIPT=${SELF_CONTAINER}/start.sh
ENV BUILD_SCRIPT=${SELF_CONTAINER}/deployment.sh
ENV HEALTHCHECK_SCRIPT=${SELF_CONTAINER}/healthcheck.sh

RUN mkdir -p ${SELF_UPDATE} && mkdir -p ${SELF_CONFIGS} && mkdir -p ${SELF_CONTAINER}

ADD ./scripts ${SELF_SCRIPS}
ADD ./configs ${SELF_CONFIGS}
ADD ./container ${SELF_CONTAINER}

RUN chmod 777 -R ${SELF_HOME}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive ${BUILD_SCRIPT}

RUN printenv 

HEALTHCHECK --interval=5s --timeout=3600s --start-period=300s --retries=3 CMD ${HEALTHCHECK_SCRIPT}

CMD ["sh", "-c", "/bin/bash ${START_SCRIPT}"]

