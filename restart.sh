#!/bin/bash
echo "🛑 Stopping existing Docker containers..."
docker compose down

echo "🔨 Building Docker images with no cache..."
docker compose build --no-cache

echo "🚀 Starting Docker containers in detached mode..."
docker compose up -d

echo ""
echo "✅ Deployment complete."