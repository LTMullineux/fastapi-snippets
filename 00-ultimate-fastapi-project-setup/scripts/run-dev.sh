#!/bin/bash

set -e

DOCKER_ARGS="$*"

trap ctrl_c INT
trap ctrl_c SIGTERM

function ctrl_c() {
    echo "Gracefully hutting down containers ..."
    docker compose --profile dev down --volumes
    exit 0
}

docker compose --profile dev up $DOCKER_ARGS
