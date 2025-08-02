#!/usr/bin/env python3
"""
Unified server launcher for RAG Application
Supports both development and production modes with Windows compatibility
"""

import os
import sys
import signal
import argparse
import socket
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Shutting down server...")
    sys.exit(0)

def check_port_available(host, port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result != 0
    except:
        return False

def find_available_port(host, start_port=5000, end_port=5100):
    """Find an available port in the given range"""
    for port in range(start_port, end_port):
        if check_port_available(host, port):
            return port
    return None

def run_development_server(host='127.0.0.1', port=5000, debug=True):
    """Run the Flask development server"""
    
    # Set up signal handling
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check if port is available
    if not check_port_available(host, port):
        print(f"⚠️  Port {port} is busy. Finding alternative...")
        new_port = find_available_port(host, port, port + 50)
        if new_port:
            port = new_port
            print(f"✅ Using port {port} instead")
        else:
            print("❌ No available ports found")
            return False
    
    try:
        from app import app
        
        print("🚀 RAG Application - Development Server")
        print("=" * 50)
        print(f"📋 Available at: http://{host}:{port}")
        print("💡 Press Ctrl+C to stop the server")
        if debug:
            print("⚡ Debug mode enabled - changes will restart the server")
        print("-" * 50)
        
        # Configure app for development
        app.config.update(
            DEBUG=debug,
            SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
            MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
        )
        
        # Run with optimal settings for Windows
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=debug,
            use_debugger=debug,
            threaded=True
        )
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        return False

def run_production_server(host='0.0.0.0', port=8000):
    """Run the production server using Waitress"""
    
    try:
        from waitress import serve
        from app import app
        
        # Production configuration
        app.config.update(
            DEBUG=False,
            SECRET_KEY=os.environ.get('SECRET_KEY', 'change-this-in-production'),
            MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
        )
        
        print("🚀 RAG Application - Production Server")
        print("=" * 50)
        print(f"📋 Available at: http://{host}:{port}")
        print("💡 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        serve(app, host=host, port=port, threads=4)
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except ImportError:
        print("❌ Waitress not installed. Install with: pip install waitress")
        return False
    except Exception as e:
        print(f"❌ Production server failed: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def main():
    """Main entry point with command line arguments"""
    parser = argparse.ArgumentParser(description='RAG Application Server')
    parser.add_argument('--mode', choices=['dev', 'prod'], default='dev',
                      help='Server mode (dev/prod)')
    parser.add_argument('--host', default='127.0.0.1',
                      help='Host to bind to (default: 127.0.0.1 for dev, 0.0.0.0 for prod)')
    parser.add_argument('--port', type=int, 
                      help='Port to bind to (default: 5000 for dev, 8000 for prod)')
    parser.add_argument('--no-debug', action='store_true',
                      help='Disable debug mode in development')
    parser.add_argument('--install-deps', action='store_true',
                      help='Install dependencies before starting')
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_dependencies():
            sys.exit(1)
    
    # Set defaults based on mode
    if args.mode == 'prod':
        host = args.host if args.host != '127.0.0.1' else '0.0.0.0'
        port = args.port if args.port else 8000
        success = run_production_server(host, port)
    else:
        host = args.host
        port = args.port if args.port else 5000
        debug = not args.no_debug
        success = run_development_server(host, port, debug)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
