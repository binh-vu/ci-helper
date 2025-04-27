#!/bin/bash

set -ex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DATE=$(date +%Y%m%d)

build_docker_image() {
    local folder=$1
    local image_name=toan2/$1
    
    if [[ -z "$folder" ]]; then
        echo "Usage: build_docker_image <folder>"
        exit 1
    fi

    cd $SCRIPT_DIR/containers/$folder
    docker build -t "$image_name:$DATE" .
}

PLATFORM=$(uname -m)
if [[ "$PLATFORM" == "arm64" ]]; then
    PLATFORM="aarch64"
fi
echo "Detected platform: $PLATFORM"

build_docker_image manylinux_2_34_$PLATFORM
