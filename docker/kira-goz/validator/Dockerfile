FROM kiracore/goz:relayer-alpha

#ADD ./scripts ${SELF_SCRIPTS}
#ADD ./configs ${SELF_CONFIGS}
ADD ./container ${SELF_CONTAINER}

RUN chmod 777 -R ${SELF_HOME}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive ${BUILD_SCRIPT}

RUN printenv

HEALTHCHECK --interval=60s --timeout=600s --start-period=300s --retries=3 CMD ${HEALTHCHECK_SCRIPT} $> ${SELF_LOGS}/healthcheck_script_output.txt

CMD ["sh", "-c", "/bin/bash ${START_SCRIPT}"]

