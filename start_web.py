#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Downloader - Web App Launcher
Quick launcher for the web application
"""

import sys
import os
from pathlib import Path

# Add web directory to path
web_dir = Path(__file__).parent / "web"
sys.path.insert(0, str(web_dir))

# Import and run app
from app import app, initialize_downloader

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌐 Instagram Downloader - Web Interface")
    print("="*60)
    print("\nInitializing...")
    
    if initialize_downloader():
        print("✅ Downloader initialized")
        print("\n🚀 Starting server...")
        print("📱 Open browser: http://localhost:5000")
        print("\n⚠️  Press Ctrl+C to stop")
        print("="*60 + "\n")
        
        try:
            app.run(
                debug=False,
                host='0.0.0.0',
                port=5000,
                threaded=True
            )
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")
    else:
        print("❌ Failed to initialize")
        sys.exit(1)
