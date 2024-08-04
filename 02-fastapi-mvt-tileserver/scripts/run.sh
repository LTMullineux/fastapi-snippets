#!/bin/bash

set -e

ENV=$1
shift
DOCKER_ARGS="$*"

trap ctrl_c INT
trap ctrl_c SIGTERM

function ctrl_c() {
    echo "Gracefully hutting down containers ..."
    docker compose --profile $ENV down --volumes
    exit 0
}

docker compose --profile $ENV up $DOCKER_ARGS
