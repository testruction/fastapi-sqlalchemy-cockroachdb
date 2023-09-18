#!/usr/bin/env bash

helm upgrade --install \
  --create-namespace \
  --namespace fastapi-demo \
  --set cockroachdb.statefulset.replicas="1" \
  --set cockroachdb.service.public.type="LoadBalancer" \
  --set cockroachdb.storage.persistentVolume.size="1Gi" \
  --set backend.service.type="LoadBalancer" \
  --set backend.serviceMonitor.enabled="true" \
  --set frontend.service.type="LoadBalancer" \
  --set frontend.serviceMonitor.enabled="true" \
  demo ./chart/

kubectl label namespace fastapi-demo "prometheus=enabled"