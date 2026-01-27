@echo off
echo Starting containers...

echo Stopping existing containers...
docker-compose down

echo Starting backend...
docker-compose up -d backend
timeout /t 10

echo Starting frontend...
docker-compose up -d frontend
timeout /t 5

echo Starting nginx...
docker-compose up -d nginx
timeout /t 5

echo Checking status...
docker ps

echo Creating test user...
python create-test-user.py

echo Done! Try logging in with: test@example.com / test123
pause