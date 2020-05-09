#!/bin/bash

exec 2>&1
set -e
set -x

apt-get -y update
apt-get install -y apt-transport-https ca-certificates gnupg curl

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

echo "APT Update, Upfrade and Intall..."
apt-get update
apt-get upgrade -y --force-yes
apt-get install -y --allow-unauthenticated --allow-downgrades --allow-remove-essential --allow-change-held-packages --force-yes \
    autoconf \
    automake \
    apt-utils \
    awscli \
    build-essential \
    bind9-host \
    bzip2 \
    coreutils \
    clang \
    cmake \
    dnsutils \
    dpkg-dev \
    ed \
    file \
    gcc \
    g++ \
    git \
    gnupg2 \
    groff \
    htop \
    imagemagick \
    iputils-tracepath \
    iputils-ping \
    jq \
    language-pack-en \
    libtool \
    libzip4 \
    libssl1.0-dev \
    libudev-dev \
    libunwind-dev \
    libusb-1.0-0-dev \
    locales \
    make \
    nano \
    nginx \
    netbase \
    netcat-openbsd \
    net-tools \
    nodejs \
    nodejs-dev \
    node-gyp \
    openssh-client \
    openssh-server \
    pkg-config \
    python \
    patch \
    procps \
    python3 \
    python3-pip \
    rename \
    rsync \
    socat \
    sshfs \
    stunnel \
    subversion \
    syslinux \
    tar \
    telnet \
    tzdata \
    unzip \
    wget \
    wipe \
    yarn \
    zip

# https://linuxhint.com/install_aws_cli_ubuntu/
aws --version

echo "Intalling NPM..."
apt-get install -y --allow-unauthenticated --force-yes \
    npm
npm install -g n
n stable

echo "APT Intall Rust Dependencies..."
apt-get install -y --allow-unauthenticated --force-yes \
    libc6-dev \
    libbz2-dev \
    libcurl4-openssl-dev \
    libdb-dev \
    libevent-dev \
    libffi-dev \
    libgdbm-dev \
    libglib2.0-dev \
    libgmp-dev \
    libjpeg-dev \
    libkrb5-dev \
    liblzma-dev \
    libmagickcore-dev \
    libmagickwand-dev \
    libmaxminddb-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libpng-dev \
    libpq-dev \
    libreadline-dev \
    libsqlite3-dev \
    libwebp-dev \
    libxml2-dev \
    libxslt-dev \
    libyaml-dev \
    xz-utils \
    zlib1g-dev

echo "Creating GIT simlink and global setup"
ln -s /usr/bin/git /bin/git

which git
/usr/bin/git --version

echo "Installing .NET"
wget -q https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
dpkg -i packages-microsoft-prod.deb
apt-get update
apt-get install -y aspnetcore-runtime-3.1
apt-get install -y dotnet-sdk-2.1
apt-get install -y dotnet-sdk-3.1

echo "Installing latest go version $GO_VERSION https://golang.org/doc/install ..."
wget https://dl.google.com/go/go$GO_VERSION.linux-amd64.tar.gz
tar -C /usr/local -xvf go$GO_VERSION.linux-amd64.tar.gz
go version
go env

echo "Installing custom systemctl..."
wget https://raw.githubusercontent.com/gdraheim/docker-systemctl-replacement/master/files/docker/systemctl.py -O /usr/local/bin/systemctl2
chmod -v 777 /usr/local/bin/systemctl2

systemctl2 --version

echo "NGINX Setup..."

cat > $NGINX_CONFIG << EOL
worker_processes 1;
events { worker_connections 512; }
http { 
#server{} 
}
#EOF
EOL

mkdir -v $NGINX_SERVICED_PATH
printf "[Service]\nExecStartPost=/bin/sleep 0.1\n" > $NGINX_SERVICED_PATH/override.conf

systemctl2 enable nginx.service

echo "Install Asmodat Automation helper tools"
${SELF_SCRIPTS}/awshelper-update-v0.0.1.sh "v0.12.0"
AWSHelper version

${SELF_SCRIPTS}/cdhelper-update-v0.0.1.sh "v0.6.0"
CDHelper version

printenv

