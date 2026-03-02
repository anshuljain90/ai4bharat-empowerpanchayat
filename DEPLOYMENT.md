# eGramSabha — AWS Deployment Guide

Complete step-by-step guide to deploy eGramSabha on AWS using a single EC2 instance with Docker Compose.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Cost Breakdown](#2-cost-breakdown)
3. [Files Overview](#3-files-overview)
4. [Configuring Environment Variables](#4-configuring-environment-variables)
5. [Step 1 — AWS Account & CLI Setup](#step-1--aws-account--cli-setup)
6. [Step 2 — Create Key Pair](#step-2--create-key-pair)
7. [Step 3 — Create Security Group](#step-3--create-security-group)
8. [Step 4 — Launch EC2 Instance](#step-4--launch-ec2-instance)
9. [Step 5 — Allocate Elastic IP](#step-5--allocate-elastic-ip)
10. [Step 6 — SSH into the Server](#step-6--ssh-into-the-server)
11. [Step 7 — Setup the Server](#step-7--setup-the-server)
12. [Step 8 — Clone and Deploy](#step-8--clone-and-deploy)
13. [Step 9 — Verify Deployment](#step-9--verify-deployment)
14. [Step 10 — Setup HTTPS (Optional)](#step-10--setup-https-optional)
15. [Step 11 — Setup Backups & Monitoring](#step-11--setup-backups--monitoring)
16. [Updating the Application](#updating-the-application)
17. [Troubleshooting](#troubleshooting)
18. [Cost Saving Tips](#cost-saving-tips)
19. [Security Checklist](#security-checklist)

---

## 1. Architecture Overview

```
                    Internet
                       |
                       v
              +------------------+
              |   Elastic IP     |
              |   (Static IP)    |
              +--------+---------+
                       |
        +--------------v---------------------------------+
        |         EC2 Instance (t3.small)                |
        |         Amazon Linux 2023                      |
        |         2 vCPU / 2 GB RAM / 30 GB EBS          |
        |                                                |
        |   +----------------------------------------+   |
        |   |         Docker Compose                 |   |
        |   |                                        |   |
        |   |  +-------------+                       |   |
        |   |  |  Frontend   | <-- Nginx port 80     |   |
        |   |  |  (React)    |     serves static     |   |
        |   |  |             |     files + proxies   |   |
        |   |  |             |     /api to backend   |   |
        |   |  +------+------+                       |   |
        |   |         |                              |   |
        |   |         v                              |   |
        |   |  +-------------+   +----------------+  |   |
        |   |  |  Backend    |   | Video MOM      |  |   |
        |   |  |  (Node.js)  |-->| (FastAPI)      |  |   |
        |   |  |  :5000      |   | :8000          |  |   |
        |   |  +------+------+   +-------+--------+  |   |
        |   |         |                  |           |   |
        |   |         v                  v           |   |
        |   |  +------------------------------+      |   |
        |   |  |        MongoDB               |      |   |
        |   |  |        :27017 (internal)     |      |   |
        |   |  +------------------------------+      |   |
        |   +----------------------------------------+   |
        +------------------------------------------------+

External APIs: HuggingFace (Whisper STT + Cohere LLM), JioMeet
```

Only port **80** (and optionally 443) is exposed to the internet. All backend services communicate over Docker's internal network.

---

## 2. Cost Breakdown

### Recommended: t3.small (~$18-27/month — lasts 4-5 months on $100)

| Resource           | Spec                   | Monthly Cost |
|--------------------|------------------------|--------------|
| EC2 Instance       | t3.small (2 vCPU, 2GB) | ~$15.18      |
| EBS Storage        | 30 GB gp3              | ~$2.40       |
| Elastic IP         | Free while attached    | $0.00        |
| Data Transfer      | First 100 GB           | ~$0-9.00     |
| **Total**          |                        | **~$18-27**  |

### If you need more RAM: t3.medium (~$33-42/month — lasts 2.5-3 months)

| Resource           | Spec                    | Monthly Cost |
|--------------------|-------------------------|--------------|
| EC2 Instance       | t3.medium (2 vCPU, 4GB) | ~$30.37      |
| EBS + Transfer     | Same as above           | ~$2-12       |
| **Total**          |                         | **~$33-42**  |

### Services to AVOID (cost traps)

| Service     | Cost       | Why avoid                        |
|-------------|------------|----------------------------------|
| DocumentDB  | ~$200+/mo  | Managed MongoDB, way overkill    |
| ECS Fargate | ~$50-100/mo| Per-container pricing adds up    |
| ALB         | ~$16+/mo   | Unnecessary for single server    |
| NAT Gateway | ~$32+/mo   | Use public subnet instead        |

---

## 3. Files Overview

All production files are already created in this repository:

| File | Purpose |
|------|---------|
| `.env.production.example` | Production environment template (copy to `.env.production` and fill in API keys) |
| `docker-compose.prod.yml` | Production Docker Compose (internal networking, no exposed ports for backend) |
| `frontend/Dockerfile.prod` | Production frontend Dockerfile (uses nginx.prod.conf) |
| `frontend/nginx.prod.conf` | Production Nginx config (gzip, security headers, rate limiting, reverse proxy) |
| `scripts/setup-server.sh` | One-time server setup (installs Docker, Compose, swap) |
| `scripts/deploy.sh` | Deployment script (generates .env, builds, starts all services) |
| `scripts/setup-backups.sh` | Sets up daily MongoDB backups with 7-day retention |
| `scripts/monitor.sh` | Health check script (containers, disk, memory, HTTP) |
| `scripts/update.sh` | Pull latest code and rebuild services |

---

## 4. Configuring Environment Variables

eGramSabha uses `.env.example` files as templates. **Never commit real secrets to git.** Copy each example, fill in your values, and the `.gitignore` will keep the real files out of version control.

### 4.1 Quick Setup (Local Development)

```bash
# From the project root:
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
cp video-mom-backend/.env.example video-mom-backend/.env

# Then edit each .env file and fill in your API keys
```

### 4.2 Quick Setup (Production on AWS)

```bash
# On the server, inside the cloned repo:
cp .env.production.example .env.production

# Edit and fill in your API keys:
nano .env.production

# Then run deploy — it generates .env from .env.production automatically
bash scripts/deploy.sh <YOUR_ELASTIC_IP>
```

### 4.3 Where to Get Each API Key

| Variable | Where to Get It |
|----------|----------------|
| `HF_TOKEN` | Sign up at [huggingface.co](https://huggingface.co), then go to **Settings > Access Tokens** and create a token with `read` scope. |
| `JIO_API_KEY` | Obtain from your Jio AI / Jio Translate platform account. Contact your Jio platform admin if you don't have access. |
| `JIOMEET_APP_ID` | Register at [jiomeetpro.jio.com](https://jiomeetpro.jio.com), create an app under **Platform API**, and copy the App ID. |

### 4.4 Generating the RSA Key Pair (for JioMeet)

The backend needs an RSA key pair to authenticate with JioMeet. Generate it on the server:

```bash
cd backend/keys/

# Generate private key
openssl genrsa -out RSA-PrivateKey.pem 2048

# Extract public key
openssl rsa -in RSA-PrivateKey.pem -pubout -out RSA-PublicKey.pub

# Set permissions
chmod 600 RSA-PrivateKey.pem
chmod 644 RSA-PublicKey.pub
```

> **Note**: Upload the public key (`RSA-PublicKey.pub`) to your JioMeet app configuration. The private key stays on the server only.

### 4.5 Generating JWT Secrets

The deploy script auto-generates JWT secrets if they still have `CHANGE_ME` placeholders. To generate them manually:

```bash
# Generate 4 random secrets
openssl rand -hex 32   # → use for JWT_ADMIN_SECRET
openssl rand -hex 32   # → use for JWT_OFFICIAL_SECRET
openssl rand -hex 32   # → use for JWT_CITIZEN_SECRET
openssl rand -hex 32   # → use for JWT_REFRESH_SECRET
```

Paste each into your `.env.production` file.

### 4.6 Updating Environment Variables After Deployment

If you need to change an API key or add a new variable after the app is already running:

```bash
cd ~/ai4bharat-empowerpanchayat

# 1. Edit the production template
nano .env.production

# 2. Regenerate .env with your server IP
sed "s/<YOUR_SERVER_IP>/$(curl -s https://checkip.amazonaws.com)/g" .env.production > .env

# 3. Restart affected services
docker-compose -f docker-compose.prod.yml up -d --build backend
docker-compose -f docker-compose.prod.yml up -d --build video-mom-backend
```

### 4.7 Environment Files Reference

| File | Purpose | Committed to Git? |
|------|---------|-------------------|
| `.env.example` | Root template (docker-compose) | Yes |
| `.env` | Root with real secrets | **No** |
| `.env.production.example` | Production template | Yes |
| `.env.production` | Production with real secrets | **No** |
| `backend/.env.example` | Backend template | Yes |
| `backend/.env` | Backend with real secrets | **No** |
| `frontend/.env.example` | Frontend template | Yes |
| `frontend/.env` | Frontend with real values | **No** |
| `video-mom-backend/.env.example` | Video-MOM template | Yes |
| `video-mom-backend/.env` | Video-MOM with real secrets | **No** |

---

## Step 1 — AWS Account & CLI Setup

### 1.1 Install AWS CLI

Download and install from: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

### 1.2 Configure AWS CLI

```bash
aws configure
```

Enter when prompted:
```
AWS Access Key ID: <your-access-key>
AWS Secret Access Key: <your-secret-key>
Default region name: ap-south-1
Default output format: json
```

> **Region**: Use `ap-south-1` (Mumbai) for India. Use `us-east-1` for cheapest global pricing.

### 1.3 Verify

```bash
aws sts get-caller-identity
```

---

## Step 2 — Create Key Pair

### Via Console (Easier)

1. **EC2 Dashboard** > **Key Pairs** > **Create Key Pair**
2. Name: `egramsabha-key`
3. Type: RSA, Format: `.pem`
4. Save the downloaded file to `~/.ssh/egramsabha-key.pem`

### Via CLI

```bash
aws ec2 create-key-pair \
  --key-name egramsabha-key \
  --query 'KeyMaterial' \
  --output text > egramsabha-key.pem
```

Set permissions:
```bash
# Mac/Linux
chmod 400 egramsabha-key.pem

# Windows PowerShell
icacls egramsabha-key.pem /inheritance:r /grant:r "$($env:USERNAME):(R)"
```

> **IMPORTANT**: Store this file safely. It is your only way to access the server.

---

## Step 3 — Create Security Group

### Via Console

1. **EC2 Dashboard** > **Security Groups** > **Create Security Group**
2. Name: `egramsabha-sg`
3. VPC: Default VPC
4. **Inbound Rules**:

| Type  | Port | Source       | Description     |
|-------|------|-------------|-----------------|
| SSH   | 22   | My IP       | SSH access      |
| HTTP  | 80   | 0.0.0.0/0  | Web traffic     |
| HTTPS | 443  | 0.0.0.0/0  | SSL traffic     |

5. Outbound: Leave default (allow all)

### Via CLI

```bash
# Create security group
SG_ID=$(aws ec2 create-security-group \
  --group-name egramsabha-sg \
  --description "eGramSabha application" \
  --query 'GroupId' --output text)

echo "Security Group: $SG_ID"

# Allow SSH from your current IP
MY_IP=$(curl -s https://checkip.amazonaws.com)
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr ${MY_IP}/32

# Allow HTTP and HTTPS from anywhere
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 443 --cidr 0.0.0.0/0
```

> **NEVER** open ports 5000, 8000, or 27017 to the public.

---

## Step 4 — Launch EC2 Instance

### Via Console (Recommended)

1. **EC2 Dashboard** > **Launch Instance**
2. Configure:

| Setting        | Value                                    |
|----------------|------------------------------------------|
| Name           | `eGramSabha-Server`                      |
| AMI            | Amazon Linux 2023                        |
| Instance type  | `t3.small` (or `t3.medium` for more RAM) |
| Key pair       | `egramsabha-key`                         |
| Security group | `egramsabha-sg`                          |
| Storage        | **30 GB gp3** (change from default 8GB)  |

3. Click **Launch Instance**

### Via CLI

```bash
# Find latest Amazon Linux 2023 AMI
AMI_ID=$(aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=al2023-ami-2023*-x86_64" "Name=state,Values=available" \
  --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' \
  --output text)

# Launch
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id $AMI_ID \
  --instance-type t3.small \
  --key-name egramsabha-key \
  --security-group-ids $SG_ID \
  --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":30,"VolumeType":"gp3","DeleteOnTermination":true}}]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=eGramSabha-Server}]' \
  --query 'Instances[0].InstanceId' --output text)

echo "Instance: $INSTANCE_ID"
```

Wait 1-2 minutes for the instance to start.

---

## Step 5 — Allocate Elastic IP

An Elastic IP gives your server a **static public IP** that survives restarts.

### Via Console

1. **EC2 Dashboard** > **Elastic IPs** > **Allocate**
2. Select the new IP > **Actions** > **Associate** > Select your instance

### Via CLI

```bash
ALLOC_ID=$(aws ec2 allocate-address --domain vpc --query 'AllocationId' --output text)
ELASTIC_IP=$(aws ec2 describe-addresses --allocation-ids $ALLOC_ID --query 'Addresses[0].PublicIp' --output text)

aws ec2 associate-address --instance-id $INSTANCE_ID --allocation-id $ALLOC_ID

echo "Your Elastic IP: $ELASTIC_IP"
```

**Write down your Elastic IP: `___.___.___.___`** — you will use this in the next steps.

> Free while attached to a running instance. Costs ~$3.65/month if unattached.

---

## Step 6 — SSH into the Server

```bash
# Mac/Linux/Git Bash
ssh -i ~/.ssh/egramsabha-key.pem ec2-user@<YOUR_ELASTIC_IP>

# Windows PowerShell
ssh -i C:\path\to\egramsabha-key.pem ec2-user@<YOUR_ELASTIC_IP>
```

You should see the Amazon Linux welcome message.

---

## Step 7 — Setup the Server

Run the included setup script. This installs Docker, Docker Compose, git, and sets up swap space.

```bash
# Still on the EC2 instance via SSH:
cd ~

# Install git first (not pre-installed on Amazon Linux 2023)
sudo yum install -y git

# Clone the repo
git clone https://github.com/anshuljain90/ai4bharat-empowerpanchayat.git
cd ai4bharat-empowerpanchayat

# Run server setup (installs Docker, Compose, swap, etc.)
bash scripts/setup-server.sh
```

**After the script completes, you MUST log out and log back in** for Docker group permissions:

```bash
exit
# SSH back in
ssh -i ~/.ssh/egramsabha-key.pem ec2-user@<YOUR_ELASTIC_IP>
```

Verify Docker works:
```bash
docker ps
# Should show empty table (no errors)
```

---

## Step 8 — Clone and Deploy

### 8.1 Configure Environment Variables

```bash
cd ~/ai4bharat-empowerpanchayat

# Create .env.production from the template
cp .env.production.example .env.production

# Edit and fill in your real API keys (HF_TOKEN, JIO_API_KEY, JIOMEET_APP_ID)
nano .env.production
```

> See [Section 4 — Configuring Environment Variables](#4-configuring-environment-variables) for details on where to get each API key and how to generate RSA keys.

### 8.2 Generate RSA Keys for JioMeet

```bash
cd ~/ai4bharat-empowerpanchayat/backend/keys/
openssl genrsa -out RSA-PrivateKey.pem 2048
openssl rsa -in RSA-PrivateKey.pem -pubout -out RSA-PublicKey.pub
chmod 600 RSA-PrivateKey.pem
cd ~/ai4bharat-empowerpanchayat
```

### 8.3 Deploy

```bash
bash scripts/deploy.sh <YOUR_ELASTIC_IP>
```

**What this does:**
1. Reads `.env.production`, replaces `<YOUR_SERVER_IP>` with your IP, generates `.env`
2. Auto-generates JWT secrets if they still have placeholder values
3. Copies the production Nginx config
4. Builds all Docker images (5-10 minutes on first run)
5. Starts all 4 containers

### 8.4 Watch the build (optional)

In another terminal:
```bash
ssh -i ~/.ssh/egramsabha-key.pem ec2-user@<YOUR_ELASTIC_IP>
cd ~/ai4bharat-empowerpanchayat
docker-compose -f docker-compose.prod.yml logs -f
```

---

## Step 9 — Verify Deployment

### From your local machine

```bash
# Frontend loads
curl -I http://<YOUR_ELASTIC_IP>
# Expected: HTTP/1.1 200 OK

# API responds
curl http://<YOUR_ELASTIC_IP>/api/health

# Health check
curl http://<YOUR_ELASTIC_IP>/health
# Expected: OK
```

### In browser

Open `http://<YOUR_ELASTIC_IP>` — you should see the eGramSabha application.

### On the server

```bash
# All containers running
docker-compose -f docker-compose.prod.yml ps

# Expected output:
# NAME                              STATUS
# egramsabha-frontend-1             Up
# egramsabha-backend-1              Up
# egramsabha-video-mom-backend-1    Up (healthy)
# egramsabha-mongodb-1              Up
```

---

## Step 10 — Setup HTTPS (Optional)

HTTPS is **required** for camera/microphone access (facial recognition, video features) in browsers.

### Option A: With a domain (Free SSL via Let's Encrypt)

**1. Point your domain to the Elastic IP:**

Add a DNS A record: `gramsabha.yourdomain.com` → `<YOUR_ELASTIC_IP>`

**2. Get SSL certificate:**

```bash
# Install certbot
sudo yum install -y certbot

# Stop frontend temporarily to free port 80
docker-compose -f docker-compose.prod.yml stop frontend

# Get certificate
sudo certbot certonly --standalone \
  -d gramsabha.yourdomain.com \
  --agree-tos \
  --email your-email@example.com \
  --non-interactive

# Restart frontend
docker-compose -f docker-compose.prod.yml start frontend
```

**3. Add SSL server block to `frontend/nginx.prod.conf`:**

Add this at the end of the file (before the closing `}`):

```nginx
server {
    listen 443 ssl;
    server_name gramsabha.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/gramsabha.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/gramsabha.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # Copy all location blocks from the port 80 server block here
}
```

**4. Mount certificates in `docker-compose.prod.yml`:**

Add under the frontend service:
```yaml
volumes:
  - /etc/letsencrypt:/etc/letsencrypt:ro
```

**5. Rebuild frontend:**
```bash
docker-compose -f docker-compose.prod.yml up -d --build frontend
```

**6. Auto-renew (cron):**
```bash
sudo crontab -e
# Add:
0 3 * * * certbot renew --pre-hook "cd /home/ec2-user/ai4bharat-empowerpanchayat && docker-compose -f docker-compose.prod.yml stop frontend" --post-hook "cd /home/ec2-user/ai4bharat-empowerpanchayat && docker-compose -f docker-compose.prod.yml start frontend"
```

### Option B: Without a domain (Self-signed — shows browser warning)

```bash
sudo mkdir -p /etc/ssl/egramsabha
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/egramsabha/privkey.pem \
  -out /etc/ssl/egramsabha/fullchain.pem \
  -subj "/CN=<YOUR_ELASTIC_IP>"
```

> After enabling HTTPS, update `.env.production` URLs from `http://` to `https://` and redeploy.

---

## Step 11 — Setup Backups & Monitoring

### MongoDB Backups

```bash
cd ~/ai4bharat-empowerpanchayat
bash scripts/setup-backups.sh
```

This sets up:
- Daily automated backups at 2 AM
- 7-day retention
- Compressed `.tar.gz` format
- Stored in `~/backups/`

### Monitoring

```bash
# Run health check manually
bash scripts/monitor.sh

# Add to cron for automatic monitoring every 5 minutes
crontab -e
# Add:
*/5 * * * * /home/ec2-user/ai4bharat-empowerpanchayat/scripts/monitor.sh >> ~/logs/monitor.log 2>&1
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs --tail=100 video-mom-backend

# Resource usage
docker stats
```

---

## Updating the Application

When you push new code:

```bash
cd ~/ai4bharat-empowerpanchayat

# Update everything
bash scripts/update.sh

# Or update only a specific service
bash scripts/update.sh backend
bash scripts/update.sh frontend
bash scripts/update.sh video-mom-backend
```

---

## Troubleshooting

### Container won't start

```bash
docker-compose -f docker-compose.prod.yml logs <service-name>
```

### Frontend shows blank page

```bash
# Check React build succeeded
docker-compose -f docker-compose.prod.yml logs frontend | grep -i error

# Check Nginx serves files
docker exec $(docker ps -qf "name=frontend") ls /usr/share/nginx/html/
```

### API returns 502 Bad Gateway

```bash
# Backend might still be starting
docker-compose -f docker-compose.prod.yml ps backend
docker-compose -f docker-compose.prod.yml logs --tail=50 backend
```

### MongoDB connection errors

```bash
docker-compose -f docker-compose.prod.yml ps mongodb
docker-compose -f docker-compose.prod.yml logs mongodb
```

### Out of memory

```bash
# Check memory
free -h
docker stats --no-stream

# If swap wasn't set up (setup-server.sh does this automatically):
sudo dd if=/dev/zero of=/swapfile bs=128M count=16
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
```

### Out of disk space

```bash
df -h
docker system df
docker system prune -f          # Clean unused containers/images
docker image prune -a -f        # Remove ALL unused images
```

### SSH connection timeout

- Check your IP hasn't changed (update Security Group SSH rule)
- Verify instance is running in AWS Console
- Try stop + start (not terminate)

---

## Cost Saving Tips

1. **Stop when not in use**: `aws ec2 stop-instances --instance-ids <ID>` (only pay ~$2.40/mo for EBS)
2. **Reserved Instance**: 1-year no-upfront t3.small = ~$8/month (47% savings)
3. **Set billing alerts**: AWS Console > Billing > Budgets > Create a $25/month budget
4. **Clean up Docker**: Weekly `docker system prune -f` (added in setup)
5. **When fully done**: Terminate instance + release Elastic IP + delete security group

---

## Security Checklist

- [ ] SSH access restricted to your IP only (not 0.0.0.0/0)
- [ ] MongoDB NOT exposed to internet (internal Docker only)
- [ ] Backend ports 5000/8000 NOT publicly accessible
- [ ] `.env` files in `.gitignore` (secrets not in git)
- [ ] CORS set to specific origin (not `*`)
- [ ] NODE_ENV set to `production`
- [ ] Nginx security headers enabled
- [ ] HTTPS enabled (for camera/mic access)
- [ ] MongoDB backups running daily
- [ ] System packages up to date (`sudo yum update -y`)

---

## Quick Reference

```bash
# SSH in
ssh -i ~/.ssh/egramsabha-key.pem ec2-user@<ELASTIC_IP>

# Start
cd ~/ai4bharat-empowerpanchayat && docker-compose -f docker-compose.prod.yml up -d

# Stop
docker-compose -f docker-compose.prod.yml down

# Restart a service
docker-compose -f docker-compose.prod.yml restart backend

# Logs
docker-compose -f docker-compose.prod.yml logs -f

# Status
docker-compose -f docker-compose.prod.yml ps

# Update
bash scripts/update.sh

# Backup
bash ~/backup-mongodb.sh

# Monitor
bash scripts/monitor.sh

# Resource usage
docker stats
```
