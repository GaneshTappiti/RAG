#!/usr/bin/env python3
"""
Development server launcher for AI Tool Prompt Generator
Provides robust Flask development server with better Windows compatibility
"""

import os
import sys
import signal
import argparse
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\n🛑 Shutting down server gracefully...')
    sys.exit(0)

def run_server(host='127.0.0.1', port=5000, debug=True, use_reloader=True):
    """Run the Flask development server with optimal Windows settings"""
    
    # Set up signal handling
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        from app import app
        
        print("🚀 Starting AI Tool Prompt Generator Web App...")
        print(f"📋 Available at: http://{host}:{port}")
        print("💡 Press Ctrl+C to stop the server")
        print("⚡ Auto-reload enabled - changes will restart the server")
        print("-" * 50)
        
        # Configure app for development
        app.config.update(
            DEBUG=debug,
            TESTING=False,
            SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
            MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
            JSON_SORT_KEYS=False
        )
        
        # Run with optimal settings for Windows
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True,
            use_reloader=use_reloader,
            reloader_type='stat',  # Better for Windows
            extra_files=None,  # Let Flask auto-detect files to watch
            load_dotenv=True
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the correct directory and dependencies are installed")
        sys.exit(1)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use")
            print(f"💡 Try using a different port: python {__file__} --port 5001")
        else:
            print(f"❌ OS Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def main():
    """Main entry point with command line arguments"""
    parser = argparse.ArgumentParser(description='Run AI Tool Prompt Generator development server')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to (default: 5000)')
    parser.add_argument('--no-debug', action='store_true', help='Disable debug mode')
    parser.add_argument('--no-reload', action='store_true', help='Disable auto-reload')
    
    args = parser.parse_args()
    
    run_server(
        host=args.host,
        port=args.port,
        debug=not args.no_debug,
        use_reloader=not args.no_reload
    )

if __name__ == '__main__':
    main()
