# 502 Error Diagnostic Script
# Ye script 502 error ke causes identify karega

Write-Host "=== NGINX 502 ERROR DIAGNOSTIC ===" -ForegroundColor Cyan

# 1. Docker containers ki status check karo
Write-Host "`n1. Checking Docker containers..." -ForegroundColor Yellow
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 2. Backend container logs check karo
Write-Host "`n2. Backend container logs (last 30 lines)..." -ForegroundColor Yellow
docker logs unified-portal-backend --tail 30

# 3. Nginx logs check karo
Write-Host "`n3. Nginx error logs..." -ForegroundColor Yellow
docker logs unified-portal-nginx --tail 30

# 4. Test if backend is responding
Write-Host "`n4. Testing backend health..." -ForegroundColor Yellow
try {
    $response = docker exec unified-portal-backend curl -f http://localhost:8000/health 2>&1
    Write-Host $response
} catch {
    Write-Host "Backend health check failed: $_" -ForegroundColor Red
}

# 5. Check Docker network
Write-Host "`n5. Checking Docker network..." -ForegroundColor Yellow
docker network inspect unified-portal-network 2>/dev/null | Select-String -Pattern "Name|Gateway|IPAddress" -A 2

# 6. Test DNS resolution inside nginx
Write-Host "`n6. Testing DNS resolution inside nginx container..." -ForegroundColor Yellow
docker exec unified-portal-nginx nslookup backend 2>&1 | tail -5

# 7. Test connectivity from nginx to backend
Write-Host "`n7. Testing connectivity from nginx to backend..." -ForegroundColor Yellow
docker exec unified-portal-nginx sh -c "curl -v http://backend:8000/health 2>&1 | head -20"

Write-Host "`n=== DIAGNOSTIC COMPLETE ===" -ForegroundColor Cyan
