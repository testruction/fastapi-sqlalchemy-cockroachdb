#!/usr/bin/env bash
set -euo pipefail

pushd src/backend/src/

python3 -m backendservice.load_data \
  --database-host="localhost" \
  --database-port="26257" \
  --username "admin" \
|| popd && exit 1

popd
