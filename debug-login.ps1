Write-Host "🔍 Login Troubleshooting Script" -ForegroundColor Cyan

Write-Host "`n1. Checking Docker containers..." -ForegroundColor Yellow
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host "`n2. Testing backend health endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "✅ Backend health: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend health failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n3. Testing auth endpoints..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/auth/me" -TimeoutSec 5
    Write-Host "❌ Auth endpoint accessible without token (should be 401)" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "✅ Auth endpoint properly protected (401 Unauthorized)" -ForegroundColor Green
    } else {
        Write-Host "❌ Auth endpoint error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n4. Testing login endpoint with test credentials..." -ForegroundColor Yellow
try {
    $body = @{
        username = "test@example.com"
        password = "test123"
    }
    
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" -Method Post -Body $body -ContentType "application/x-www-form-urlencoded"
    Write-Host "✅ Login successful! Token received." -ForegroundColor Green
    Write-Host "   Token type: $($response.token_type)" -ForegroundColor Gray
    Write-Host "   Access token: $($response.access_token.Substring(0,20))..." -ForegroundColor Gray
} catch {
    Write-Host "❌ Login failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $errorResponse = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($errorResponse)
        $errorContent = $reader.ReadToEnd()
        Write-Host "   Error details: $errorContent" -ForegroundColor Red
    }
}

Write-Host "`n5. Testing nginx proxy to backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost/api/auth/me" -TimeoutSec 5
    Write-Host "❌ Nginx proxy accessible without token (should be 401)" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "✅ Nginx proxy working (401 Unauthorized)" -ForegroundColor Green
    } else {
        Write-Host "❌ Nginx proxy error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n6. Testing frontend accessibility..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3003" -TimeoutSec 5
    Write-Host "✅ Frontend accessible on port 3003: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend not accessible: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n7. Testing nginx frontend proxy..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost/" -TimeoutSec 5
    Write-Host "✅ Nginx frontend proxy working: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Nginx frontend proxy failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n8. Checking recent backend logs..." -ForegroundColor Yellow
docker logs unified-portal-backend --tail 5

Write-Host "`n9. Creating test user if needed..." -ForegroundColor Yellow
try {
    python create-test-user.py
} catch {
    Write-Host "❌ Failed to run test user script: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Try running: python create-test-user.py" -ForegroundColor Yellow
}

Write-Host "`n🎯 Summary:" -ForegroundColor Cyan
Write-Host "   - If backend health fails: Run docker-compose restart backend" -ForegroundColor Gray
Write-Host "   - If login fails: Check if test user exists in database" -ForegroundColor Gray
Write-Host "   - If nginx proxy fails: Run docker-compose restart nginx" -ForegroundColor Gray
Write-Host "   - Test credentials: test@example.com / test123" -ForegroundColor Gray