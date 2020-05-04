FROM kiracore/goz:relayer-alpha

#ADD ./scripts ${SELF_SCRIPS}
#ADD ./configs ${SELF_CONFIGS}
ADD ./container ${SELF_CONTAINER}

RUN chmod 777 -R ${SELF_HOME}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive ${BUILD_SCRIPT}

RUN printenv 

CMD ["sh", "-c", "/bin/bash ${START_SCRIPT}"]

