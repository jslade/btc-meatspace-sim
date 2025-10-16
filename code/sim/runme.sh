#!/bin/bash

# Bitcoin Blockchain Simulator - Deployment Script
# This script automates the deployment process

set -e

echo "========================================="
echo "BTC Blockchain Simulator - Deployment"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed${NC}"
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo -e "${GREEN}Docker installed successfully${NC}"
    echo -e "${YELLOW}Please log out and back in for group changes to take effect${NC}"
    exit 0
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed${NC}"
    echo "Installing Docker Compose..."
    sudo apt update
    sudo apt install -y docker-compose
    echo -e "${GREEN}Docker Compose installed successfully${NC}"
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Installing git..."
    sudo apt update
    sudo apt install -y git
fi

# Display system information
echo ""
echo "System Information:"
echo "==================="
echo "Hostname: $(hostname)"
echo "IP Address: $(hostname -I | awk '{print $1}')"
echo "Temperature: $(vcgencmd measure_temp 2>/dev/null || echo 'N/A')"
echo "Memory: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo ""

# Pull latest changes if in a git repository
if [ -d .git ]; then
    echo "Pulling latest changes..."
    git pull
fi

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Build and start services
echo ""
echo "Building and starting services..."
echo "This may take several minutes on Raspberry Pi..."
docker-compose up --build -d

# Wait for services to be ready
echo ""
echo "Waiting for services to start..."
sleep 10

# Check service status
echo ""
echo "Service Status:"
echo "==============="
docker-compose ps

# Test backend health
echo ""
echo "Testing backend health..."
if curl -f http://localhost:8000/health &> /dev/null; then
    echo -e "${GREEN}✓ Backend is healthy${NC}"
else
    echo -e "${RED}✗ Backend health check failed${NC}"
fi

# Test frontend
echo ""
echo "Testing frontend..."
if curl -f http://localhost/ &> /dev/null; then
    echo -e "${GREEN}✓ Frontend is accessible${NC}"
else
    echo -e "${RED}✗ Frontend is not accessible${NC}"
fi

# Display access information
IP_ADDR=$(hostname -I | awk '{print $1}')
echo ""
echo "====================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "====================================="
echo ""
echo "Access the application at:"
echo "  Local:    http://localhost"
echo "  Network:  http://${IP_ADDR}"
echo ""
echo "API available at:"
echo "  http://${IP_ADDR}:8000/api"
echo ""
echo "Useful commands:"
echo "  docker-compose logs -f       # View logs"
echo "  docker-compose restart       # Restart services"
echo "  docker-compose down          # Stop services"
echo "  docker-compose ps            # Service status"
echo ""

# Optional: Set up auto-start
read -p "Do you want to enable auto-start on boot? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Setting up systemd service..."
    
    SERVICE_FILE="/etc/systemd/system/btc-sim.service"
    CURRENT_DIR=$(pwd)
    
    sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Bitcoin Meatspace Simulator
Requires=docker.service
After=docker.service network.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$CURRENT_DIR
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
User=$USER

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable btc-sim.service
    echo -e "${GREEN}✓ Auto-start enabled${NC}"
    echo "Service will start automatically on boot"
fi

echo ""
echo "Deployment complete! 🎉"
