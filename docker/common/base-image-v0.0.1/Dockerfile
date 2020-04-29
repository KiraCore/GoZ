FROM ubuntu:18.04
COPY ./deployment.sh /tmp/build.sh

RUN apt-get update && apt-get install -y gnupg2

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
ENV SCRIPTS_DIR=/root/scripts

RUN mkdir -p ${GOPATH}/src ${GOPATH}/bin ${SCRIPTS_DIR}
ADD ./scripts ${SCRIPTS_DIR}

RUN chmod +x /tmp/build.sh
RUN chmod 777 $PROFILE_PATH
RUN chmod 777 $BASHRC_PATH
RUN chmod -R 777 ${SCRIPTS_DIR}

ARG DEBIAN_FRONTEND=noninteractive
RUN LC_ALL=C /tmp/build.sh \
  && rm -rf /var/lib/apt/lists/*

#RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
#RUN apt-get update && apt-get -qq install -y nodejs

RUN npm install -g @angular/cli
RUN npm install -g web3 --unsafe-perm=true --allow-root

RUN git config --global url.https://github.com/.insteadOf git://github.com/

# Update new packages
RUN apt-get update

# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

# Check if cargo is visible
RUN cargo --version 

# Check go version and environment
RUN echo $PATH
RUN go version
RUN go env

# Install Asmodat Helper tools
RUN ${SCRIPTS_DIR}/awshelper-update-v0.0.1.sh "v0.12.0" 
RUN ${SCRIPTS_DIR}/cdhelper-update-v0.0.1.sh "v0.5.0" 
ENV AWSHelperVersion="v0.12.0"
ENV CDHelperVersion="v0.5.0"



