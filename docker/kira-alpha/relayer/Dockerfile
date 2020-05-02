FROM kiracore/goz:relayer-alpha

ENV RELAY_HOME=/root/relay
ENV RLYS_HOME=${RELAY_HOME}/relayers
ENV RELAY_SCRIPS=${RELAY_HOME}/scripts
ENV RELAY_CONFIGS=${RELAY_HOME}/configs
ENV CONTAINER_SCRIPTS=${RELAY_HOME}/container
ENV BUILD_SCRIPT=${CONTAINER_SCRIPTS}/deployment.sh
ENV START_SCRIPT=${CONTAINER_SCRIPTS}/start.sh
ENV TESTCHAIN_JSON_PATH=${RELAY_CONFIGS}/kira-alpha.json
ENV GOZCHAIN_JSON_PATH=${RELAY_CONFIGS}/kira-1.json
ENV HUBCHAIN_JSON_PATH=${RELAY_CONFIGS}/goz-hub.json

ENV RLY_REPO="https://github.com/iqlusioninc/relayer"
ENV RLY_BRANCH="master"
ENV RLY_CHECKOUT=""
ENV RLY_OUTPUT=/tmp/rly
ENV RLYS_SOURCE=${RLY_OUTPUT}/testnets/relayer-alpha-2
ENV BUCKET="kira-core-alpha"

ADD ./scripts ${RELAY_SCRIPS}
ADD ./configs ${RELAY_CONFIGS}
ADD ./container ${CONTAINER_SCRIPTS}

# store the repo content to acquire json files
RUN ${SCRIPTS_DIR}/git-pull-v0.0.1.sh "${RLY_REPO}" "${RLY_BRANCH}" "${RLY_CHECKOUT}" "${RLY_OUTPUT}"

RUN rm -rfv $RLYS_HOME && cp -avr $RLYS_SOURCE $RLYS_HOME

RUN chmod 777 -R ${RELAY_HOME}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive ${BUILD_SCRIPT}

RUN printenv 

CMD [ "/bin/bash", ${START_SCRIPT} ]

