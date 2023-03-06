#!/usr/bin/env bash
set -euo pipefail

source hack/libraries/custom-logger.sh -v

function init_env()
{
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
}

function init_venv()
{
    if [ ! -d .venv ]
    then
        python3 -m venv .venv/
    fi

    source .venv/bin/activate

    python3 -m pip install --upgrade pip --quiet
    pip3 install -r requirements.txt --quiet
    eok 'Pythond virtual environment initialized'
}


function start_infrastructure()
{
    docker compose up --detach --quiet-pull --remove-orphans
    eok "CockroachDB and Jager started"
    sleep 5
    docker compose exec roach1 sh -c 'cockroach sql --execute="SELECT VERSION()" --insecure || cockroach init --insecure'
    eok "Cockroachdb cluster \"http://localhost:8080\" initialized"
}


init_env
init_venv
start_infrastructure
