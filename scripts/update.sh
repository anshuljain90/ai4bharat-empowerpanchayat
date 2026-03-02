#!/bin/bash
# =============================================================
# eGramSabha — Update / Redeploy Script
# =============================================================
# Pull latest code and rebuild.
# Usage:
#   bash scripts/update.sh              # rebuild all
#   bash scripts/update.sh backend      # rebuild only backend
#   bash scripts/update.sh frontend     # rebuild only frontend
# =============================================================

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SERVICE="$1"

cd "$PROJECT_DIR"

echo "========================================="
echo "  eGramSabha Update"
echo "========================================="

# --- Pull latest code ---
echo ""
echo "Pulling latest code..."
git pull origin main

# --- Rebuild ---
if [ -z "$SERVICE" ]; then
    echo ""
    echo "Rebuilding ALL services..."
    docker-compose -f docker-compose.prod.yml up -d --build
else
    echo ""
    echo "Rebuilding: $SERVICE"
    docker-compose -f docker-compose.prod.yml up -d --build "$SERVICE"
fi

# --- Cleanup old images ---
echo ""
echo "Cleaning up old Docker images..."
docker image prune -f

# --- Status ---
echo ""
echo "Current container status:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "========================================="
echo "  Update Complete!"
echo "========================================="
