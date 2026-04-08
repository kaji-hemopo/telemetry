#!/usr/bin/env python3
"""
Saito's Airbnb Execution Dashboard Server
Simple HTTP server to serve the dashboard locally
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Configuration
PORT = 8081
DASHBOARD_DIR = Path(__file__).parent

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve dashboard files"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}")
    
    def do_GET(self):
        """Handle GET requests"""
        # Default to index.html if root path
        if self.path == '/':
            self.path = '/index.html'
        
        # Check if file exists
        file_path = DASHBOARD_DIR / self.path.lstrip('/')
        if not file_path.exists():
            self.send_error(404, f"File not found: {self.path}")
            return
        
        # Serve the file
        return super().do_GET()

def main():
    """Start the dashboard server"""
    os.chdir(DASHBOARD_DIR)
    
    print("=" * 60)
    print("🏡 Saito's Airbnb Execution Dashboard Server")
    print("=" * 60)
    print(f"Dashboard directory: {DASHBOARD_DIR}")
    print(f"Server starting on port {PORT}")
    print(f"Access dashboard at: http://localhost:{PORT}")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except OSError as e:
        print(f"Error starting server: {e}")
        print(f"Port {PORT} may already be in use")
        sys.exit(1)

if __name__ == "__main__":
    main()