#!/bin/bash
# Force Frontend Update Script
# This will completely rebuild and restart the frontend container

echo "🚀 Force updating frontend container..."

# Stop frontend container
echo "⏹️ Stopping frontend container..."
docker-compose stop frontend

# Remove frontend container and image
echo "🗑️ Removing old frontend container and image..."
docker rm unified-portal-frontend 2>/dev/null || true
docker rmi unified-portal-frontend 2>/dev/null || true

# Clear Docker build cache for frontend
echo "🧹 Clearing Docker build cache..."
docker builder prune -f

# Rebuild frontend with no cache
echo "🔨 Rebuilding frontend (no cache)..."
docker-compose build frontend --no-cache

# Start frontend container
echo "▶️ Starting frontend container..."
docker-compose up -d frontend

# Wait for container to be ready
echo "⏳ Waiting for frontend to be ready..."
sleep 15

# Check container status
echo "📊 Checking container status..."
docker ps | grep frontend

# Test if frontend is responding
echo "🧪 Testing frontend response..."
curl -s http://localhost:3003 > /dev/null && echo "✅ Frontend is responding" || echo "❌ Frontend not responding"

# Check if test account text is removed
echo "🔍 Checking if test account text is removed..."
if curl -s http://localhost:3003 | grep -q "test@example.com"; then
    echo "❌ Test account text still present"
    echo "🔄 Try clearing browser cache and hard refresh (Ctrl+F5)"
else
    echo "✅ Test account text removed successfully!"
fi

echo "🎉 Frontend update completed!"
echo ""
echo "📋 Next steps:"
echo "1. Clear your browser cache"
echo "2. Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)"
echo "3. Or open in incognito/private mode"