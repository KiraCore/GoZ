FROM kiracore/goz:gaia-ibc-alpha
COPY ./deployment.sh /tmp/build.sh
COPY ./start.sh /root/start.sh
COPY ./validator.key /root/validator.key

ENV SENTRY_SCRIPS=/root/scripts/sentry
ENV SENTRY_CONFIGS=/root/configs/sentry

ADD ./scripts ${SENTRY_SCRIPS}
ADD ./configs ${SENTRY_CONFIGS}

RUN chmod +x /tmp/build.sh
RUN chmod +x /root/start.sh
RUN chmod 777 /root/validator.key
RUN chmod 777 -R ${SENTRY_SCRIPS}
RUN chmod 777 -R ${SENTRY_CONFIGS}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh

RUN printenv 

CMD [ "/bin/bash","/root/start.sh" ]

