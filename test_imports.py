#!/usr/bin/env python3
"""
Simple test script to verify all imports work correctly
"""

def test_imports():
    """Test all critical imports for the application"""
    
    print("Testing imports...")
    
    try:
        import flask
        version = getattr(flask, '__version__', 'unknown')
        print(f"✅ Flask {version} imported successfully")
    except Exception as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import waitress
        version = getattr(waitress, '__version__', 'unknown')
        print(f"✅ Waitress {version} imported successfully")
    except Exception as e:
        print(f"❌ Waitress import failed: {e}")
        return False
    
    try:
        from src.generators.llm_generator import LLMUIGenerator
        print("✅ LLMUIGenerator imported successfully")
    except Exception as e:
        print(f"❌ LLMUIGenerator import failed: {e}")
        return False
    
    try:
        from src.generators.enhanced_generator import EnhancedMultiToolGenerator
        print("✅ EnhancedMultiToolGenerator imported successfully")
    except Exception as e:
        print(f"❌ EnhancedMultiToolGenerator import failed: {e}")
        return False
    
    try:
        from src.core.types import SupportedTool, ProjectInfo, TaskContext, PromptStage
        print("✅ Core types imported successfully")
    except Exception as e:
        print(f"❌ Core types import failed: {e}")
        return False
    
    try:
        import app
        print("✅ Main app module imported successfully")
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        return False
    
    print("\n🎉 All imports successful!")
    return True

if __name__ == "__main__":
    success = test_imports()
    if not success:
        exit(1)
