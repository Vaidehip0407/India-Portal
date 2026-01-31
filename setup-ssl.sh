#!/bin/bash

# 🔒 SSL Certificate Setup Script for India Portal
# This script sets up Let's Encrypt SSL certificates

echo "🔒 Setting up SSL certificates for India Portal..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DOMAIN=${1:-"your-domain.com"}
EMAIL=${2:-"admin@your-domain.com"}

echo -e "${YELLOW}📋 SSL Configuration:${NC}"
echo "   Domain: $DOMAIN"
echo "   Email: $EMAIL"
echo ""

# Check if domain is provided
if [ "$DOMAIN" = "your-domain.com" ]; then
    echo -e "${RED}❌ Please provide a domain name${NC}"
    echo "Usage: ./setup-ssl.sh your-domain.com admin@your-domain.com"
    echo ""
    echo -e "${YELLOW}🔧 Setting up self-signed certificate instead...${NC}"
    
    # Create self-signed certificate
    sudo mkdir -p /etc/nginx/ssl
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/key.pem \
        -out /etc/nginx/ssl/cert.pem \
        -subj "/C=IN/ST=Gujarat/L=Ahmedabad/O=IndiaPortal/CN=50.19.189.29"
    
    sudo chmod 600 /etc/nginx/ssl/key.pem
    sudo chmod 644 /etc/nginx/ssl/cert.pem
    
    echo -e "${GREEN}✅ Self-signed certificate created${NC}"
    echo -e "${YELLOW}⚠️  Browser will show 'Not Secure' warning${NC}"
    echo -e "${YELLOW}   Click 'Advanced' → 'Proceed to site' to accept${NC}"
    exit 0
fi

# Install Certbot
echo -e "${YELLOW}📦 Installing Certbot...${NC}"
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# Stop nginx temporarily
echo -e "${YELLOW}🛑 Stopping nginx temporarily...${NC}"
docker compose -f docker-compose.prod.yml stop nginx

# Create SSL directories
sudo mkdir -p /etc/letsencrypt
sudo mkdir -p /var/www/certbot

# Get SSL certificate
echo -e "${YELLOW}🔒 Obtaining SSL certificate from Let's Encrypt...${NC}"
sudo certbot certonly --standalone \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# Check if certificate was obtained
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo -e "${GREEN}✅ SSL certificate obtained successfully${NC}"
    
    # Copy certificates to nginx directory
    sudo mkdir -p /etc/nginx/ssl
    sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem /etc/nginx/ssl/cert.pem
    sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem /etc/nginx/ssl/key.pem
    
    # Set proper permissions
    sudo chmod 644 /etc/nginx/ssl/cert.pem
    sudo chmod 600 /etc/nginx/ssl/key.pem
    
    echo -e "${GREEN}✅ Certificates copied to nginx directory${NC}"
else
    echo -e "${RED}❌ Failed to obtain SSL certificate${NC}"
    echo -e "${YELLOW}🔧 Creating self-signed certificate as fallback...${NC}"
    
    sudo mkdir -p /etc/nginx/ssl
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/key.pem \
        -out /etc/nginx/ssl/cert.pem \
        -subj "/C=IN/ST=Gujarat/L=Ahmedabad/O=IndiaPortal/CN=$DOMAIN"
    
    sudo chmod 600 /etc/nginx/ssl/key.pem
    sudo chmod 644 /etc/nginx/ssl/cert.pem
fi

# Start nginx
echo -e "${YELLOW}🚀 Starting nginx with SSL...${NC}"
docker compose -f docker-compose.prod.yml up -d nginx

# Test SSL
echo -e "${YELLOW}🧪 Testing SSL configuration...${NC}"
sleep 10

if curl -k -s https://localhost/health > /dev/null; then
    echo -e "${GREEN}✅ HTTPS is working${NC}"
else
    echo -e "${RED}❌ HTTPS test failed${NC}"
fi

# Setup auto-renewal (only for Let's Encrypt)
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo -e "${YELLOW}⏰ Setting up auto-renewal...${NC}"
    
    # Create renewal script
    sudo tee /etc/cron.d/certbot-renew > /dev/null <<EOF
0 12 * * * root certbot renew --quiet --post-hook "docker compose -f /opt/india-portal/docker-compose.prod.yml restart nginx"
EOF
    
    echo -e "${GREEN}✅ Auto-renewal configured${NC}"
fi

echo ""
echo -e "${GREEN}🎉 SSL setup completed!${NC}"
echo ""
echo -e "${YELLOW}🌐 Access your portal:${NC}"
echo "   HTTPS: https://$DOMAIN"
echo "   HTTP:  http://$DOMAIN"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "   1. Update DNS to point $DOMAIN to 50.19.189.29"
echo "   2. Test HTTPS access"
echo "   3. Update frontend environment to use HTTPS"