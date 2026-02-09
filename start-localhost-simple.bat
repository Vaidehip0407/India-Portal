@echo off
echo 🚀 Starting Localhost Development - Simple Version
echo ================================================

echo 🐍 Starting Backend Server...
start "Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo ⏰ Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak

echo 🎨 Starting Frontend Server...
start "Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo ⏰ Waiting 5 seconds for frontend to start...
timeout /t 5 /nobreak

echo 🌐 Opening browser...
timeout /t 3 /nobreak
start http://localhost:3000

echo ✅ Both services should be starting...
echo 📋 Check the opened command windows for status
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs

pause