#!/bin/bash
# Start LiteLLM Proxy in Docker for secure API key management
# Containers use dummy keys pointing to this proxy

set -e

echo "=========================================="
echo "LITELLM PROXY STARTUP (DOCKER)"
echo "Timestamp: $(date)"
echo "=========================================="

# Configuration
OPENCLAW_ROOT="/Users/jacksonhemopo/.openclaw"
CONFIG_FILE="$OPENCLAW_ROOT/workspace_ito/intel/Tier1_Scripts/litellm_config.yaml"
# Fallback if config isn't in ito
if [ ! -f "$CONFIG_FILE" ]; then
    CONFIG_FILE="$OPENCLAW_ROOT/workspace_saito/scripts/Tier1_Scripts/litellm_config.yaml"
fi
LOG_FILE="$OPENCLAW_ROOT/workspace_saito/scripts/Tier1_Scripts/litellm_proxy_docker.log"
PORT=4000
IMAGE="ghcr.io/berriai/litellm:main-latest"

# Check if already running
if /usr/local/bin/docker ps -f name=litellm-proxy --format '{{.Names}}' | grep -q 'litellm-proxy'; then
    echo "LiteLLM proxy container already running"
    exit 0
fi

# Remove existing container if it exists but is not running
if /usr/local/bin/docker ps -a -f name=litellm-proxy --format '{{.Names}}' | grep -q 'litellm-proxy'; then
    echo "Removing existing stopped litellm-proxy container..."
    /usr/local/bin/docker rm litellm-proxy
fi

# Load environment variables from OpenClaw config
if [ -f "/Users/jacksonhemopo/.openclaw/openclaw.json" ]; then
    echo "Loading API keys from OpenClaw configuration..."
    
    # Use jq if available for robust parsing
    if command -v jq > /dev/null 2>&1; then
        DEEPSEEK_KEY=$(jq -r '.models.providers["custom-api-deepseek-com"].apiKey // ""' /Users/jacksonhemopo/.openclaw/openclaw.json)
    else
        # Fallback to grep
        DEEPSEEK_KEY=$(grep -o '"custom-api-deepseek-com"[^}]*' /Users/jacksonhemopo/.openclaw/openclaw.json | grep -o '"apiKey":"[^"]*"' | cut -d'"' -f4 | head -1)
    fi
    
    # Use environment variables as fallback
    [ -z "$DEEPSEEK_KEY" ] && DEEPSEEK_KEY="$DEEPSEEK_API_KEY"
    
    echo "API keys loaded (masked for security)"
else
    echo "WARNING: OpenClaw configuration not found"
    exit 1
fi

# Start LiteLLM proxy in Docker
echo "Starting LiteLLM proxy in Docker on port $PORT..."

/usr/local/bin/docker run -d \
  --name litellm-proxy \
  -p $PORT:$PORT \
  -v "$CONFIG_FILE":/app/config.yaml \
  -e OPENAI_API_KEY="$OPENAI_KEY" \
  -e ANTHROPIC_API_KEY="$ANTHROPIC_KEY" \
  -e DEEPSEEK_API_KEY="$DEEPSEEK_KEY" \
  $IMAGE \
  --config /app/config.yaml --port $PORT > "$LOG_FILE" 2>&1

# Wait for proxy to start
echo "Waiting for proxy to start..."
sleep 10

if /usr/local/bin/docker ps -f name=litellm-proxy --format '{{.Names}}' | grep -q 'litellm-proxy'; then
    echo "✅ LiteLLM proxy started successfully in Docker"
    echo "Container: litellm-proxy"
    echo "Port: $PORT"
    echo ""
    echo "Test endpoint:"
    echo "  curl http://localhost:$PORT/health"
else
    echo "❌ Failed to start LiteLLM proxy in Docker"
    echo "Check docker logs: docker logs litellm-proxy"
    /usr/local/bin/docker logs litellm-proxy | tail -20
    exit 1
fi

exit 0