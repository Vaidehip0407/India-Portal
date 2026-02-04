# RPA Troubleshooting Guide - Windows EC2

## 🚨 Current Issue: "Simple RPA test failed"

Based on the screenshots, the RPA automation is failing. Here's how to fix it:

### 🔍 Diagnosis Steps

#### 1. Check Backend Connection
```powershell
# Test if backend is running
Invoke-WebRequest -Uri "http://34.228.199.241:8000/health"

# If this fails, backend is not running on port 8000
```

#### 2. Check Chrome Installation
```powershell
# Check Chrome paths
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"
Test-Path "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# Test Chrome version
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --version
```

#### 3. Test Python Selenium
```powershell
cd C:\rpa-gov-portal\backend
python -c "
try:
    from selenium import webdriver
    print('✅ Selenium imported successfully')
    
    from selenium.webdriver.chrome.options import Options
    print('✅ Chrome options imported')
    
    from webdriver_manager.chrome import ChromeDriverManager
    print('✅ WebDriver Manager imported')
    
except ImportError as e:
    print(f'❌ Import error: {e}')
"
```

### 🛠️ Fix Steps

#### Step 1: Ensure Backend is Running on Port 8000
```powershell
# Check what's running on port 8000
netstat -ano | findstr :8000

# If nothing, start backend
cd C:\rpa-gov-portal\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 2: Fix Chrome Driver Issues
```powershell
# Install/reinstall Chrome
choco install googlechrome -y --force --ignore-checksums

# Test Chrome driver setup
cd C:\rpa-gov-portal\backend
python -c "
from app.services.simple_rpa_service import SimpleTorrentRPA
rpa = SimpleTorrentRPA()
result = rpa.setup_driver()
print(f'Chrome Setup Result: {result}')
if rpa.driver:
    print('✅ Chrome driver working!')
    rpa.driver.quit()
else:
    print('❌ Chrome driver failed')
"
```

#### Step 3: Test RPA Service Directly
```powershell
cd C:\rpa-gov-portal\backend
python -c "
from app.services.simple_rpa_service import SimpleTorrentRPA

# Test data
test_data = {
    'city': 'Ahmedabad',
    'service_number': 'TP123456',
    't_number': 'T789',
    'mobile': '9632587410',
    'email': 'test@gmail.com'
}

# Run RPA test
rpa = SimpleTorrentRPA()
result = rpa.run_automation(test_data)
print(f'RPA Test Result: {result}')
"
```

### 🔧 Common Fixes

#### Fix 1: Port 8000 Already in Use
```powershell
# Find process using port 8000
$process = netstat -ano | findstr :8000 | ForEach-Object { ($_ -split '\s+')[4] }
if ($process) {
    Write-Host "Killing process on port 8000: $process"
    taskkill /PID $process /F
}

# Start backend
cd C:\rpa-gov-portal\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Fix 2: Chrome Driver Not Found
```powershell
# Reinstall webdriver-manager
cd C:\rpa-gov-portal\backend
pip uninstall webdriver-manager -y
pip install webdriver-manager==4.0.1

# Clear webdriver cache
Remove-Item "$env:USERPROFILE\.wdm" -Recurse -Force -ErrorAction SilentlyContinue
```

#### Fix 3: Python Path Issues
```powershell
# Add Python to PATH if needed
$pythonPath = (Get-Command python).Source
$pythonDir = Split-Path $pythonPath
$env:PATH += ";$pythonDir;$pythonDir\Scripts"

# Verify Python can find modules
cd C:\rpa-gov-portal\backend
python -c "import sys; print('\n'.join(sys.path))"
```

### 🚀 Complete RPA Reset

If all else fails, run this complete reset:

```powershell
# Stop all Python processes
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force

# Clear Chrome processes
Get-Process | Where-Object {$_.ProcessName -eq "chrome"} | Stop-Process -Force

# Reinstall Python packages
cd C:\rpa-gov-portal\backend
pip uninstall selenium webdriver-manager -y
pip install selenium==4.15.2 webdriver-manager==4.0.1 requests==2.31.0

# Reinstall Chrome
choco uninstall googlechrome -y
choco install googlechrome -y --ignore-checksums

# Test RPA setup
python -c "
print('🧪 Testing RPA Setup...')
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver_path = ChromeDriverManager().install()
    print(f'✅ ChromeDriver path: {driver_path}')
    
    from selenium.webdriver.chrome.service import Service
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get('data:text/html,<h1>RPA Test Success!</h1>')
    print('✅ Chrome browser opened successfully')
    
    driver.quit()
    print('✅ RPA setup complete!')
    
except Exception as e:
    print(f'❌ RPA setup failed: {e}')
"

# Restart backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 📊 Verification Steps

After fixing, verify everything works:

#### 1. Backend Health Check
```powershell
Invoke-WebRequest -Uri "http://34.228.199.241:8000/health"
# Should return: {"status":"healthy"}
```

#### 2. RPA Endpoint Test
```powershell
# Test RPA endpoint directly
$body = @{
    city = "Ahmedabad"
    service_number = "TP123456"
    t_number = "T789"
    mobile = "9632587410"
    email = "test@gmail.com"
    confirm_email = "test@gmail.com"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://34.228.199.241:8000/api/torrent-automation/start-automation" -Method POST -Body $body -ContentType "application/json"
```

#### 3. Frontend Connection Test
```powershell
# Test frontend can reach backend
Invoke-WebRequest -Uri "http://34.228.199.241"
# Should load the portal homepage
```

### 🎯 Expected Results

After successful fix:
1. ✅ Backend running on port 8000
2. ✅ Chrome browser opens visibly
3. ✅ Form fields get filled automatically
4. ✅ Green highlighting on filled fields
5. ✅ Success message after submission
6. ✅ No "Simple RPA test failed" errors

### 📞 Emergency Contact

If RPA still fails after all fixes:
1. Check Windows Event Logs for errors
2. Verify AWS Security Group allows ports 80 and 8000
3. Ensure Windows Firewall isn't blocking connections
4. Try restarting the Windows EC2 instance

### 🔍 Debug Logs

Enable detailed logging:
```powershell
cd C:\rpa-gov-portal\backend
$env:PYTHONPATH = "."
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)

from app.services.simple_rpa_service import SimpleTorrentRPA
rpa = SimpleTorrentRPA()
result = rpa.setup_driver()
print(f'Debug Result: {result}')
"
```

This should resolve the "Simple RPA test failed" error and get your automation working! 🚀