#!/usr/bin/env bash
##
## deploy-frontend.sh
## Run this ONCE on your EC2 instance to install Nginx and serve the dashboard.
## After first run, every git push auto-deploys via your existing CD pipeline.
##

set -e

echo "── Step 1: Install Nginx ──────────────────────────────────"
sudo apt update -qq
sudo apt install -y nginx

echo "── Step 2: Create frontend directory ─────────────────────"
sudo mkdir -p /home/ubuntu/devops-project/frontend

echo "── Step 3: Copy index.html into place ────────────────────"
# Run from the root of your cloned repo:
sudo cp frontend/index.html /home/ubuntu/devops-project/frontend/index.html
sudo chown -R ubuntu:ubuntu /home/ubuntu/devops-project/frontend

echo "── Step 4: Install Nginx site config ─────────────────────"
sudo cp frontend/nginx.conf /etc/nginx/sites-available/devops
sudo ln -sf /etc/nginx/sites-available/devops /etc/nginx/sites-enabled/devops
sudo rm -f /etc/nginx/sites-enabled/default   # remove Nginx default placeholder

echo "── Step 5: Test and reload Nginx ─────────────────────────"
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx

echo ""
echo "✓ Done. Open http://$(curl -s ifconfig.me) in your browser."
echo "  FastAPI still runs on :8000 — Nginx proxies /students and /health through :80."
echo ""
echo "  Add port 80 to your EC2 security group if you haven't already."
echo "  (EC2 → Security Groups → Inbound Rules → Add Rule → HTTP → 0.0.0.0/0)"
