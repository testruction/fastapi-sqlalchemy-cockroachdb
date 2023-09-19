#!/usr/bin/env bash

NS="${1:-fastapi-demo}"
RN="${2:-demo}"

helm upgrade --install \
  --create-namespace \
  --namespace "${NS}" \
  --set cockroachdb.statefulset.replicas="1" \
  --set cockroachdb.service.public.type="LoadBalancer" \
  --set cockroachdb.service.ports.http.port="18280" \
  --set cockroachdb.storage.persistentVolume.size="1Gi" \
  --set backend.service.type="LoadBalancer" \
  --set backend.service.port="18180" \
  --set backend.serviceMonitor.enabled="true" \
  --set frontend.service.type="LoadBalancer" \
  --set frontend.service.port="18080" \
  --set frontend.serviceMonitor.enabled="true" \
  "${RN}" ./chart/

kubectl label namespace "${NS}" "prometheus=enabled"

echo

COCKROACHDB_HOST="$(kubectl get svc -n ${NS} ${RN}-cockroachdb-public -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"
COCKROACHDB_PORT="$(kubectl get svc -n ${NS} ${RN}-cockroachdb-public -o jsonpath='{.spec.ports[?(@.name == "grpc")].port}')"
COCKROACHDB_HTTP="$(kubectl get svc -n ${NS} ${RN}-cockroachdb-public -o jsonpath='{.spec.ports[?(@.name == "http")].port}')"
echo "CockroachDB: \"cockroachdb://${COCKROACHDB_HOST}:${COCKROACHDB_PORT}\""
echo "CockroachDB console: \"http://${COCKROACHDB_HOST}:${COCKROACHDB_HTTP}\""

BACKEND_HOST="$(kubectl get svc -n ${NS} ${RN}-fastapi-backend -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"
BACKEND_HTTP="$(kubectl get svc -n ${NS} ${RN}-fastapi-backend -o jsonpath='{.spec.ports[?(@.name == "http")].port}')"
echo "Rest API doc: \"http://${BACKEND_HOST}:${BACKEND_HTTP}/v1/docs\""

FRONTEND_HOST="$(kubectl get svc -n ${NS} ${RN}-fastapi-frontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"
FRONTEND_HTTP="$(kubectl get svc -n ${NS} ${RN}-fastapi-frontend -o jsonpath='{.spec.ports[?(@.name == "http")].port}')"
echo "Web UI: \"http://${FRONTEND_HOST}:${FRONTEND_HTTP}\""
