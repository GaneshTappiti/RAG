"""
Setup Script for LLM Integration Fix
Helps configure the environment and test the integration
"""

import os
import sys

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking Environment Configuration...")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    
    # Check for .env file
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file found")
        
        # Check for Google API key
        from dotenv import load_dotenv
        load_dotenv()
        
        if os.environ.get('GOOGLE_API_KEY'):
            print("✅ GOOGLE_API_KEY found in environment")
        else:
            print("❌ GOOGLE_API_KEY not found in .env file")
            print("📝 Please add: GOOGLE_API_KEY=your_key_here")
            return False
    else:
        print("❌ .env file not found")
        print("📝 Creating sample .env file...")
        
        with open(env_file, 'w') as f:
            f.write("# Google API Key for Gemini\n")
            f.write("GOOGLE_API_KEY=your_google_api_key_here\n")
            f.write("\n# Optional: OpenAI API Key\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
        
        print("✅ Sample .env file created")
        print("📝 Please edit .env and add your actual API keys")
        return False
    
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n🔧 Checking Dependencies...")
    print("=" * 50)
    
    required_packages = [
        'flask',
        'langchain-google-genai',
        'python-dotenv',
        'chromadb'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Missing packages: {', '.join(missing_packages)}")
        print("💡 Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🧪 Testing Basic Functionality...")
    print("=" * 50)
    
    try:
        # Test imports
        from src.generators.llm_generator import LLMUIGenerator
        print("✅ LLM generator import successful")
        
        # Test initialization (without API call)
        print("✅ All imports working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 LLM Integration Setup & Diagnostics")
    print("=" * 60)
    
    checks = [
        ("Environment", check_environment),
        ("Dependencies", check_dependencies),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 All checks passed!")
        print("✅ Your environment is properly configured")
        print("\n📋 Next Steps:")
        print("   1. Run: python test_llm_integration.py")
        print("   2. If test passes, run: python app.py")
        print("   3. Open: http://localhost:5000")
    else:
        print("❌ Some checks failed!")
        print("🔧 Please resolve the issues above and run this script again")
    
    print("\n💡 Need help?")
    print("   - Get Google API key: https://aistudio.google.com/app/apikey")
    print("   - Install dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
