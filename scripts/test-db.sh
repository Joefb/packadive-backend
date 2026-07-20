#!/bin/bash
set -e
CONTAINER_NAME="packadive-test-postgres"
IMAGE="postgres:16"
NETWORK="packadive-test-net"
PORT="${TEST_DB_PORT:-5433}"
DB_NAME="${TEST_DB_NAME:-packadive_test}"
DB_USER="${TEST_DB_USER:-packadive}"
DB_PASSWORD="${TEST_DB_PASSWORD:-packadive}"

case "$1" in
  up)
    podman network create "$NETWORK" 2>/dev/null || true
    podman run -d --name "$CONTAINER_NAME" \
      --network "$NETWORK" \
      -e POSTGRES_USER="$DB_USER" \
      -e POSTGRES_PASSWORD="$DB_PASSWORD" \
      -e POSTGRES_DB="$DB_NAME" \
      -p "$PORT:5432" \
      "$IMAGE"
    ;;
  down)
    podman stop "$CONTAINER_NAME"
    podman rm "$CONTAINER_NAME"
    ;;
  reset)
    podman stop "$CONTAINER_NAME" 2>/dev/null || true
    podman rm "$CONTAINER_NAME" 2>/dev/null || true
    "$0" up
    ;;
  *)
    echo "Usage: $0 {up|down|reset}"
    exit 1
    ;;
esac
