Write-Host "=== Docker Container Status ===" -ForegroundColor Yellow
docker ps -a

Write-Host "`n=== Backend Health Check ===" -ForegroundColor Yellow
try {
    docker exec unified-portal-backend curl -f http://localhost:8000/health
    Write-Host "✅ Backend health check passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend health check failed" -ForegroundColor Red
}

Write-Host "`n=== Frontend Health Check ===" -ForegroundColor Yellow
try {
    docker exec unified-portal-frontend curl -f http://localhost:80
    Write-Host "✅ Frontend health check passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend health check failed" -ForegroundColor Red
}

Write-Host "`n=== Network Connectivity Test ===" -ForegroundColor Yellow
Write-Host "Testing backend DNS resolution..."
docker exec unified-portal-nginx nslookup backend

Write-Host "Testing frontend DNS resolution..."
docker exec unified-portal-nginx nslookup frontend

Write-Host "`n=== Backend Connection Test from Nginx ===" -ForegroundColor Yellow
try {
    docker exec unified-portal-nginx wget -q --spider http://backend:8000/health
    Write-Host "✅ Backend reachable from nginx" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend unreachable from nginx" -ForegroundColor Red
}

Write-Host "`n=== Frontend Connection Test from Nginx ===" -ForegroundColor Yellow
try {
    docker exec unified-portal-nginx wget -q --spider http://frontend:80
    Write-Host "✅ Frontend reachable from nginx" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend unreachable from nginx" -ForegroundColor Red
}

Write-Host "`n=== Recent Backend Logs ===" -ForegroundColor Yellow
docker logs unified-portal-backend --tail 10

Write-Host "`n=== Recent Nginx Logs ===" -ForegroundColor Yellow
docker logs unified-portal-nginx --tail 10

Write-Host "`n=== Network Details ===" -ForegroundColor Yellow
docker network ls
docker network inspect unified-portal_unified-portal-network