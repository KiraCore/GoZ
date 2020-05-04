FROM kiracore/goz:relayer-alpha

ENV VALIDATOR_HOME=/root/valiator
ENV VALIDATOR_SCRIPS=${VALIDATOR_HOME}/scripts
ENV VALIDATOR_CONFIGS=${VALIDATOR_HOME}/configs
ENV CONTAINER_SCRIPTS=${VALIDATOR_HOME}/container

ENV START_SCRIPT=${CONTAINER_SCRIPTS}/start.sh
ENV BUILD_SCRIPT=${CONTAINER_SCRIPTS}/deployment.sh
ENV VALIDATOR_SELF_KEY_PATH=${VALIDATOR_CONFIGS}/validator.key

ENV DENOM=ukex
ENV CHAINID=kira-alpha
ENV DOMAIN=alpha.kiraex.com
ENV RLYKEY=faucet
ENV RLYTRUSTING="10m"

#ADD ./scripts ${VALIDATOR_SCRIPS}
ADD ./configs ${VALIDATOR_CONFIGS}
ADD ./container ${CONTAINER_SCRIPTS}

RUN chmod 777 -R ${VALIDATOR_HOME}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive ${BUILD_SCRIPT}

RUN printenv 

CMD ["sh", "-c", "/bin/bash ${START_SCRIPT}"]

################################################################

FROM kiracore/goz:relayer-alpha

ENV DENOM=ukex
ENV CHAINID=kira-1
ENV DOMAIN=goz.kiraex.com
ENV RLYKEY=faucet
ENV RLYTRUSTING="90m"

#ADD ./scripts ${SELF_SCRIPS}
ADD ./configs ${SELF_CONFIGS}
ADD ./container ${SELF_CONTAINER}

RUN chmod 777 -R ${SELF_HOME}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive ${BUILD_SCRIPT}

RUN printenv 

CMD ["sh", "-c", "/bin/bash ${START_SCRIPT}"]

