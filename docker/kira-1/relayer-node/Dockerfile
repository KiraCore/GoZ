FROM kiracore/goz:relayer-alpha
COPY ./deployment.sh /tmp/build.sh
COPY ./start.sh /root/start.sh
COPY ./kira-1.json /root/kira-1.json

ENV CHAINID=kira-1
ENV RLYKEY=testkey
ENV BASECHAIN_JSON_PATH=/root/kira-1.json



RUN chmod +x /tmp/build.sh
RUN chmod +x /root/start.sh
RUN chmod a+r,a+w /root/kira-1.json

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh

CMD [ "/bin/bash","/root/start.sh" ]

