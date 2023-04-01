#!/usr/bin/env bash
set -euo pipefail

source make/libraries/custom-logger.sh -v

source make/init.sh

pushd src/backend/src/
python3 tests/populate.py
eok 'Database populated using "tests/unit/fakenames.csv" dataset'
popd

# export DOCKER_BUILDKIT=1
# docker compose up --build  --remove-orphans
