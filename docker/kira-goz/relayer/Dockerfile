FROM kiracore/goz:relayer-alpha
COPY ./deployment.sh /tmp/build.sh
COPY ./start.sh /root/start.sh

ENV RELAY_SCRIPS=/root/scripts/relay
ENV RELAY_CONFIGS=/root/configs/relay
ENV BASECHAIN_JSON_PATH=${RELAY_CONFIGS}/kira-1.json
ENV RLYS_HOME=/root/relayers
ENV BUCKET="kira-core-goz"

ADD ./scripts ${RELAY_SCRIPS}
ADD ./configs ${RELAY_CONFIGS}

RUN mkdir -p -v ${RLYS_HOME}

RUN chmod +x /tmp/build.sh
RUN chmod +x /root/start.sh
RUN chmod 777 -R ${RELAY_SCRIPS}
RUN chmod 777 -R ${RELAY_CONFIGS}
RUN chmod 777 -R ${RLYS_HOME}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh

RUN printenv 

CMD [ "/bin/bash","/root/start.sh" ]

