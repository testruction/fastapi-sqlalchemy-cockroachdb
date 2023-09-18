#!/usr/bin/env bash

helm upgrade --install \
  --create-namespace \
  --namespace fastapi-demo \
  --set cockroachdb.statefulset.replicas="1" \
  --set cockroachdb.service.public.type="NodePort" \
  --set cockroachdb.storage.persistentVolume.size="1Gi" \
  --set backend.service.type="NodePort" \
  --set backend.serviceMonitor.enabled="true" \
  --set frontend.service.type="NodePort" \
  --set frontend.serviceMonitor.enabled="true" \
  demo ./chart/