FROM kiracore/goz:gaia-ibc-alpha

ENV SENTRY_HOME=/root/sentry
ENV SENTRY_SCRIPS=${SENTRY_HOME}/scripts
ENV SENTRY_CONFIGS=${SENTRY_HOME}/configs
ENV CONTAINER_SCRIPTS=${SENTRY_HOME}/container

ENV START_SCRIPT=${CONTAINER_SCRIPTS}/start.sh
ENV BUILD_SCRIPT=${CONTAINER_SCRIPTS}/deployment.sh

#ADD ./scripts ${SENTRY_SCRIPS}
ADD ./configs ${SENTRY_CONFIGS}
ADD ./container ${CONTAINER_SCRIPTS}

RUN chmod 777 -R ${SENTRY_HOME}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive ${BUILD_SCRIPT}

RUN printenv 

CMD ["sh", "-c", "/bin/bash ${START_SCRIPT}"]

