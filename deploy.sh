#!/bin/bash
set -e

REPO_DIR="/home/joefb/services/packadive-backend"
LOG_FILE="$REPO_DIR/deploy.log"

exec >>"$LOG_FILE" 2>&1

cd "$REPO_DIR"

git fetch origin main

LOCAL=$(git rev-parse main)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "$(date): New changes detected on main. Deploying..."
  git pull origin main
  podman build -t packadive-backend:latest .
  systemctl --user restart container-packadive-api.service
  echo "$(date): Deploy complete."
else
  echo "$(date): No changes."
fi
