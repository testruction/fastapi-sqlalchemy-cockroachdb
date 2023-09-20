#!/usr/bin/env bash
set -euo pipefail

pushd src/backend/src/

python3 -m backendservice.load_data \
  --database-engine="sqlite" \
|| popd && exit 1

popd