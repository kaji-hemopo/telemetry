#!/bin/bash
# Zero-Compute System Maintenance Script
# Deletes old log files and telemetry data to prevent storage bloat
# Runs weekly on Sundays at midnight via cron

echo "=========================================="
echo "ZERO-COMPUTE SYSTEM MAINTENANCE"
echo "Date: $(date)"
echo "Purpose: Prune old logs and telemetry data"
echo "=========================================="

# Configuration
WORKSPACE="/Users/jacksonhemopo/.openclaw/workspace"
WORKSPACE="/Users/jacksonhemopo/.openclaw"
EMPIRE_DIR="$WORKSPACE/workspace_ito/intel/empire"
TELEMETRY_DIR="$WORKSPACE/workspace_ito/intel/Telemetry"
RETENTION_DAYS=7

echo "1. Deleting log files older than $RETENTION_DAYS days..."

# Delete OpenClaw log files
find "$WORKSPACE" -name "*.log" -type f -mtime +$RETENTION_DAYS -delete
LOGS_DELETED=$?

# Delete Empire swarm logs
find "$EMPIRE_DIR/logs" -name "*.log" -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null
EMPIRE_LOGS_DELETED=$?

echo "2. Deleting raw telemetry JSON older than $RETENTION_DAYS days..."

# Delete raw telemetry data (prevents storage bloat)
if [ -d "$TELEMETRY_DIR/raw" ]; then
    find "$TELEMETRY_DIR/raw" -name "*.json" -type f -mtime +$RETENTION_DAYS -delete
    TELEMETRY_DELETED=$?
else
    echo "   WARNING: Telemetry raw directory not found"
    TELEMETRY_DELETED=1
fi

echo "3. Cleaning up Docker sandbox temp directories..."

# Delete Docker sandbox temp directories older than 7 days
find /tmp -name .openclaw_kaji-sandbox-*" -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \; 2>/dev/null
DOCKER_CLEANED=$?

echo "4. Checking disk usage..."

# Report disk usage before/after (simplified)
DU_BEFORE=$(du -sh "$WORKSPACE" 2>/dev/null | cut -f1)

echo ""
echo "=========================================="
echo "MAINTENANCE COMPLETE"
echo "=========================================="
echo "Workspace size: $DU_BEFORE"
echo "Log cleanup: $(if [ $LOGS_DELETED -eq 0 ]; then echo "SUCCESS"; else echo "NO FILES"; fi)"
echo "Empire logs: $(if [ $EMPIRE_LOGS_DELETED -eq 0 ]; then echo "SUCCESS"; else echo "NO FILES"; fi)"
echo "Telemetry data: $(if [ $TELEMETRY_DELETED -eq 0 ]; then echo "SUCCESS"; else echo "NO FILES/ERROR"; fi)"
echo "Docker temp: $(if [ $DOCKER_CLEANED -eq 0 ]; then echo "SUCCESS"; else echo "NO DIRS"; fi)"
echo "Next maintenance: Next Sunday at midnight"
echo "=========================================="

exit 0