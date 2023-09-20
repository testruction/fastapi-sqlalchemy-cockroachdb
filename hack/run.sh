#!/usr/bin/env bash
set -euo pipefail

source hack/libraries/custom-logger.sh -v

source hack/init.sh

hack/populate-docker.sh
eok 'Database populated using "tests/unit/fakenames.csv" dataset'

# export DOCKER_BUILDKIT=1
# docker compose up --build  --remove-orphans
