#!/usr/bin/env bats
setup() {
  BACKEND_HOST="localhost"
  BACKEND_PORT="8001"
  FRONTEND_HOST="localhost"
  FRONTEND_PORT="8000"
}

@test "Check backend API" {
  curl --retry 3 --fail "http://${BACKEND_HOST}:${BACKEND_PORT}/health"
  curl --retry 3 --fail "http://${BACKEND_HOST}:${BACKEND_PORT}/v1/fakenames/postgres?limit=5"
}

@test "Check frontend UI" {
  curl --retry 3 --fail "http://${FRONTEND_HOST}:${FRONTEND_PORT}/health"
  curl --retry 3 --fail "http://${FRONTEND_HOST}:${FRONTEND_PORT}/status"
  curl --retry 3 --fail "http://${FRONTEND_HOST}:${FRONTEND_PORT}/"
}