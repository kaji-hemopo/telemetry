#!/bin/bash

# Saito's Airbnb Execution Dashboard Startup Script

echo "🏡 Starting Saito's Airbnb Execution Dashboard..."
echo "================================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 to run the dashboard."
    exit 1
fi

# Check if server.py exists
if [ ! -f "server.py" ]; then
    echo "❌ server.py not found. Please run this script from the dashboard directory."
    exit 1
fi

# Start the server
echo "✅ Starting dashboard server on port 8081..."
echo "🌐 Dashboard will be available at: http://localhost:8081"
echo "📝 Press Ctrl+C to stop the server"
echo "================================================"

python3 server.py