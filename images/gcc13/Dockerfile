FROM ubuntu:24.04

LABEL maintainer="Conan.io <info@conan.io>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -qq update \
    && apt-get -qq install -y --no-install-recommends --no-install-suggests \
       binutils \
       git \
       pkg-config \
       cmake \
       make \
       ca-certificates \
       python3 \
       python3-dev \
       pipx \
       gcc \
       g++ \
       libc6-dev \
       vim \
       wget \
       bison \
       gawk \
       sudo \
       xz-utils \
       adduser

RUN rm -rf /var/lib/apt/lists/*

RUN groupadd -f conan-1001 -g 1001 \
    && groupadd -f conan-1000 -g 1000 \
    && groupadd -f conan-2000 -g 2000 \
    && groupadd -f conan-999 -g 999 \
    && useradd -ms /bin/bash conan -g 1001 -G 1000,2000,999 \
    && printf "conan:conan" | chpasswd \
    && adduser conan sudo \
    && printf "conan ALL= NOPASSWD: ALL\\n" >> /etc/sudoers

USER conan
WORKDIR /home/conan
ENV PATH="/home/conan/.local/bin:${PATH}"

ARG CONAN_VERSION=2.23.0

RUN pipx install conan==${CONAN_VERSION} ninja \
    && conan profile detect \
    && echo "core.sources:download_cache=/home/conan/.conan2/download_cache" >> /home/conan/.conan2/global.conf \
    && echo 'core.sources:download_urls=["origin", "https://c3i.jfrog.io/artifactory/conan-center-backup-sources/"]' >> /home/conan/.conan2/global.conf \
    && echo "[conf]\ntools.cmake.cmaketoolchain:generator=Ninja\ntools.build:verbosity=verbose\ntools.compilation:verbosity=verbose\ntools.system.package_manager:sudo=true\ntools.system.package_manager:mode=install" >> /home/conan/.conan2/profiles/default
