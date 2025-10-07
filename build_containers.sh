#!/bin/bash

set -ex

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DATE=$(date +%Y%m%d)
PLATFORM=$(uname -m)
if [[ "$PLATFORM" == "arm64" ]]; then
    PLATFORM="aarch64"
fi
echo "Detected platform: $PLATFORM"

build_docker_image() {
    local folder=$1
    local image_name=toan2/$1_$PLATFORM
    
    if [[ -z "$folder" ]]; then
        echo "Usage: build_docker_image <folder>"
        exit 1
    fi

    cd $SCRIPT_DIR/containers/$folder
    docker build --build-arg PLATFORM=$PLATFORM -t "$image_name" .
}

build_docker_image manylinux_2_34
