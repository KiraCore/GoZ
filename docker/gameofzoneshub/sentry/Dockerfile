FROM kiracore/goz:gaia-ibc-alpha

ENV SENTRY_SCRIPS=/root/scripts/sentry
ENV SENTRY_CONFIGS=/root/configs/sentry
ENV START_SCRIPT=${SENTRY_SCRIPS}/start.sh

ADD ./scripts ${SENTRY_SCRIPS}
ADD ./configs ${SENTRY_CONFIGS}

RUN chmod 777 /root/validator.key
RUN chmod 777 -R ${SENTRY_SCRIPS}
RUN chmod 777 -R ${SENTRY_CONFIGS}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh

RUN printenv 

CMD [ "/bin/bash", ${START_SCRIPT} ]

