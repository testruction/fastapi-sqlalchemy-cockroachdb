#!/usr/bin/env bash

function logger
{
    echo "CONFIG - [${BASH_SOURCE[0]}] - ${1}"
}

logger "Application version: ${APP_VERSION}"
logger "Runtime version: $(python3 --version)"

export RUN_ID=${RUN_ID:-$(echo $RANDOM | sha256sum | head -c 16; echo)}
logger "Run identifier: ${RUN_ID}"
logger "Database engine: \"${DATABASE_ENGINE}\""

if [ "${DATABASE_ENGINE}" == "sqlite" ]
then
  logger "Loading dataset to \"${DATABASE_ENGINE}\" database"
  
  python3 -m backendservice.load_data \
    --database-engine "sqlite"
fi

# Run CMD instruction
exec "$@"