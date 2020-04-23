FROM ubuntu:18.04
COPY ./deployment.sh /tmp/build.sh

RUN apt-get update && apt-get install -y gnupg2

ENV PROFILE_PATH="/etc/profile"
ENV BASHRC_PATH="/root/.bashrc"

ENV GOROOT="/usr/local/go"
ENV GOPATH="/home/go"
ENV GOBIN="/home/bin"
ENV GO_VERSION="1.14"
ENV PATH="/root/.cargo/bin:${PATH}:${GOBIN}"
ENV RUSTFLAGS="-Ctarget-feature=+aes,+ssse3"

RUN chmod +x /tmp/build.sh
RUN chmod 777 $PROFILE_PATH
RUN chmod 777 $BASHRC_PATH

RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive /tmp/build.sh \
  && rm -rf /var/lib/apt/lists/*

ARG DEBIAN_FRONTEND=noninteractive
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get update && apt-get -qq install -y nodejs && apt-get -qq install -y nginx

RUN npm install -g @angular/cli
RUN npm install -g web3 --unsafe-perm=true --allow-root

RUN git config --global url.https://github.com/.insteadOf git://github.com/

RUN curl -sSf sh.rustup.rs | sh -s -- -y

# Check if cargo is visible
RUN cargo --help
