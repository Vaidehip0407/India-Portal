Write-Host "🔧 Fixing 502 Gateway Error..." -ForegroundColor Cyan

Write-Host "`n1. Stopping all containers..." -ForegroundColor Yellow
docker-compose down

Write-Host "`n2. Removing any orphaned containers..." -ForegroundColor Yellow
docker container prune -f

Write-Host "`n3. Removing unused networks..." -ForegroundColor Yellow
docker network prune -f

Write-Host "`n4. Starting services in correct order..." -ForegroundColor Yellow
Write-Host "   Starting backend first..."
docker-compose up -d backend

Write-Host "   Waiting for backend to be ready..."
Start-Sleep -Seconds 15

Write-Host "   Starting frontend..."
docker-compose up -d frontend

Write-Host "   Waiting for frontend to be ready..."
Start-Sleep -Seconds 10

Write-Host "   Starting nginx..."
docker-compose up -d nginx

Write-Host "`n5. Checking container status..." -ForegroundColor Yellow
docker ps

Write-Host "`n6. Testing backend health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 10
    Write-Host "✅ Backend is responding: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend not responding: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n7. Testing nginx proxy..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost/health" -TimeoutSec 10
    Write-Host "✅ Nginx proxy working: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Nginx proxy failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 Fix attempt complete! Check http://localhost" -ForegroundColor Green