#!/usr/bin/env bash
#
# Adapted from EttusResearch/uhd .ci/docker/uhd-builder-ubuntu2604.Dockerfile
# https://github.com/EttusResearch/uhd/blob/master/.ci/docker/uhd-builder-ubuntu2604.Dockerfile
#
# Installs the same build dependencies directly on a host machine instead of
# inside a Docker image. Intended for Ubuntu 26.04 (or a close derivative) —
# some package names below are release-specific and may not exist on other
# Ubuntu versions.
#
# This script only installs dependencies. It does NOT clone or build UHD
# itself — see "Next steps" at the bottom.
#
# Usage:
#   chmod +x install-uhd-build-deps.sh
#   sudo ./install-uhd-build-deps.sh
#
# Optional: point pip at a custom index before running, e.g.
#   PIP_INDEX_URL=https://example.org/simple PIP_INDEX_HOST=example.org sudo -E ./install-uhd-build-deps.sh

set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root (e.g. with sudo)." >&2
    exit 1
fi

export DEBIAN_FRONTEND=noninteractive

echo "==> Updating package index and upgrading existing packages..."
apt-get update
apt-get -y upgrade

echo "==> Installing UHD build dependencies..."
apt-get -y install -q \
    build-essential \
    ccache \
    clang \
    curl \
    git \
    sudo \
    abi-dumper \
    cmake \
    doxygen \
    dpdk \
    libboost-all-dev \
    libdpdk-dev \
    libgps-dev \
    libudev-dev \
    libusb-1.0-0-dev \
    ncompress \
    ninja-build \
    python3-dev \
    python3-docutils \
    python3-mako \
    python3-numpy \
    python3-pip \
    python3-requests \
    python3-setuptools \
    pybind11-dev \
    libgrpc++-dev \
    libprotobuf-dev \
    protobuf-compiler-grpc \
    python3-grpcio \
    debootstrap \
    devscripts \
    pbuilder \
    debhelper \
    libncurses5-dev \
    python3-ruamel.yaml \
    python3-sphinx \
    python3-lxml \
    libsdl1.2-dev \
    libgsl-dev \
    libqwt-qt5-dev \
    libqt5opengl5-dev \
    libgmp3-dev \
    libfftw3-dev \
    gir1.2-gtk-3.0 \
    libpango1.0-dev \
    python3-pyqt5 \
    liblog4cpp5-dev \
    libzmq3-dev \
    python3-click \
    python3-click-plugins \
    python3-zmq \
    python3-scipy \
    python3-gi-cairo \
    python3-pygccxml \
    python3-jsonschema \
    libspdlog-dev \
    libsndfile1-dev

# Optional: use a cached/custom pip index if the caller set these env vars.
if [ -n "${PIP_INDEX_URL:-}" ]; then
    echo "==> Configuring pip to use custom index: $PIP_INDEX_URL"
    python3 -m pip config --global set global.index-url "$PIP_INDEX_URL"
    if [ -n "${PIP_INDEX_HOST:-}" ]; then
        python3 -m pip config --global set global.trusted-host "$PIP_INDEX_HOST"
    fi
fi

echo "==> Done. Build dependencies installed."
echo
echo "Next steps to actually build UHD:"
echo "  git clone https://github.com/EttusResearch/uhd.git"
echo "  cd uhd/host"
echo "  mkdir build && cd build"
echo "  cmake -GNinja .."
echo "  ninja"
echo "  sudo ninja install"
echo "  sudo ldconfig"
