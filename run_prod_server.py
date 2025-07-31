#!/usr/bin/env python3
"""
Production server configuration for AI Tool Prompt Generator
Uses Waitress WSGI server for better production deployment
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

def create_app():
    """Create and configure Flask app for production"""
    from app import app
    
    # Production configuration
    app.config.update(
        DEBUG=False,
        TESTING=False,
        SECRET_KEY=os.environ.get('SECRET_KEY', 'change-this-in-production'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
        JSON_SORT_KEYS=False,
        # Add security headers
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )
    
    return app

def run_production_server(host='0.0.0.0', port=8000):
    """Run the production server using Waitress"""
    try:
        from waitress import serve
        app = create_app()
        
        print("🚀 Starting AI Tool Prompt Generator (Production Mode)")
        print(f"📋 Available at: http://{host}:{port}")
        print("🔒 Running in production mode")
        print("-" * 50)
        
        serve(
            app,
            host=host,
            port=port,
            threads=6,
            url_scheme='http',
            ident='AI-Tool-Generator/1.0'
        )
        
    except ImportError:
        print("❌ Waitress not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'waitress'])
        
        # Try again
        from waitress import serve
        app = create_app()
        serve(app, host=host, port=port, threads=6)
        
    except Exception as e:
        print(f"❌ Production server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run AI Tool Prompt Generator production server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to (default: 8000)')
    
    args = parser.parse_args()
    
    run_production_server(host=args.host, port=args.port)
