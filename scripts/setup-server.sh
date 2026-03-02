#!/bin/bash
# =============================================================
# eGramSabha — EC2 Server Setup Script
# =============================================================
# Run this ONCE on a fresh Amazon Linux 2023 EC2 instance.
# Usage: bash setup-server.sh
# =============================================================

set -e

echo "========================================="
echo "  eGramSabha Server Setup"
echo "========================================="

# --- 1. System update ---
echo ""
echo "[1/6] Updating system packages..."
sudo yum update -y

# --- 2. Install Docker ---
echo ""
echo "[2/6] Installing Docker..."
sudo yum install -y docker git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# --- 3. Install Docker Compose ---
echo ""
echo "[3/6] Installing Docker Compose..."
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep '"tag_name"' | cut -d'"' -f4)
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# --- 4. Setup swap space (recommended for t3.small with 2GB RAM) ---
echo ""
echo "[4/6] Setting up 2GB swap space..."
if [ ! -f /swapfile ]; then
    sudo dd if=/dev/zero of=/swapfile bs=128M count=16
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
    echo "Swap configured: 2GB"
else
    echo "Swap already exists, skipping"
fi

# --- 5. Create directory structure ---
echo ""
echo "[5/6] Creating directory structure..."
mkdir -p ~/backups
mkdir -p ~/logs

# --- 6. Verify installations ---
echo ""
echo "[6/6] Verifying installations..."
echo ""
echo "Docker version:"
docker --version
echo ""
echo "Docker Compose version:"
docker-compose --version
echo ""
echo "Git version:"
git --version

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "IMPORTANT: You must log out and log back in"
echo "for Docker group permissions to take effect."
echo ""
echo "Next steps:"
echo "  1. exit"
echo "  2. SSH back in"
echo "  3. git clone your repo"
echo "  4. cd ai4bharat-empowerpanchayat"
echo "  5. bash scripts/deploy.sh <YOUR_SERVER_IP>"
echo "========================================="
