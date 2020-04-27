#!/bin/bash

exec 2>&1
set -e
set -x

echo "APT Update, Upfrade and Intall..."
apt-get update
apt-get upgrade -y --force-yes
apt-get install -y --allow-unauthenticated --allow-downgrades --allow-remove-essential --allow-change-held-packages --force-yes \
    apt-transport-https \
    autoconf \
    automake \
    apt-utils \
    build-essential \
    bind9-host \
    bzip2 \
    ca-certificates \
    coreutils \
    curl \
    clang \
    cmake \
    dnsutils \
    dpkg-dev \
    ed \
    file \
    gcc \
    g++ \
    git \
    gnupg \
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
    nodejs-dev \
    node-gyp \
    openssh-client \
    openssh-server \
    pkg-config \
    python \
    patch \
    procps \
    rename \
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

echo "Creating GIT simlink"
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

echo "Installing custom systemctl..."
wget https://raw.githubusercontent.com/gdraheim/docker-systemctl-replacement/master/files/docker/systemctl.py -O /usr/local/bin/systemctl2
chmod -v 777 /usr/local/bin/systemctl2

systemctl2 --version

echo "Installing CDHelper..."
CDHelperVersion="v0.5.0" && \
 cd /usr/local/src && \
 rm -f -v ./CDHelper-linux-x64.zip && \
 wget https://github.com/asmodat/CDHelper/releases/download/$CDHelperVersion/CDHelper-linux-x64.zip && \
 rm -rfv /usr/local/bin/CDHelper && \
 unzip CDHelper-linux-x64.zip -d /usr/local/bin/CDHelper && \
 chmod -R -v 555 /usr/local/bin/CDHelper

CDHelper version

echo "NGINX Setup..."

cat > $NGINX_CONFIG << EOL
worker_processes 1;
events { worker_connections 512; }
http { 
#server{} 
}
#EOF
EOL

mkdir -v /etc/systemd/system/nginx.service.d
printf "[Service]\nExecStartPost=/bin/sleep 0.1\n" > /etc/systemd/system/nginx.service.d/override.conf

systemctl2 enable nginx.service


