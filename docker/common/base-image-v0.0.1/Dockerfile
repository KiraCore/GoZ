FROM ubuntu:18.04

ENV PROFILE_PATH="/etc/profile"
ENV BASHRC_PATH="/root/.bashrc"

ENV GOROOT="/usr/local/go"
ENV GOPATH="/home/go"
ENV GOBIN="${GOROOT}/bin"
ENV GO_VERSION="1.14"
ENV DOTNET_ROOT="/usr/bin/dotnet"
ENV PATH="/root/.cargo/bin:${PATH}:${GOBIN}:${GOROOT}:${GOPATH}:/usr/local/bin/CDHelper:/usr/local/bin/AWSHelper"
ENV RUSTFLAGS="-Ctarget-feature=+aes,+ssse3"
ENV GO111MODULE=on
ENV NGINX_CONFIG="/etc/nginx/nginx.conf"
ENV NGINX_SERVICED_PATH="/etc/systemd/system/nginx.service.d"

# Env necessary for the individual child container setup
ENV SELF_HOME=/self/home
ENV SELF_SCRIPS=${SELF_HOME}/scripts
ENV SELF_CONFIGS=${SELF_HOME}/configs
ENV SELF_UPDATE=${SELF_HOME}/update
ENV SELF_UPDATE_TMP=${SELF_HOME}/tmp/update
ENV SELF_CONTAINER=${SELF_HOME}/container
ENV START_SCRIPT=${SELF_CONTAINER}/start.sh
ENV BUILD_SCRIPT=${SELF_CONTAINER}/deployment.sh
ENV HEALTHCHECK_SCRIPT=${SELF_CONTAINER}/healthcheck.sh
ENV ON_FAILURE_SCRIPT=${SELF_CONTAINER}/on_failure.sh
ENV ON_INIT_SCRIPT=${SELF_CONTAINER}/on_init.sh
ENV ON_SUCCESS_SCRIPT=${SELF_CONTAINER}/on_success.sh
ENV INIT_START_FILE=${SELF_HOME}/init_start
ENV INIT_END_FILE=${SELF_HOME}/init_end
ENV FAILURE_START_FILE=${SELF_HOME}/failure_start
ENV FAILURE_END_FILE=${SELF_HOME}/failure_end
ENV SUCCESS_START_FILE=${SELF_HOME}/success_start
ENV SUCCESS_END_FILE=${SELF_HOME}/success_end
ENV MAINTENANCE_FILE=${SELF_HOME}/maintenence

RUN mkdir -p ${SELF_HOME} ${SELF_SCRIPS} ${SELF_CONFIGS} ${SELF_UPDATE} ${SELF_UPDATE_TMP} ${SELF_CONTAINER} ${GOPATH}/src ${GOPATH}/bin

ADD ./scripts ${SELF_SCRIPS}
#ADD ./configs ${SELF_CONFIGS}
ADD ./container ${SELF_CONTAINER}

# TODO: Remove - Logacy Dir
RUN chmod -R 777 ${SELF_HOME} && chmod 777 ${PROFILE_PATH} && chmod 777 ${BASHRC_PATH}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C ${BUILD_SCRIPT} && rm -rf /var/lib/apt/lists/*

