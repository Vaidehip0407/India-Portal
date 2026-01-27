Write-Host "Testing Login Issue..." -ForegroundColor Cyan

Write-Host "`nStep 1: Check containers" -ForegroundColor Yellow
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host "`nStep 2: Test backend directly" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "Backend health: OK ($($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "Backend health: FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nStep 3: Test login API directly" -ForegroundColor Yellow
try {
    $body = @{
        username = "test@example.com"
        password = "test123"
    }
    
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" -Method Post -Body $body -ContentType "application/x-www-form-urlencoded"
    Write-Host "Direct login: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "Direct login: FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nStep 4: Test through nginx proxy" -ForegroundColor Yellow
try {
    $body = @{
        username = "test@example.com"
        password = "test123"
    }
    
    $response = Invoke-RestMethod -Uri "http://localhost/api/auth/login" -Method Post -Body $body -ContentType "application/x-www-form-urlencoded"
    Write-Host "Nginx proxy login: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "Nginx proxy login: FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nStep 5: Check recent logs" -ForegroundColor Yellow
Write-Host "Backend logs:" -ForegroundColor Gray
docker logs unified-portal-backend --tail 3

Write-Host "`nNginx logs:" -ForegroundColor Gray
docker logs unified-portal-nginx --tail 3