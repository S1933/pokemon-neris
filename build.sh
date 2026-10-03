#!/usr/bin/env bash
# Build pokered (Pokémon Néris base) on the Pi using Docker.
# RGBDS is built from source inside the container (no sudo needed on the host).
set -euo pipefail

cd "$(dirname "$0")"

docker run --rm -v "$PWD":/src -w /tmp debian:bookworm-slim bash -c '
set -e
apt-get update -qq
apt-get install -y -qq git make cmake g++ libpng-dev bison pkg-config python3 >/dev/null
git clone --depth 1 --branch v1.0.4 https://github.com/gbdev/rgbds.git
cd rgbds
make -j4 >/dev/null 2>&1
make install >/dev/null
cd /src
make -j4
ls -la pokered.gbc pokeblue.gbc
'
