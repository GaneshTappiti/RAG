#!/usr/bin/env python3
"""
Setup script for RAG Application
Handles dependency installation and basic configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        return True
    except subprocess.CalledProcessError:
        return False

def setup_environment():
    """Set up the application environment"""
    print("🔧 Setting up RAG Application Environment")
    print("=" * 50)
    
    # Required packages
    packages = [
        'flask>=2.0.0',
        'chromadb>=0.5.0',
        'langchain>=0.2.2',
        'langchain-community>=0.2.3',
        'langchain-google-genai>=1.0.0',
        'google-generativeai>=0.3.0',
        'python-dotenv>=1.0.1',
        'waitress>=2.1.0',
        'unstructured>=0.11.8',
        'numpy>=1.24.0',
        'jinja2>=3.1.0',
        'pyyaml>=6.0',
        'streamlit>=1.28.0'
    ]
    
    print("📦 Installing/updating required packages...")
    
    failed_packages = []
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed successfully")
        else:
            print(f"❌ Failed to install {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️  Failed to install: {', '.join(failed_packages)}")
        print("💡 Try installing them manually or check your internet connection")
        return False
    else:
        print("\n🎉 All packages installed successfully!")
        return True

def create_env_file():
    """Create .env file template"""
    env_path = Path('.env.example')
    if not env_path.exists():
        env_content = """# RAG Application Environment Variables
# Copy this file to .env and fill in your actual values

# Google Gemini API Key (required for AI features)
GOOGLE_API_KEY=your_gemini_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secret_key_here

# Optional: Custom settings
MAX_CONTENT_LENGTH=16777216
"""
        env_path.write_text(env_content)
        print("✅ Created .env.example file")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Database
*.sqlite3
*.db

# Logs
*.log

# ChromaDB
chroma_*/
"""
        gitignore_path.write_text(gitignore_content)
        print("✅ Created .gitignore file")

def test_installation():
    """Test if everything is working"""
    print("\n🧪 Testing installation...")
    
    try:
        import flask
        print("✅ Flask working")
    except ImportError:
        print("❌ Flask not working")
        return False
    
    try:
        import chromadb
        print("✅ ChromaDB working")
    except ImportError:
        print("❌ ChromaDB not working")
        return False
    
    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        print("✅ Google Gemini embeddings working")
    except ImportError:
        print("❌ Google Gemini embeddings not working")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 RAG Application Setup")
    print("=" * 40)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Setup failed!")
        return False
    
    # Create configuration files
    create_env_file()
    create_gitignore()
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed!")
        return False
    
    print("\n✨ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Copy .env.example to .env and add your Google API key")
    print("2. Run: python scripts/server.py --mode dev")
    print("3. Visit: http://127.0.0.1:5000")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
