FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    apt-utils \
    bison \
    ca-certificates \
    ccache \
    check \
    curl \
    flex \
    git \
    gperf \
    lcov \
    libffi-dev \
    libncurses-dev \
    libusb-1.0-0-dev \
    make \
    ninja-build \
    libpython2.7 \
    python3 \
    python3-pip \
    unzip \
    wget \
    xz-utils \
    zip \
   && apt-get autoremove -y \
   && rm -rf /var/lib/apt/lists/* \
   && update-alternatives --install /usr/bin/python python /usr/bin/python3 10

RUN python -m pip install --upgrade pip virtualenv

ARG SSH_PRIVATE_KEY
RUN mkdir -m 700 /root/.ssh/ \
    && echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa \
    && chmod 600 /root/.ssh/id_rsa \
    && touch -m 600 /root/.ssh/known_hosts \
    && echo "Host glab.espressif.cn" > /root/.ssh/config \
    && echo "    StrictHostKeyChecking no" >> /root/.ssh/config

ARG IDF_CLONE_URL=ssh://git@glab.espressif.cn:8266/technical_support/signify/esp-idf-signify.git
ARG IDF_CHECKOUT_REF=

ENV IDF_PATH=/opt/esp/idf

RUN echo IDF_CHECKOUT_REF=$IDF_CHECKOUT_REF && \
    git clone $IDF_CLONE_URL $IDF_PATH && \
    cd $IDF_PATH && \
    git checkout $IDF_CHECKOUT_REF && \
    sed -i 's/https:\/\/glab.espressif.cn/ssh:\/\/git@glab.espressif.cn:8266/g' .gitmodules && \
    git submodule update --init --recursive && \
    rm -rf /root/.ssh 

#can be done when docker build
RUN python -m pip install --user -r $IDF_PATH/requirements.txt
ENV TOOLCHAIN_TARBALL=xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz
ENV TOOLCHAIN_PATH=/opt/xtensa-esp32-elf/bin

RUN wget https://dl.espressif.com/dl/$TOOLCHAIN_TARBALL -P /opt && \
    tar -xzf /opt/$TOOLCHAIN_TARBALL -C /opt && \
    rm -rf /opt/$TOOLCHAIN_TARBALL


#docker build script
#ENV BATCH_BUILD=1
#ENV PATH=$PATH:$TOOLCHAIN_PATH