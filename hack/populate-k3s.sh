#!/usr/bin/env bash
set -euo pipefail

NS="${1:-fastapi-demo}"
RN="${2:-demo}"

pushd src/backend/src/

python3 -m backendservice.load_data \
  --database-host="$(kubectl get svc -n ${NS} ${RN}-cockroachdb-public -o jsonpath='{.status.loadBalancer.ingress[0].ip}')" \
  --database-port="$(kubectl get svc -n ${NS} ${RN}-cockroachdb-public -o jsonpath='{.spec.ports[?(@.name == "grpc")].port}')" \
  --username "admin" \
|| popd && exit 1

popd