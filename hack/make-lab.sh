#!/usr/bin/env bash
set -euo pipefail

source hack/libraries/custom-logger.sh -v

source hack/init.sh

python3 tests/populate.py
eok 'Database populated using "tests/integration/fakenames.csv" dataset'

eok 'Development environment successfully initialized'
pushd src/
python3 -m fakenamesservice.asgi
popd
