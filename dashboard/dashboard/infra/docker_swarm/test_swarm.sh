#!/bin/bash
# Test Swarm with proper Docker Compose networking

set -e

echo "=========================================="
echo "SWARM DOCKER COMPOSE TEST"
echo "Timestamp: $(date)"
echo "=========================================="

# Stop any existing litellm-proxy (we'll use the compose one)
echo "Stopping any existing litellm-proxy containers..."
docker stop litellm-proxy 2>/dev/null || true
docker rm litellm-proxy 2>/dev/null || true

# Start the LiteLLM proxy via docker-compose
echo "Starting LiteLLM proxy via docker-compose..."
cd "$(dirname "$0")"
docker-compose up -d litellm-proxy

# Wait for proxy to start
echo "Waiting for proxy to start..."
sleep 10

# Test proxy is working
echo "Testing proxy connectivity..."
curl -s http://localhost:4000/v1/models -H "Authorization: Bearer sk-litellm-your-secret-key" | grep -q "gpt-4o" && echo "✅ Proxy working with gpt-4o model" || echo "❌ Proxy not working"

# Test scout agent
echo ""
echo "Testing scout agent..."
echo "Generate a business idea for Japan market" > /tmp/swarm_test_task.txt

# Run scout via docker-compose (one-off)
docker-compose run --rm -v /tmp/swarm_test_task.txt:/input/task.txt scout 2>&1 | tail -20

# Cleanup
echo ""
echo "Cleaning up..."
docker-compose down

echo "=========================================="
echo "TEST COMPLETE"
echo "=========================================="