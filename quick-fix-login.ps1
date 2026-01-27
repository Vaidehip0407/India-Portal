Write-Host "Quick Login Fix Script" -ForegroundColor Cyan

# Wait for Docker Desktop to start
Write-Host "Waiting for Docker Desktop to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Try to check if docker is working
$dockerWorking = $false
for ($i = 1; $i -le 5; $i++) {
    try {
        $null = docker version 2>$null
        $dockerWorking = $true
        Write-Host "Docker is ready!" -ForegroundColor Green
        break
    } catch {
        Write-Host "Waiting for Docker... ($i/5)" -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    }
}

if (-not $dockerWorking) {
    Write-Host "Docker not ready. Please start Docker Desktop manually." -ForegroundColor Red
    exit 1
}

Write-Host "`nStep 1: Stopping all containers..." -ForegroundColor Yellow
docker-compose down

Write-Host "`nStep 2: Starting containers in order..." -ForegroundColor Yellow
docker-compose up -d backend
Start-Sleep -Seconds 10

docker-compose up -d frontend  
Start-Sleep -Seconds 5

docker-compose up -d nginx
Start-Sleep -Seconds 5

Write-Host "`nStep 3: Checking container status..." -ForegroundColor Yellow
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host "`nStep 4: Creating test user..." -ForegroundColor Yellow
python create-test-user.py

Write-Host "`nStep 5: Testing login..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    $body = @{
        username = "test@example.com"
        password = "test123"
    }
    
    $response = Invoke-RestMethod -Uri "http://localhost/api/auth/login" -Method Post -Body $body -ContentType "application/x-www-form-urlencoded"
    Write-Host "Login test: SUCCESS!" -ForegroundColor Green
    Write-Host "You can now login with: test@example.com / test123" -ForegroundColor Cyan
} catch {
    Write-Host "Login test: FAILED - $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Check browser console for detailed errors" -ForegroundColor Yellow
}

Write-Host "`nDone! Try logging in now." -ForegroundColor Green