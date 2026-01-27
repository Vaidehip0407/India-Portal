#!/bin/bash

echo "🔧 Fixing Nginx 502 Error on EC2..."

echo "Step 1: Check nginx logs"
docker logs unified-portal-nginx --tail 20

echo -e "\nStep 2: Test backend connectivity from nginx container"
docker exec unified-portal-nginx nslookup backend
docker exec unified-portal-nginx wget -q --spider http://backend:8000/health && echo "✅ Backend reachable" || echo "❌ Backend unreachable"

echo -e "\nStep 3: Test frontend connectivity from nginx container"
docker exec unified-portal-nginx nslookup frontend
docker exec unified-portal-nginx wget -q --spider http://frontend:80 && echo "✅ Frontend reachable" || echo "❌ Frontend unreachable"

echo -e "\nStep 4: Restart nginx container"
docker-compose restart nginx

echo -e "\nStep 5: Wait for nginx to be healthy"
sleep 10

echo -e "\nStep 6: Check container status"
docker ps

echo -e "\nStep 7: Test login API through nginx"
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123" \
  && echo -e "\n✅ Login API working!" || echo -e "\n❌ Login API failed"

echo -e "\nStep 8: Create test user if needed"
python3 create-test-user.py

echo -e "\n🎉 Fix complete! Try accessing: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"