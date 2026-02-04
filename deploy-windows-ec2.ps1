# Windows EC2 Deployment Script for RPA Government Portal
# Server: 34.228.199.241

Write-Host "🚀 DEPLOYING RPA GOVERNMENT PORTAL TO WINDOWS EC2" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "❌ Please run this script as Administrator" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Checking Prerequisites..." -ForegroundColor Yellow

# Check Git
try {
    $gitVersion = git --version
    Write-Host "✅ Git: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git not found. Installing..." -ForegroundColor Red
    # Install Git via Chocolatey
    if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
        Write-Host "Installing Chocolatey..." -ForegroundColor Yellow
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    }
    choco install git -y
    refreshenv
}

# Check Python
try {
    $pythonVersion = python --version
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Installing..." -ForegroundColor Red
    choco install nodejs -y
    refreshenv
}

# Check Chrome
$chromePaths = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)

$chromeFound = $false
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        Write-Host "✅ Chrome found at: $path" -ForegroundColor Green
        $chromeFound = $true
        break
    }
}

if (-not $chromeFound) {
    Write-Host "❌ Chrome not found. Installing..." -ForegroundColor Red
    choco install googlechrome -y --ignore-checksums
}

Write-Host ""
Write-Host "📥 Cloning Repository..." -ForegroundColor Yellow

# Clone repository
if (Test-Path "C:\rpa-gov-portal") {
    Write-Host "Repository already exists. Updating..." -ForegroundColor Yellow
    Set-Location "C:\rpa-gov-portal"
    git pull origin main
} else {
    Set-Location "C:\"
    git clone https://github.com/Vaidehip0407/rpa-gov-portal.git
    Set-Location "C:\rpa-gov-portal"
}

Write-Host ""
Write-Host "🐍 Setting up Backend..." -ForegroundColor Yellow

# Setup backend
Set-Location "C:\rpa-gov-portal\backend"

# Install Python dependencies
Write-Host "Installing Python packages..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env file
$envContent = @"
DATABASE_URL=sqlite:///./unified_portal.db
SECRET_KEY=windows-ec2-rpa-portal-secret-key-2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=RPA Government Portal
ENVIRONMENT=production
DEBUG=false

# CORS for Windows EC2
FRONTEND_URL=http://34.228.199.241
BACKEND_CORS_ORIGINS=["http://34.228.199.241", "http://34.228.199.241:80", "http://localhost:3000"]

# OpenAI API Key (replace with actual key)
OPENAI_API_KEY=your-openai-api-key-here
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "✅ Backend environment configured" -ForegroundColor Green

Write-Host ""
Write-Host "🎨 Setting up Frontend..." -ForegroundColor Yellow

# Setup frontend
Set-Location "C:\rpa-gov-portal\frontend"

# Install Node dependencies
Write-Host "Installing Node packages..." -ForegroundColor Yellow
npm install

# Build frontend
Write-Host "Building frontend..." -ForegroundColor Yellow
npm run build

Write-Host "✅ Frontend build complete" -ForegroundColor Green

Write-Host ""
Write-Host "🔥 Configuring Windows Firewall..." -ForegroundColor Yellow

# Configure firewall
netsh advfirewall firewall add rule name="RPA Portal Frontend" dir=in action=allow protocol=TCP localport=80
netsh advfirewall firewall add rule name="RPA Portal Backend" dir=in action=allow protocol=TCP localport=8000

Write-Host "✅ Firewall configured" -ForegroundColor Green

Write-Host ""
Write-Host "📝 Creating startup scripts..." -ForegroundColor Yellow

# Backend startup script
$backendScript = @"
@echo off
cd /d C:\rpa-gov-portal\backend
echo 🚀 Starting RPA Government Portal Backend...
echo Backend will be available at: http://34.228.199.241:8000
echo API Documentation: http://34.228.199.241:8000/docs
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
"@

$backendScript | Out-File -FilePath "C:\rpa-gov-portal\start-backend.bat" -Encoding UTF8

# Frontend startup script
$frontendScript = @"
@echo off
cd /d C:\rpa-gov-portal\frontend
echo 🎨 Starting RPA Government Portal Frontend...
echo Frontend will be available at: http://34.228.199.241
npx serve dist -l 80
pause
"@

$frontendScript | Out-File -FilePath "C:\rpa-gov-portal\start-frontend.bat" -Encoding UTF8

# Combined startup script
$combinedScript = @"
@echo off
echo 🚀 Starting RPA Government Portal - Windows EC2
echo ===============================================
echo.
echo 🌐 URLs:
echo Frontend: http://34.228.199.241
echo Backend:  http://34.228.199.241:8000
echo API Docs: http://34.228.199.241:8000/docs
echo.
echo 🤖 RPA Features:
echo ✅ Visible Chrome browser automation
echo ✅ Torrent Power form auto-fill  
echo ✅ Real-time visual feedback
echo.

start "Backend" cmd /k "C:\rpa-gov-portal\start-backend.bat"
timeout /t 5 /nobreak
start "Frontend" cmd /k "C:\rpa-gov-portal\start-frontend.bat"

echo ✅ Both services starting...
echo Check the opened windows for status
pause
"@

$combinedScript | Out-File -FilePath "C:\rpa-gov-portal\start-portal.bat" -Encoding UTF8

Write-Host "✅ Startup scripts created" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 To start the portal:" -ForegroundColor Yellow
Write-Host "   Double-click: C:\rpa-gov-portal\start-portal.bat" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Access URLs:" -ForegroundColor Yellow
Write-Host "   Frontend: http://34.228.199.241" -ForegroundColor White
Write-Host "   Backend:  http://34.228.199.241:8000" -ForegroundColor White
Write-Host "   API Docs: http://34.228.199.241:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "🤖 RPA Features:" -ForegroundColor Yellow
Write-Host "   ✅ Visible Chrome browser automation" -ForegroundColor Green
Write-Host "   ✅ Torrent Power form auto-fill" -ForegroundColor Green
Write-Host "   ✅ Real-time visual feedback" -ForegroundColor Green
Write-Host "   ✅ Success messages after submission" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Update OPENAI_API_KEY in backend\.env" -ForegroundColor White
Write-Host "   2. Run: C:\rpa-gov-portal\start-portal.bat" -ForegroundColor White
Write-Host "   3. Test RPA automation" -ForegroundColor White
Write-Host "   4. Enjoy visible browser automation!" -ForegroundColor White
Write-Host ""

# Ask if user wants to start now
$startNow = Read-Host "Start the portal now? (y/n)"
if ($startNow -eq "y" -or $startNow -eq "Y") {
    Write-Host "🚀 Starting portal..." -ForegroundColor Green
    Start-Process "C:\rpa-gov-portal\start-portal.bat"
}

Write-Host "✅ Deployment script completed!" -ForegroundColor Green