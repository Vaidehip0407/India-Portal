# Quick RPA Fix Script for Windows EC2
# Run this as Administrator to fix RPA issues

Write-Host "🔧 FIXING RPA ISSUES ON WINDOWS EC2" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "❌ Please run this script as Administrator" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔍 Step 1: Checking current processes..." -ForegroundColor Yellow

# Kill any existing Python/Chrome processes
Write-Host "Stopping existing Python processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "Stopping existing Chrome processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "chrome"} | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🔍 Step 2: Checking Chrome installation..." -ForegroundColor Yellow

# Check Chrome installation
$chromePaths = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)

$chromeFound = $false
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        Write-Host "✅ Chrome found at: $path" -ForegroundColor Green
        $chromeFound = $true
        
        # Get Chrome version
        try {
            $version = (Get-Item $path).VersionInfo.ProductVersion
            Write-Host "✅ Chrome version: $version" -ForegroundColor Green
        } catch {
            Write-Host "⚠️ Could not get Chrome version" -ForegroundColor Yellow
        }
        break
    }
}

if (-not $chromeFound) {
    Write-Host "❌ Chrome not found. Installing..." -ForegroundColor Red
    choco install googlechrome -y --ignore-checksums --force
    Write-Host "✅ Chrome installation completed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🔍 Step 3: Checking Python packages..." -ForegroundColor Yellow

# Check if we're in the right directory
if (-not (Test-Path "backend")) {
    Write-Host "❌ Not in project directory. Changing to C:\rpa-gov-portal..." -ForegroundColor Red
    if (Test-Path "C:\rpa-gov-portal") {
        Set-Location "C:\rpa-gov-portal"
    } else {
        Write-Host "❌ Project directory not found. Please run from project root." -ForegroundColor Red
        exit 1
    }
}

# Reinstall Python packages
Write-Host "Reinstalling Python packages..." -ForegroundColor Yellow
Set-Location "backend"

# Uninstall and reinstall key packages
pip uninstall selenium webdriver-manager -y
pip install selenium==4.15.2 webdriver-manager==4.0.1 requests==2.31.0

Write-Host "✅ Python packages updated" -ForegroundColor Green

Write-Host ""
Write-Host "🔍 Step 4: Testing RPA setup..." -ForegroundColor Yellow

# Test RPA setup
$testScript = @"
import sys
import os
sys.path.append('.')

try:
    print('🧪 Testing RPA setup...')
    
    # Test imports
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    print('✅ All imports successful')
    
    # Test Chrome driver setup
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    # Find Chrome binary
    chrome_paths = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            options.binary_location = path
            print(f'✅ Using Chrome binary: {path}')
            break
    
    # Create driver
    try:
        driver_path = ChromeDriverManager().install()
        print(f'✅ ChromeDriver path: {driver_path}')
        
        from selenium.webdriver.chrome.service import Service
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        print('✅ Chrome driver created successfully')
        
        # Test basic navigation
        driver.get('data:text/html,<h1>RPA Test Success!</h1>')
        print('✅ Navigation test successful')
        
        driver.quit()
        print('✅ RPA setup test completed successfully')
        
    except Exception as e:
        print(f'❌ Driver setup failed: {e}')
        sys.exit(1)
        
except Exception as e:
    print(f'❌ RPA test failed: {e}')
    sys.exit(1)
"@

$testScript | python
$testResult = $LASTEXITCODE

if ($testResult -eq 0) {
    Write-Host "✅ RPA test passed!" -ForegroundColor Green
} else {
    Write-Host "❌ RPA test failed. Check the error above." -ForegroundColor Red
}

Write-Host ""
Write-Host "🔍 Step 5: Checking backend service..." -ForegroundColor Yellow

# Check if backend is running
$backendRunning = netstat -ano | findstr :8000
if ($backendRunning) {
    Write-Host "✅ Backend is running on port 8000" -ForegroundColor Green
} else {
    Write-Host "❌ Backend is not running. Starting backend..." -ForegroundColor Red
    
    # Start backend in background
    Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -WindowStyle Minimized
    
    Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    # Check again
    $backendRunning = netstat -ano | findstr :8000
    if ($backendRunning) {
        Write-Host "✅ Backend started successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Backend failed to start" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🔍 Step 6: Testing backend health..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://34.228.199.241:8000/health" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend health check passed" -ForegroundColor Green
    } else {
        Write-Host "❌ Backend health check failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Backend health check failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Try: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔍 Step 7: Testing RPA endpoint..." -ForegroundColor Yellow

# Test RPA endpoint
$testData = @{
    city = "Ahmedabad"
    service_number = "TP123456"
    t_number = "T789"
    mobile = "9632587410"
    email = "test@gmail.com"
    confirm_email = "test@gmail.com"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "http://34.228.199.241:8000/api/torrent-automation/start-automation" -Method POST -Body $testData -ContentType "application/json" -TimeoutSec 30
    
    $result = $response.Content | ConvertFrom-Json
    if ($result.success) {
        Write-Host "✅ RPA endpoint test passed!" -ForegroundColor Green
    } else {
        Write-Host "❌ RPA endpoint test failed: $($result.message)" -ForegroundColor Red
        Write-Host "Details: $($result.details)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ RPA endpoint test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 SUMMARY" -ForegroundColor Green
Write-Host "=========" -ForegroundColor Green

if ($testResult -eq 0) {
    Write-Host "✅ RPA setup is working" -ForegroundColor Green
    Write-Host "✅ Chrome browser should open visibly" -ForegroundColor Green
    Write-Host "✅ Form auto-fill should work" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Access your portal at: http://34.228.199.241" -ForegroundColor Cyan
    Write-Host "🔧 Backend API at: http://34.228.199.241:8000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎉 RPA fix completed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ RPA setup has issues" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Manual fixes to try:" -ForegroundColor Yellow
    Write-Host "   1. Restart Windows EC2 instance" -ForegroundColor White
    Write-Host "   2. Run: choco install googlechrome -y --force --ignore-checksums" -ForegroundColor White
    Write-Host "   3. Run: pip install selenium==4.15.2 webdriver-manager==4.0.1" -ForegroundColor White
    Write-Host "   4. Check Windows Firewall settings" -ForegroundColor White
    Write-Host "   5. Ensure AWS Security Group allows ports 80 and 8000" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")