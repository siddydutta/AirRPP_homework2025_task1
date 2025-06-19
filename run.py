#!/usr/bin/env python3
"""
Simple script to run the FastAPI application with initial data setup.
"""

import os
import sys
import subprocess

def main():
    print("Shop API Setup and Run Script")
    print("=" * 40)
    
    # Check if we should initialize data
    if len(sys.argv) > 1 and sys.argv[1] == "--init-data":
        print("Initializing database with sample data...")
        try:
            subprocess.run([sys.executable, "init_data.py"], check=True)
            print("✓ Database initialized successfully!")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error initializing database: {e}")
            return 1
    
    print("Starting FastAPI server...")
    print("API will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("-" * 40)
    
    try:
        # Run the FastAPI application
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n" + "=" * 40)
        print("Server stopped by user")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
