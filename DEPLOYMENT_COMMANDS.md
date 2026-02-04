# Windows EC2 Deployment Commands - RPA Government Portal

## Server: 34.228.199.241

### 🚀 Quick Start (PowerShell - Recommended)
```powershell
# Run this on Windows EC2 as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Vaidehip0407/rpa-gov-portal/main/deploy-windows-ec2.ps1" -OutFile "deploy.ps1"
.\deploy.ps1
```

### 📋 Manual Installation Commands

#### 1. Install Prerequisites
```powershell
# Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install required software
choco install git -y
choco install nodejs -y
choco install googlechrome -y --ignore-checksums
choco install python -y

# Refresh environment
refreshenv
```

#### 2. Clone and Setup
```powershell
# Clone repository
cd C:\
git clone https://github.com/Vaidehip0407/rpa-gov-portal.git
cd rpa-gov-portal

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd ..\frontend
npm install
npm run build
```

#### 3. Configuration
```powershell
# Create backend .env file
cd C:\rpa-gov-portal\backend
@"
DATABASE_URL=sqlite:///./unified_portal.db
SECRET_KEY=windows-ec2-rpa-portal-secret-key-2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=RPA Government Portal
ENVIRONMENT=production
DEBUG=false
FRONTEND_URL=http://34.228.199.241
BACKEND_CORS_ORIGINS=["http://34.228.199.241", "http://34.228.199.241:80"]
OPENAI_API_KEY=your-openai-api-key-here
"@ | Out-File -FilePath ".env" -Encoding UTF8

# Configure Windows Firewall
netsh advfirewall firewall add rule name="RPA Portal Frontend" dir=in action=allow protocol=TCP localport=80
netsh advfirewall firewall add rule name="RPA Portal Backend" dir=in action=allow protocol=TCP localport=8000
```

#### 4. Start Services
```powershell
# Method 1: Use startup scripts (created by PowerShell script)
C:\rpa-gov-portal\start-portal.bat

# Method 2: Manual start
# Terminal 1 - Backend:
cd C:\rpa-gov-portal\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend:
cd C:\rpa-gov-portal\frontend
npx serve dist -l 80
```

### 🌐 Access URLs
- Frontend: http://34.228.199.241
- Backend: http://34.228.199.241:8000
- API Docs: http://34.228.199.241:8000/docs
- Health Check: http://34.228.199.241:8000/health

### 🐛 Troubleshooting Commands

#### Check Services
```powershell
# Check if ports are in use
netstat -ano | findstr :80
netstat -ano | findstr :8000

# Test backend health
Invoke-WebRequest -Uri "http://34.228.199.241:8000/health"

# Test Chrome installation
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --version
```

#### Kill Processes
```powershell
# Find and kill processes on specific ports
$port80 = netstat -ano | findstr :80 | ForEach-Object { ($_ -split '\s+')[4] }
$port8000 = netstat -ano | findstr :8000 | ForEach-Object { ($_ -split '\s+')[4] }

if ($port80) { taskkill /PID $port80 /F }
if ($port8000) { taskkill /PID $port8000 /F }
```

#### Restart Services
```powershell
# Kill existing processes and restart
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force
Get-Process | Where-Object {$_.ProcessName -eq "node"} | Stop-Process -Force

# Wait and restart
Start-Sleep -Seconds 3
Start-Process -FilePath "C:\rpa-gov-portal\start-portal.bat"
```

### 🤖 RPA Testing Commands

#### Test RPA Components
```powershell
# Test Python Selenium
python -c "from selenium import webdriver; print('✅ Selenium working')"

# Test webdriver-manager
python -c "from webdriver_manager.chrome import ChromeDriverManager; print('✅ WebDriver Manager working')"

# Test Chrome paths
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"
Test-Path "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
```

#### RPA Service Test
```powershell
# Test RPA service directly
cd C:\rpa-gov-portal\backend
python -c "
from app.services.simple_rpa_service import SimpleTorrentRPA
rpa = SimpleTorrentRPA()
result = rpa.setup_driver()
print(f'RPA Setup Result: {result}')
if rpa.driver:
    rpa.driver.quit()
"
```

### 📊 Monitoring Commands

#### System Resources
```powershell
# Check CPU and Memory usage
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10

# Check disk space
Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, @{Name="Size(GB)";Expression={[math]::Round($_.Size/1GB,2)}}, @{Name="FreeSpace(GB)";Expression={[math]::Round($_.FreeSpace/1GB,2)}}
```

#### Service Status
```powershell
# Check if services are running
$backendRunning = Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.CommandLine -like "*uvicorn*"}
$frontendRunning = Get-Process | Where-Object {$_.ProcessName -eq "node" -and $_.CommandLine -like "*serve*"}

Write-Host "Backend Running: $($backendRunning -ne $null)"
Write-Host "Frontend Running: $($frontendRunning -ne $null)"
```

### 🔧 Maintenance Commands

#### Update Repository
```powershell
cd C:\rpa-gov-portal
git pull origin main

# Rebuild frontend
cd frontend
npm run build

# Restart services
C:\rpa-gov-portal\start-portal.bat
```

#### Backup Database
```powershell
# Backup SQLite database
$backupPath = "C:\rpa-gov-portal\backups\$(Get-Date -Format 'yyyy-MM-dd-HH-mm-ss')"
New-Item -ItemType Directory -Path $backupPath -Force
Copy-Item "C:\rpa-gov-portal\backend\unified_portal.db" "$backupPath\unified_portal.db"
Write-Host "Database backed up to: $backupPath"
```

#### Clean Logs
```powershell
# Clean old log files (if any)
Get-ChildItem "C:\rpa-gov-portal" -Recurse -Name "*.log" | Remove-Item -Force
Write-Host "Log files cleaned"
```

### 🎯 Production Optimization

#### Performance Tuning
```powershell
# Set high performance power plan
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c

# Disable Windows Defender real-time protection (optional, for performance)
# Set-MpPreference -DisableRealtimeMonitoring $true
```

#### Auto-start Configuration
```powershell
# Create scheduled task to start portal on boot
$action = New-ScheduledTaskAction -Execute "C:\rpa-gov-portal\start-portal.bat"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "Administrator" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "RPA Government Portal" -Action $action -Trigger $trigger -Principal $principal
```

### 📞 Emergency Commands

#### Complete Reset
```powershell
# Stop all services
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force
Get-Process | Where-Object {$_.ProcessName -eq "node"} | Stop-Process -Force

# Remove and re-clone repository
Remove-Item "C:\rpa-gov-portal" -Recurse -Force
cd C:\
git clone https://github.com/Vaidehip0407/rpa-gov-portal.git

# Re-run deployment
cd C:\rpa-gov-portal
.\deploy-windows-ec2.ps1
```

#### Service Recovery
```powershell
# If services are stuck, force restart
Restart-Computer -Force
```

---

## 📝 Notes
- Always run PowerShell as Administrator
- Ensure AWS Security Group allows ports 80 and 8000
- Keep Chrome browser updated for RPA compatibility
- Monitor system resources during RPA operations
- Backup database regularly