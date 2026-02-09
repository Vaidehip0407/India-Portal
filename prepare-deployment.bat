@echo off
echo 🚀 PREPARING DEPLOYMENT FOR WINDOWS EC2: 52.91.52.123
echo =====================================================

echo 📦 Step 1: Creating deployment package...
if exist deployment-package rmdir /s /q deployment-package
mkdir deployment-package

echo 📁 Step 2: Copying backend files...
xcopy /E /I /Q backend deployment-package\backend
if not exist deployment-package\backend echo ❌ Backend copy failed & pause & exit

echo 📁 Step 3: Copying frontend files...
xcopy /E /I /Q frontend deployment-package\frontend
if not exist deployment-package\frontend echo ❌ Frontend copy failed & pause & exit

echo 📁 Step 4: Copying configuration files...
copy docker-compose.yml deployment-package\ >nul
copy nginx.conf deployment-package\ >nul
copy WINDOWS_EC2_DEPLOYMENT_NEW.md deployment-package\ >nul

echo 📝 Step 5: Creating Windows setup scripts...

echo @echo off > deployment-package\setup-backend.bat
echo echo 🐍 Setting up Backend... >> deployment-package\setup-backend.bat
echo cd backend >> deployment-package\setup-backend.bat
echo pip install -r requirements.txt >> deployment-package\setup-backend.bat
echo echo ✅ Backend setup complete! >> deployment-package\setup-backend.bat
echo pause >> deployment-package\setup-backend.bat

echo @echo off > deployment-package\setup-frontend.bat
echo echo 🎨 Setting up Frontend... >> deployment-package\setup-frontend.bat
echo cd frontend >> deployment-package\setup-frontend.bat
echo npm install >> deployment-package\setup-frontend.bat
echo npm run build >> deployment-package\setup-frontend.bat
echo echo ✅ Frontend setup complete! >> deployment-package\setup-frontend.bat
echo pause >> deployment-package\setup-frontend.bat

echo @echo off > deployment-package\start-backend.bat
echo cd /d %%~dp0backend >> deployment-package\start-backend.bat
echo echo 🚀 Starting Backend Server... >> deployment-package\start-backend.bat
echo echo Backend: http://52.91.52.123:8000 >> deployment-package\start-backend.bat
echo echo API Docs: http://52.91.52.123:8000/docs >> deployment-package\start-backend.bat
echo python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload >> deployment-package\start-backend.bat

echo @echo off > deployment-package\start-frontend.bat
echo cd /d %%~dp0frontend >> deployment-package\start-frontend.bat
echo echo 🎨 Starting Frontend Server... >> deployment-package\start-frontend.bat
echo echo Frontend: http://52.91.52.123 >> deployment-package\start-frontend.bat
echo npx serve dist -l 80 >> deployment-package\start-frontend.bat

echo @echo off > deployment-package\start-portal.bat
echo echo 🚀 Starting RPA Government Portal >> deployment-package\start-portal.bat
echo echo ================================= >> deployment-package\start-portal.bat
echo echo. >> deployment-package\start-portal.bat
echo echo 🌐 Access URLs: >> deployment-package\start-portal.bat
echo echo Frontend: http://52.91.52.123 >> deployment-package\start-portal.bat
echo echo Backend:  http://52.91.52.123:8000 >> deployment-package\start-portal.bat
echo echo API Docs: http://52.91.52.123:8000/docs >> deployment-package\start-portal.bat
echo echo. >> deployment-package\start-portal.bat
echo start "Backend" cmd /k "%%~dp0start-backend.bat" >> deployment-package\start-portal.bat
echo timeout /t 3 /nobreak >> deployment-package\start-portal.bat
echo start "Frontend" cmd /k "%%~dp0start-frontend.bat" >> deployment-package\start-portal.bat
echo echo ✅ Services starting... Check the opened windows >> deployment-package\start-portal.bat
echo pause >> deployment-package\start-portal.bat

echo 📝 Step 6: Creating environment file...
echo DATABASE_URL=sqlite:///./unified_portal.db > deployment-package\backend\.env
echo SECRET_KEY=windows-ec2-rpa-portal-secret-key-2026 >> deployment-package\backend\.env
echo ALGORITHM=HS256 >> deployment-package\backend\.env
echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> deployment-package\backend\.env
echo APP_NAME=RPA Government Portal >> deployment-package\backend\.env
echo ENVIRONMENT=production >> deployment-package\backend\.env
echo DEBUG=false >> deployment-package\backend\.env
echo FRONTEND_URL=http://52.91.52.123 >> deployment-package\backend\.env
echo BACKEND_CORS_ORIGINS=["http://52.91.52.123", "http://52.91.52.123:80", "http://localhost:3000"] >> deployment-package\backend\.env
echo OPENAI_API_KEY=your-openai-api-key-here >> deployment-package\backend\.env

echo 📦 Step 7: Creating deployment archive...
powershell -Command "Compress-Archive -Path 'deployment-package\*' -DestinationPath 'deployment-package.zip' -Force"

echo ✅ DEPLOYMENT PACKAGE READY!
echo ============================
echo.
echo 📦 Package: deployment-package.zip
echo 📁 Folder:  deployment-package\
echo.
echo 🚀 Next Steps:
echo 1. Copy deployment-package.zip to Windows EC2 (52.91.52.123)
echo 2. Extract the zip file on EC2
echo 3. Run setup-backend.bat (install Python dependencies)
echo 4. Run setup-frontend.bat (install Node dependencies)
echo 5. Run start-portal.bat (start both services)
echo.
echo 🌐 Access URLs after deployment:
echo Frontend: http://52.91.52.123
echo Backend:  http://52.91.52.123:8000
echo API Docs: http://52.91.52.123:8000/docs
echo.
echo 📋 Manual copy command (if needed):
echo scp -i your-key.pem deployment-package.zip Administrator@52.91.52.123:C:\
echo.

pause