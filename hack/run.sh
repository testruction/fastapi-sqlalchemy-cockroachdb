#!/usr/bin/env bash

set -o allexport
source .env
set +o allexport

python3 tests/populate_db.py

pushd src/
python3 -m fakenamesservice.asgi
popd