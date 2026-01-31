#!/bin/bash

# 🔒 Enhanced Self-Signed SSL Certificate Generator
# Creates a more browser-friendly self-signed certificate

echo "🔒 Creating enhanced self-signed SSL certificate..."

# Configuration
DOMAIN="50.19.189.29"
COUNTRY="IN"
STATE="Gujarat"
CITY="Ahmedabad"
ORG="India Portal"
OU="Government Services"

# Create SSL directory
sudo mkdir -p /etc/nginx/ssl

# Create certificate configuration
cat > /tmp/cert.conf <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
C=$COUNTRY
ST=$STATE
L=$CITY
O=$ORG
OU=$OU
CN=$DOMAIN

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = $DOMAIN
DNS.2 = localhost
DNS.3 = *.50.19.189.29
IP.1 = 50.19.189.29
IP.2 = 127.0.0.1
EOF

# Generate private key
echo "🔑 Generating private key..."
sudo openssl genrsa -out /etc/nginx/ssl/key.pem 2048

# Generate certificate
echo "📜 Generating certificate..."
sudo openssl req -new -x509 -key /etc/nginx/ssl/key.pem \
    -out /etc/nginx/ssl/cert.pem \
    -days 365 \
    -config /tmp/cert.conf \
    -extensions v3_req

# Set proper permissions
sudo chmod 600 /etc/nginx/ssl/key.pem
sudo chmod 644 /etc/nginx/ssl/cert.pem

# Clean up
rm /tmp/cert.conf

# Verify certificate
echo "🔍 Certificate details:"
sudo openssl x509 -in /etc/nginx/ssl/cert.pem -text -noout | grep -A 5 "Subject:"

echo ""
echo "✅ Enhanced SSL certificate created successfully!"
echo ""
echo "📋 Certificate details:"
echo "   Location: /etc/nginx/ssl/"
echo "   Valid for: 365 days"
echo "   Domains: $DOMAIN, localhost"
echo ""
echo "⚠️  Browser Warning:"
echo "   Browsers will show 'Not Secure' warning"
echo "   Click 'Advanced' → 'Proceed to $DOMAIN (unsafe)'"
echo ""
echo "🚀 Next steps:"
echo "   1. Restart nginx: docker compose -f docker-compose.prod.yml restart nginx"
echo "   2. Test HTTPS: https://$DOMAIN"