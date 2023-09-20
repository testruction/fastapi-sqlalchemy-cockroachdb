#!/usr/bin/env bash
set -euo pipefail

pushd src/backend/src/

python3 ./tests/populate.py \
  --database-host="localhost" \
  --database-port="26257" \
  --username "admin" || popd && exit 1

popd
