#!/bin/bash

exec 2>&1
set -e
set -x

cat > /etc/apt/sources.list <<EOF
deb http://archive.ubuntu.com/ubuntu/ xenial main universe
deb http://archive.ubuntu.com/ubuntu/ xenial-security main universe
deb http://archive.ubuntu.com/ubuntu/ xenial-updates main universe
deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main
EOF

echo "APT Update, Upfrade and Intall..."
apt-get update
apt-get upgrade -y --force-yes
apt-get install -y --force-yes \
    apt-transport-https \
    apt-utils \
	build-essential \
    bind9-host \
    bzip2 \
    coreutils \
    curl \
    clang \
    cmake \
    dnsutils \
    ed \
    gcc \
    git \
    htop \
    imagemagick \
    iputils-tracepath \
    jq \
    language-pack-en \
    libcurl3 \
    libev4 \
    libevent-2.0-5 \
    libevent-core-2.0-5 \
    libevent-extra-2.0-5 \
    libevent-openssl-2.0-5 \
    libevent-pthreads-2.0-5 \
    libexif12 \
    libgd3 \
    libgnutls-openssl27 \
    libgnutlsxx28 \
    libmcrypt4 \
    libmemcached11 \
    libmysqlclient20 \
    librabbitmq4 \
    libseccomp2 \
    libsodium18 \
    libuv1 \
    libxslt1.1 \
    libzip4 \
    libssl-dev \
    libudev-dev \
    libunwind-dev \
    locales \
    make \
    netcat-openbsd \
    openssh-client \
    openssh-server \
    pkg-config \
    python \
    rename \
    socat \
    sshfs \
    stunnel \
    syslinux \
    tar \
    telnet \
    tzdata \
    unzip \
    wget \
    wipe \
    yarn \
    zip

apt install -y --force-yes npm
npm install -g n && n stable

chmod +x -R /etc/env

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
