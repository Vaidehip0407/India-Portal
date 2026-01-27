#!/bin/bash

echo "=== Docker Container Status ==="
docker ps -a

echo -e "\n=== Backend Health Check ==="
docker exec unified-portal-backend curl -f http://localhost:8000/health || echo "Backend health check failed"

echo -e "\n=== Frontend Health Check ==="
docker exec unified-portal-frontend curl -f http://localhost:80 || echo "Frontend health check failed"

echo -e "\n=== Network Connectivity Test ==="
docker exec unified-portal-nginx nslookup backend || echo "Backend DNS resolution failed"
docker exec unified-portal-nginx nslookup frontend || echo "Frontend DNS resolution failed"

echo -e "\n=== Backend Connection Test from Nginx ==="
docker exec unified-portal-nginx wget -q --spider http://backend:8000/health && echo "✅ Backend reachable" || echo "❌ Backend unreachable"

echo -e "\n=== Frontend Connection Test from Nginx ==="
docker exec unified-portal-nginx wget -q --spider http://frontend:80 && echo "✅ Frontend reachable" || echo "❌ Frontend unreachable"

echo -e "\n=== Recent Backend Logs ==="
docker logs unified-portal-backend --tail 10

echo -e "\n=== Recent Nginx Logs ==="
docker logs unified-portal-nginx --tail 10

echo -e "\n=== Network Details ==="
docker network ls
docker network inspect unified-portal_unified-portal-network