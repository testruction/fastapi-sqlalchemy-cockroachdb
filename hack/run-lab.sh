#!/usr/bin/env bash
set -euo pipefail

source hack/libraries/custom-logger.sh -v

if [ ! -f .env ]
then
    ewarn 'Environment ".env" file not found'
    ewarn 'Creating using default settings from ".env.example"'
    cp .env.example .env
fi

set -o allexport
source .env
set +o allexport
eok 'Environment variables initialized'

docker compose up --detach --quiet-pull --remove-orphans
eok "CockroachDB and Jager started"
sleep 5
docker compose exec roach1 sh -c 'cockroach sql --execute="SELECT VERSION()" --insecure || cockroach init --insecure'
eok "Cockroachdb cluster \"http://localhost:8080\" initialized"


python3 -m venv .venv/
source .venv/bin/activate
python3 -m pip install --upgrade pip --quiet
pip3 install -r requirements.txt --quiet
eok 'Pythond virtual environment initialized'

python3 tests/populate.py
eok 'Database populated using "tests/integration/fakenames.csv" dataset'

eok 'Development environment successfully initialized'
pushd src/
python3 -m fakenamesservice.asgi
popd
