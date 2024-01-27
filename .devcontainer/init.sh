#!/bin/bash

set -euo pipefail

ARCH=$(uname -m | grep 'x86_64' > /dev/null && echo 'amd64' || echo 'arm64')

drawio_version=23.0.2
drawio_deb="drawio-${ARCH}-${drawio_version}.deb"
drawio_url="https://github.com/jgraph/drawio-desktop/releases/download/v${drawio_version}/${drawio_deb}"
curl -L -o "/tmp/$drawio_deb" "$drawio_url"
sudo apt-get update && sudo apt-get install -y libasound2 xvfb "/tmp/$drawio_deb"

poetry install && echo 'source .venv/bin/activate' >> $HOME/.bashrc