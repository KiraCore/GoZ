FROM kiracore/goz:gaia-ibc-alpha

#ADD ./scripts ${SELF_SCRIPS}
ADD ./configs ${SELF_CONFIGS}
ADD ./container ${SELF_CONTAINER}

RUN chmod 777 -R ${SELF_HOME}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive ${BUILD_SCRIPT}

RUN printenv 

HEALTHCHECK --interval=10s --timeout=3600s --start-period=150s --retries=3 CMD ${HEALTHCHECK_SCRIPT}

CMD ["sh", "-c", "/bin/bash ${START_SCRIPT}"]

