#!/usr/bin/env python3
"""
Test script to validate the web application can start properly
"""

def test_app_creation():
    """Test that the Flask app can be created and configured"""
    
    print("Testing Flask app creation...")
    
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
            
        print("\n🎉 Flask app validation successful!")
        return True
        
    except Exception as e:
        print(f"❌ App validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_app_creation()
    if not success:
        exit(1)
