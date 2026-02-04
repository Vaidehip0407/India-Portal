# Windows EC2 Deployment Guide - RPA Government Portal

## Server Details
- **IP Address**: 34.228.199.241
- **OS**: Windows Server 2019/2022
- **Access**: RDP (Remote Desktop Protocol)
- **Username**: Administrator

## 🚀 Quick Deployment

### Option 1: Automated PowerShell Script (Recommended)
1. Connect to Windows EC2 via RDP
2. Open PowerShell as Administrator
3. Run the deployment script:
```powershell
# Download and run deployment script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Vaidehip0407/rpa-gov-portal/main/deploy-windows-ec2.ps1" -OutFile "deploy.ps1"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deploy.ps1
```

### Option 2: Manual Deployment
Follow the steps below if automated script fails.

## 📋 Prerequisites

### 1. Install Required Software
```powershell
# Install Chocolatey (Package Manager)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Git
choco install git -y

# Install Node.js
choco install nodejs -y

# Install Chrome (for RPA automation)
choco install googlechrome -y --ignore-checksums

# Install Python (if not already installed)
choco install python -y
```

### 2. Verify Installations
```powershell
git --version
node --version
python --version
```

## 📥 Repository Setup

### 1. Clone Repository
```powershell
cd C:\
git clone https://github.com/Vaidehip0407/rpa-gov-portal.git
cd rpa-gov-portal
```

### 2. Backend Setup
```powershell
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup
```powershell
cd ..\frontend
npm install
npm run build
```

## ⚙️ Configuration

### 1. Backend Environment (.env)
Create `backend\.env` file:
```env
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
```

### 2. Windows Firewall Configuration
```powershell
# Allow frontend port (80)
netsh advfirewall firewall add rule name="RPA Portal Frontend" dir=in action=allow protocol=TCP localport=80

# Allow backend port (8000)
netsh advfirewall firewall add rule name="RPA Portal Backend" dir=in action=allow protocol=TCP localport=8000
```

## 🚀 Starting Services

### Method 1: Using Startup Scripts
```powershell
# Start both services
C:\rpa-gov-portal\start-portal.bat
```

### Method 2: Manual Start
```powershell
# Terminal 1: Start Backend
cd C:\rpa-gov-portal\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Frontend
cd C:\rpa-gov-portal\frontend
npx serve dist -l 80
```

## 🌐 Access URLs

- **Frontend**: http://34.228.199.241
- **Backend**: http://34.228.199.241:8000
- **API Documentation**: http://34.228.199.241:8000/docs
- **Health Check**: http://34.228.199.241:8000/health

## 🤖 RPA Features

### ✅ What Works on Windows EC2:
- **Visible Chrome Browser**: No headless restrictions
- **Torrent Power Automation**: Complete form auto-fill
- **Real-time Visual Feedback**: Green highlighting of filled fields
- **Success Messages**: Confirmation after form submission
- **Chrome Driver Management**: Automatic driver download and setup

### 🔧 RPA Configuration:
- Chrome browser opens visibly for automation
- Form fields are automatically filled with user data
- Visual feedback with green borders on filled fields
- Success message displayed after form submission
- Browser stays open for 5 minutes for user interaction

## 🐛 Troubleshooting

### Backend Not Starting
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID_NUMBER> /F

# Restart backend
cd C:\rpa-gov-portal\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend Not Accessible
```powershell
# Check if port 80 is in use
netstat -ano | findstr :80

# Install serve globally if needed
npm install -g serve

# Start frontend
cd C:\rpa-gov-portal\frontend
npx serve dist -l 80
```

### Chrome/RPA Issues
```powershell
# Check Chrome installation
dir "C:\Program Files\Google\Chrome\Application\chrome.exe"
dir "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# Reinstall Chrome if needed
choco install googlechrome -y --force --ignore-checksums
```

### API Connection Issues
1. Check backend is running: http://34.228.199.241:8000/health
2. Verify CORS settings in `backend/app/main.py`
3. Check Windows Firewall rules
4. Ensure AWS Security Group allows ports 80 and 8000

## 📝 Testing RPA Automation

1. Access frontend: http://34.228.199.241
2. Register/Login to the portal
3. Navigate: Services → Electricity → Name Change → Torrent Power
4. Click "Start AI Auto-fill in Website"
5. Watch Chrome browser open and auto-fill the form
6. Verify success message appears

## 🔐 Security Notes

- Change default SECRET_KEY in production
- Add your actual OpenAI API key
- Consider using HTTPS for production
- Restrict CORS origins for production use

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check Windows Event Logs for errors
4. Ensure AWS Security Group allows required ports