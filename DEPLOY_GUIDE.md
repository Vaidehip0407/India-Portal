# Unified Portal - Complete Deployment Guide

This guide provides step-by-step instructions to deploy the Unified Portal application to AWS EC2 with automatic installation of all dependencies.

## Prerequisites

- AWS EC2 instance running Ubuntu 20.04 or later
- SSH access to the instance (PEM key file)
- Git installed on your local machine
- Basic knowledge of terminal/command line

## Quick Start (Automated)

### Option 1: Linux/Mac (Bash)

```bash
# Make the script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh /path/to/your/key.pem your-instance-ip-or-dns
```

**Example:**
```bash
./deploy.sh ~/Downloads/gov-portal.pem 54.167.51.207
```

### Option 2: Windows (PowerShell)

```powershell
# Run the deployment script
.\deploy-complete.ps1 -KeyPath "C:\path\to\key.pem" -InstanceIP "54.167.51.207"
```

**Example:**
```powershell
.\deploy-complete.ps1 -KeyPath "C:\Users\YourName\Downloads\gov-portal.pem" -InstanceIP "54.167.51.207"
```

## What the Script Does

The deployment script automatically:

1. **Updates System Packages** - Ensures all system libraries are current
2. **Installs Git** - For repository management
3. **Installs Docker** - Container runtime
4. **Installs Docker Compose** - Multi-container orchestration
5. **Clones Repository** - Downloads the latest code from GitHub
6. **Stops Existing Containers** - Cleans up any previous deployments
7. **Starts Application** - Launches all services (backend, frontend, nginx)

## Access Your Application

After deployment completes, access your application at:

- **Frontend**: `http://your-instance-ip`
- **API Documentation**: `http://your-instance-ip/docs`
- **Health Check**: `http://your-instance-ip/health`

## Manual Deployment (If Script Fails)

If the automated script doesn't work, follow these manual steps:

### 1. SSH into your EC2 instance
```bash
ssh -i /path/to/key.pem ubuntu@your-instance-ip
```

### 2. Update system packages
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 3. Install Docker
```bash
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```

### 4. Install Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 5. Install Git
```bash
sudo apt-get install -y git
```

### 6. Clone the repository
```bash
cd /home/ubuntu
git clone https://github.com/Vaidehip0407/unified-portal.git
cd unified-portal
```

### 7. Start the application
```bash
docker-compose up -d
```

### 8. Verify deployment
```bash
docker-compose ps
```

## Common Commands

### View Application Logs
```bash
docker-compose logs -f
```

### View Specific Service Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
```

### Stop the Application
```bash
docker-compose down
```

### Restart the Application
```bash
docker-compose restart
```

### Update to Latest Code
```bash
git pull origin main
docker-compose down
docker-compose up -d
```

### Check Service Status
```bash
docker-compose ps
```

## Troubleshooting

### Port Already in Use
If port 80 is already in use:
```bash
sudo lsof -i :80
sudo kill -9 <PID>
```

### Docker Permission Denied
```bash
sudo usermod -aG docker ubuntu
# Log out and log back in
```

### Container Won't Start
```bash
# Check logs
docker-compose logs backend

# Rebuild containers
docker-compose down
docker-compose up -d --build
```

### Database Issues
```bash
# Reset database
rm backend/unified_portal.db
docker-compose restart backend
```

## Application Features

- **User Registration & Authentication** - Secure account creation and login
- **Service Management** - Electricity, Gas, Water, Property services
- **RPA Automation** - Automated form filling and submission
- **Document Upload** - OCR-based document processing
- **Application Tracking** - Monitor submitted applications

## Support

For issues or questions:
1. Check the logs: `docker-compose logs -f`
2. Review the README.md in the project root
3. Check GitHub issues: https://github.com/Vaidehip0407/unified-portal/issues

## Security Notes

- Change the SECRET_KEY in production
- Use HTTPS in production (configure SSL certificate)
- Keep Docker and system packages updated
- Use strong passwords for user accounts
- Regularly backup the database

## Next Steps

1. Access the application at `http://your-instance-ip`
2. Create a test account
3. Explore the features
4. Configure any additional settings as needed
