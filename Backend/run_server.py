#!/usr/bin/env python3
"""
CIMR-OS Server Startup Script
Run this script to start the FastAPI server
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the Backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    print("Starting CIMR-OS FastAPI Server...")
    print("Server will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        "Server:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    )
