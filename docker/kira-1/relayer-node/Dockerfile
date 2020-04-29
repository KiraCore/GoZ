FROM kiracore/goz:relayer-alpha
COPY ./deployment.sh /tmp/build.sh
COPY ./start.sh /root/start.sh
COPY ./kira-1.json /root/kira-1.json
ADD ./scripts /root/scripts/relay

ENV CHAINID=kira-1
ENV RLYKEY=testkey
ENV BASECHAIN_JSON_PATH=/root/kira-1.json
ENV RELAY_SCRIPS=/root/scripts/relay

RUN mkdir -p ${RELAY_SCRIPS}

RUN chmod +x /tmp/build.sh
RUN chmod +x /root/start.sh
RUN chmod a+r,a+w /root/kira-1.json
RUN chmod 777 -R ${RELAY_SCRIPS}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh

CMD [ "/bin/bash","/root/start.sh" ]

