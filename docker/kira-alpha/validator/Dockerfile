FROM kiracore/goz:relayer-alpha
COPY ./deployment.sh /tmp/build.sh
COPY ./start.sh /root/start.sh
COPY ./validator.key /root/validator.key

ENV DENOM=ukex
ENV CHAINID=kira-1
ENV DOMAIN=goz.kiraex.com
ENV RLYKEY=faucet
ENV VALIDATOR_SELF_KEY_PATH=/root/validator.key

RUN chmod +x /tmp/build.sh
RUN chmod +x /root/start.sh
RUN chmod 777 /root/validator.key

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh

CMD [ "/bin/bash","/root/start.sh" ]

