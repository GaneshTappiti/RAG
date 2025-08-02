#!/usr/bin/env python3
"""
Comprehensive test suite for the RAG application
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all critical imports for the application"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print(f"✅ Flask {getattr(flask, '__version__', 'unknown')} imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import chromadb
        print("✅ ChromaDB imported successfully")
    except ImportError as e:
        print(f"❌ ChromaDB import failed: {e}")
        return False
    
    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        print("✅ Google Gemini embeddings imported successfully")
    except ImportError as e:
        print(f"❌ Google Gemini embeddings import failed: {e}")
        return False
    
    try:
        from src.core.types import SupportedTool, ProjectInfo
        print("✅ Core types imported successfully")
    except ImportError as e:
        print(f"❌ Core types import failed: {e}")
        return False
    
    try:
        from src.generators.enhanced_generator import EnhancedMultiToolGenerator
        print("✅ Enhanced generator imported successfully")
    except ImportError as e:
        print(f"❌ Enhanced generator import failed: {e}")
        return False
    
    return True

def test_app():
    """Test Flask app creation and basic functionality"""
    print("🔍 Testing Flask app...")
    
    try:
        from app import app, generator, llm_generator
        print("✅ App imported successfully")
        
        # Test app configuration
        print(f"✅ App name: {app.name}")
        print(f"✅ Secret key configured: {'Yes' if app.secret_key else 'No'}")
        
        # Test generator instances
        print(f"✅ Generator type: {type(generator).__name__}")
        print(f"✅ LLM Generator type: {type(llm_generator).__name__}")
        
        # Test that we can create a test client
        with app.test_client() as client:
            print("✅ Test client created successfully")
            
        return True
        
    except Exception as e:
        print(f"❌ App test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Running RAG Application Tests")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("App Tests", test_app),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            failed += 1
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
