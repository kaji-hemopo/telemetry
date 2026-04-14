#!/bin/bash
# Docker Sandbox for OpenClaw Subagents
# Protects against prompt injection attacks by isolating agents in containers

set -e

# Configuration
AGENT_TYPE="$1"
TASK="$2"
OUTPUT_DIR="/tmp.openclaw_kaji-sandbox-$(date +%s)"
INPUT_FILE="/tmp/input-$(date +%s).json"

# Create output directory
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/input"
mkdir -p "$OUTPUT_DIR/output"

# Write task to input file
echo "$TASK" > "$OUTPUT_DIR/input/task.txt"

# Agent-specific configurations
case "$AGENT_TYPE" in
    "scout")
        NETWORK="bridge"
        MEMORY="1g"
        CPUS="2"
        IMAGE=.openclaw_kaji-scout-sandbox"
        ;;
    "quant")
        NETWORK="bridge"
        MEMORY="512m"
        CPUS="1"
        IMAGE=.openclaw_kaji-quant-sandbox"
        ;;
    "auditor")
        NETWORK="bridge"
        MEMORY="512m"
        CPUS="1"
        IMAGE=.openclaw_kaji-auditor-sandbox"
        ;;
    "spy")
        NETWORK="bridge"
        MEMORY="1g"
        CPUS="2"
        IMAGE=.openclaw_kaji-spy-sandbox"
        ;;
    "tactician")
        NETWORK="bridge"
        MEMORY="768m"
        CPUS="1"
        IMAGE=.openclaw_kaji-tactician-sandbox"
        ;;
    "macro_economist")
        NETWORK="bridge"
        MEMORY="1g"
        CPUS="2"
        IMAGE=.openclaw_kaji-macro-sandbox"
        ;;
    "technical_sniper")
        NETWORK="bridge"
        MEMORY="1g"
        CPUS="2"
        IMAGE=.openclaw_kaji-technical-sandbox"
        ;;
    *)
        echo "Unknown agent type: $AGENT_TYPE"
        exit 1
        ;;
esac

# Check if Docker image exists, build if not
if ! docker image inspect "$IMAGE" > /dev/null 2>&1; then
    echo "Building Docker image: $IMAGE"
    
    # Create minimal Dockerfile with Python
    cat > "$OUTPUT_DIR/Dockerfile" << EOF
FROM python:3.12-alpine

# Non-root user for security
RUN addgroup -g 1001 -S.openclaw_kaji && \
    adduser -S.openclaw_kaji -u 1001 -G.openclaw_kaji

# Create isolated workspace and directories as root
RUN mkdir -p /workspace /input /output && \
    chown -R.openclaw_kaji.openclaw_kaji /workspace /input /output

WORKDIR /workspace
USER.openclaw_kaji

# Install Python dependencies
COPY --chown.openclaw_kaji.openclaw_kaji requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent script
COPY --chown.openclaw_kaji.openclaw_kaji agent.py .

# Entrypoint
ENTRYPOINT ["python", "agent.py"]
EOF
    
    # Create requirements file
    cat > "$OUTPUT_DIR/requirements.txt" << EOF
requests>=2.31.0
EOF
    
    # Copy the Python agent script
    OPENCLAW_ROOT="/Users/jacksonhemopo/.openclaw"
    cp "$OPENCLAW_ROOT/workspace_ito/intel/empire/agent.py" "$OUTPUT_DIR/agent.py"
    
    # Build image
    docker build -t "$IMAGE" "$OUTPUT_DIR"
fi

# Run agent in Docker container with security constraints
echo "Running $AGENT_TYPE agent in Docker sandbox..."
/usr/local/bin/docker run \
    --rm \
    --memory="$MEMORY" \
    --cpus="$CPUS" \
    --network="$NETWORK" \
    --read-only \
    --tmpfs /tmp:rw,noexec,nosuid \
    -v "$OUTPUT_DIR/input:/input:ro" \
    -v "$OUTPUT_DIR/output:/output:rw" \
    -e "AGENT_TYPE=$AGENT_TYPE" \
    -e "OPENCLAW_SANDBOX=true" \
    -e "LLM_API_BASE=http://host.docker.internal:4000" \
    -e "LLM_API_KEY=sk-litellm-your-secret-key" \
    --add-host=host.docker.internal:host-gateway \
    --name .openclaw_kaji-$AGENT_TYPE-$(date +%s)" \
    "$IMAGE"

# Read and return result
if [ -f "$OUTPUT_DIR/output/result.json" ]; then
    cat "$OUTPUT_DIR/output/result.json"
else
    echo "{\"error\": \"No output generated\", \"agent\": \"$AGENT_TYPE\"}"
fi

# Cleanup (optional - keep for debugging)
# rm -rf "$OUTPUT_DIR"

echo "Sandbox execution complete for $AGENT_TYPE"