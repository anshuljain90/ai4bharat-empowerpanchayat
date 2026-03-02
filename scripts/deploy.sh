#!/bin/bash
# =============================================================
# eGramSabha — Production Deployment Script
# =============================================================
# Usage: bash scripts/deploy.sh <SERVER_IP_OR_DOMAIN>
#
# Examples:
#   bash scripts/deploy.sh 13.234.56.78
#   bash scripts/deploy.sh gramsabha.yourdomain.com
# =============================================================

set -e

# --- Validate input ---
if [ -z "$1" ]; then
    echo "Error: Server IP or domain is required."
    echo ""
    echo "Usage: bash scripts/deploy.sh <SERVER_IP_OR_DOMAIN>"
    echo ""
    echo "Examples:"
    echo "  bash scripts/deploy.sh 13.234.56.78"
    echo "  bash scripts/deploy.sh gramsabha.yourdomain.com"
    exit 1
fi

SERVER_ADDRESS="$1"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "========================================="
echo "  eGramSabha Production Deployment"
echo "========================================="
echo "Server: $SERVER_ADDRESS"
echo "Project: $PROJECT_DIR"
echo "========================================="

cd "$PROJECT_DIR"

# --- 1. Generate production .env from template ---
echo ""
echo "[1/5] Generating production .env file..."

if [ -f .env.production ]; then
    echo "Using existing .env.production"
elif [ -f .env.production.example ]; then
    echo "Creating .env.production from .env.production.example..."
    echo "IMPORTANT: Edit .env.production and fill in your real API keys before continuing."
    cp .env.production.example .env.production
else
    echo "Error: Neither .env.production nor .env.production.example found in $PROJECT_DIR"
    echo "Copy .env.production.example to .env.production and fill in your API keys."
    exit 1
fi

# Replace placeholder with actual server address
sed "s/<YOUR_SERVER_IP>/${SERVER_ADDRESS}/g" .env.production > .env

# Auto-generate JWT secrets if they still have default placeholder values
if grep -q "CHANGE_ME" .env; then
    echo "Generating secure JWT secrets..."
    JWT_ADMIN=$(openssl rand -hex 32)
    JWT_OFFICIAL=$(openssl rand -hex 32)
    JWT_CITIZEN=$(openssl rand -hex 32)
    JWT_REFRESH=$(openssl rand -hex 32)
    sed -i "s/CHANGE_ME_admin_secret_replace_with_random_string/${JWT_ADMIN}/" .env
    sed -i "s/CHANGE_ME_official_secret_replace_with_random_string/${JWT_OFFICIAL}/" .env
    sed -i "s/CHANGE_ME_citizen_secret_replace_with_random_string/${JWT_CITIZEN}/" .env
    sed -i "s/CHANGE_ME_refresh_secret_replace_with_random_string/${JWT_REFRESH}/" .env
    echo "JWT secrets generated."
fi

echo "Generated .env with server address: $SERVER_ADDRESS"

# --- 2. Use production nginx config ---
echo ""
echo "[2/5] Setting up production Nginx config..."

if [ -f frontend/nginx.conf ]; then
    cp frontend/nginx.conf frontend/nginx.conf.dev.bak
fi
cp frontend/nginx.prod.conf frontend/nginx.conf

echo "Production Nginx config applied."

# --- 3. Update docker-compose frontend to use prod Dockerfile ---
echo ""
echo "[3/5] Preparing Docker build..."

# Ensure we're using the prod compose file
echo "Using docker-compose.prod.yml"

# --- 4. Build and start services ---
echo ""
echo "[4/5] Building and starting services (this may take 5-10 minutes on first run)..."

docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
docker-compose -f docker-compose.prod.yml up -d --build

# --- 5. Verify ---
echo ""
echo "[5/5] Verifying deployment..."

echo "Waiting 15 seconds for services to start..."
sleep 15

echo ""
echo "Container status:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "========================================="
echo "  Deployment Complete!"
echo "========================================="
echo ""
echo "Your application is now running at:"
echo "  http://${SERVER_ADDRESS}"
echo ""
echo "Quick checks:"
echo "  Frontend: curl -I http://${SERVER_ADDRESS}"
echo "  API:      curl http://${SERVER_ADDRESS}/api/health"
echo "  Logs:     docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "To set up daily MongoDB backups, run:"
echo "  bash scripts/setup-backups.sh"
echo "========================================="
