FROM kiracore/goz:relayer-alpha
COPY ./deployment.sh /tmp/build.sh
COPY ./start.sh /root/start.sh

ENV RELAY_SCRIPS=/root/scripts/relay
ENV RELAY_CONFIGS=/root/configs/relay
ENV BASECHAIN_JSON_PATH=${RELAY_CONFIGS}/kira-alpha.json
ENV GOZCHAIN_JSON_PATH=${RELAY_CONFIGS}/kira-1.json
ENV RLY_REPO="https://github.com/iqlusioninc/relayer"
ENV RLY_BRANCH="master"
ENV RLY_CHECKOUT=""
ENV RLY_OUTPUT=/tmp/rly
ENV RLYS_SOURCE=${RLY_OUTPUT}/testnets/relayer-alpha-2
ENV RLYS_HOME=/root/relayers
ENV BUCKET="kira-core-alpha"

ADD ./scripts ${RELAY_SCRIPS}
ADD ./configs ${RELAY_CONFIGS}

# store the repo content to acquire json files
RUN ${SCRIPTS_DIR}/git-pull-v0.0.1.sh "${RLY_REPO}" "${RLY_BRANCH}" "${RLY_CHECKOUT}" "${RLY_OUTPUT}"

RUN rm -rfv $RLYS_HOME && cp -avr $RLYS_SOURCE $RLYS_HOME

RUN chmod +x /tmp/build.sh
RUN chmod +x /root/start.sh
RUN chmod 777 -R ${RELAY_SCRIPS}
RUN chmod 777 -R ${RELAY_CONFIGS}
RUN chmod 777 -R ${RLYS_HOME}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh

CMD [ "/bin/bash","/root/start.sh" ]

