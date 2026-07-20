#!/bin/bash
set -e
IMAGE_NAME="packadive-backend:test"
CONTAINER_NAME="packadive-test-app"
DB_CONTAINER_NAME="packadive-test-postgres"
NETWORK="packadive-test-net"
APP_PORT="${TEST_APP_PORT:-8000}"
DB_NAME="${TEST_DB_NAME:-packadive_test}"
DB_USER="${TEST_DB_USER:-packadive}"
DB_PASSWORD="${TEST_DB_PASSWORD:-packadive}"

case "$1" in
  build)
    podman build -t "$IMAGE_NAME" .
    ;;
  up)
    podman run -d --name "$CONTAINER_NAME" \
      --network "$NETWORK" \
      -e SECRET_KEY="${SECRET_KEY:-dev-secret}" \
      -e SQLALCHEMY_DATABASE_URI="postgresql://$DB_USER:$DB_PASSWORD@$DB_CONTAINER_NAME:5432/$DB_NAME" \
      -p "$APP_PORT:8000" \
      "$IMAGE_NAME"
    ;;
  down)
    podman stop "$CONTAINER_NAME"
    podman rm "$CONTAINER_NAME"
    ;;
  logs)
    podman logs -f "$CONTAINER_NAME"
    ;;
  *)
    echo "Usage: $0 {build|up|down|logs}"
    exit 1
    ;;
esac
