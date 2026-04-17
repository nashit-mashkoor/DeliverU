#!/bin/bash
echo "🛑 Stopping existing Docker containers..."
docker compose down

echo "🔨 Building Docker images with no cache..."
docker compose --profile infra --profile storage --profile app --profile worker --profile web build --no-cache

echo "🚀 Starting Docker containers in detached mode..."
docker compose --profile infra --profile storage --profile app --profile worker --profile web up -d

echo ""
echo "✅ Deployment complete."
