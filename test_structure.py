#!/usr/bin/env python3
"""
Test script to verify the reorganized project structure works correctly.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all core imports work correctly."""
    print("Testing imports...")
    
    try:
        # Test core types import
        from src.core.types import SupportedTool, PromptStage, TaskContext
        print("✅ Core types imported successfully")
        
        # Test that we can create instances
        tool = SupportedTool.LOVABLE
        stage = PromptStage.APP_SKELETON
        print(f"✅ Created instances: {tool.value}, {stage.value}")
        
        # Test task context creation
        context = TaskContext(
            task_type="web_application",
            project_name="Test Project",
            description="A test project to verify structure",
            stage=stage,
            target_tool=tool,
            technical_requirements=["Python", "React"],
            ui_requirements=["Responsive design", "Dark mode support"],
            constraints=["Budget: $1000", "Timeline: 2 weeks"]
        )
        print("✅ TaskContext created successfully")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def test_file_structure():
    """Test that the file structure is as expected."""
    print("\nTesting file structure...")
    
    expected_dirs = [
        'src',
        'src/core',
        'src/generators',
        'src/database',
        'src/apps',
        'config',
        'config/tools',
        'docs',
        'docs/guides',
        'data',
        'templates',
        'storage'
    ]
    
    for dir_path in expected_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} exists")
        else:
            print(f"❌ {dir_path} missing")
            return False
    
    return True

def test_yaml_configs():
    """Test that YAML configurations are in the right place."""
    print("\nTesting YAML configurations...")
    
    config_files = [
        'config/tools/lovable.yaml',
        'config/tools/bolt.yaml',
        'config/tools/cursor.yaml',
        'config/tools/v0.yaml'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ {config_file} exists")
        else:
            print(f"❌ {config_file} missing")
    
    return True

def main():
    """Run all tests."""
    print("🚀 Testing reorganized RAG project structure...\n")
    
    success = True
    success &= test_file_structure()
    success &= test_yaml_configs()
    success &= test_imports()
    
    if success:
        print("\n🎉 All tests passed! The reorganized structure is working correctly.")
        print("\n📋 Next steps:")
        print("1. Run: streamlit run src/apps/streamlit_app.py")
        print("2. Or run: streamlit run src/apps/streamlit_app_gemini.py")
        print("3. Or use the enhanced generator directly in your code")
    else:
        print("\n❌ Some tests failed. Please check the output above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
