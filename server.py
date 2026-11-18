#!/usr/bin/env python3
"""
Main Entry Point for AI Virtual Assistant
Runs the HTTP server and serves the chat interface and REST API.
"""
import sys
import os

# Ensure current working directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import run_server

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port=port)

