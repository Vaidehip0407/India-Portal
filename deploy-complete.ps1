# Unified Portal - Complete AWS EC2 Deployment Script (PowerShell)
# Installs Docker, Docker Compose, Git, and deploys the application

param(
    [Parameter(Mandatory=$true)]
    [string]$KeyPath,
    
    [Parameter(Mandatory=$true)]
    [string]$InstanceIP
)

# Color functions
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Info { Write-Host $args -ForegroundColor Cyan }

Write-Info "=========================================="
Write-Info "Unified Portal - Complete Deployment"
Write-Info "=========================================="

# Validate inputs
if (-not (Test-Path $KeyPath)) {
    Write-Error "ERROR: Key file not found at: $KeyPath"
    exit 1
}

Write-Warning "Target Instance: $InstanceIP"
Write-Warning "Key File: $KeyPath"
Write-Warning "Repository: https://github.com/Vaidehip0407/unified-portal.git"
Write-Host ""

# Create deployment script
$deploymentScript = @'
#!/bin/bash
set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "\n${BLUE}[1/7] Updating system packages...${NC}"
sudo apt-get update
sudo apt-get upgrade -y

echo -e "\n${BLUE}[2/7] Installing Git...${NC}"
sudo apt-get install -y git

echo -e "\n${BLUE}[3/7] Installing Docker...${NC}"
if ! command -v docker &> /dev/null; then
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker ubuntu
    echo -e "${GREEN}Docker installed successfully${NC}"
else
    echo -e "${GREEN}Docker already installed${NC}"
fi

echo -e "\n${BLUE}[4/7] Installing Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}Docker Compose installed successfully${NC}"
else
    echo -e "${GREEN}Docker Compose already installed${NC}"
fi

echo -e "\n${BLUE}[5/7] Cloning/Updating repository...${NC}"
if [ ! -d "unified-portal" ]; then
    git clone https://github.com/Vaidehip0407/unified-portal.git
    cd unified-portal
else
    cd unified-portal
    git fetch origin
    git reset --hard origin/main
fi

echo -e "\n${BLUE}[6/7] Stopping existing containers...${NC}"
docker-compose down 2>/dev/null || true

echo -e "\n${BLUE}[7/7] Starting application with Docker Compose...${NC}"
docker-compose up -d

sleep 5

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}Application Status:${NC}"
docker-compose ps
echo -e "\n${YELLOW}Access Points:${NC}"
echo -e "  Frontend: http://$(hostname -I | awk '{print $1}')"
echo -e "  API Docs: http://$(hostname -I | awk '{print $1}')/docs"
echo -e "  Health Check: http://$(hostname -I | awk '{print $1}')/health"
'@

# Execute SSH command
Write-Info "Connecting to EC2 instance and deploying..."
Write-Info ""

$sshCommand = "ssh -i `"$KeyPath`" ubuntu@$InstanceIP `"$deploymentScript`""
Invoke-Expression $sshCommand

Write-Success ""
Write-Success "=========================================="
Write-Success "✓ Remote Deployment Successful!"
Write-Success "=========================================="
Write-Warning "Your application is now live at:"
Write-Info "  http://$InstanceIP"
Write-Host ""
Write-Warning "Next Steps:"
Write-Host "  1. Open http://$InstanceIP in your browser"
Write-Host "  2. Register a new account"
Write-Host "  3. Start using the portal"
Write-Host ""
Write-Warning "To view logs:"
Write-Host "  ssh -i $KeyPath ubuntu@$InstanceIP"
Write-Host "  cd unified-portal; docker-compose logs -f"
