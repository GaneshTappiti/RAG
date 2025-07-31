"""
Test Script for LLM UI/UX Generator
Tests the integration of LLM response generation
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.generators.llm_generator import LLMUIGenerator

def test_llm_generation():
    """Test the LLM UI/UX generation functionality"""
    
    print("🧪 Testing LLM UI/UX Generator...")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Check if API key is available
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in environment variables")
        print("📝 Please add your Google API key to a .env file:")
        print("   GOOGLE_API_KEY=your_key_here")
        return False
    
    print("✅ Google API key found")
    
    # Initialize generator
    try:
        generator = LLMUIGenerator()
        print("✅ LLM generator initialized successfully")
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize LLM generator: {e}")
        return False
    
    # Test prompt
    test_prompt = """UI/UX Page-by-Page Design Plan for Cross-Device App

You are a senior UI/UX designer with 10+ years of experience designing responsive, production-ready interfaces for both mobile and desktop applications.

App Details:
- **App Name**: TaskFlow
- **Platform**: Web
- **Design Style**: Minimal
- **Style Description**: Clean, modern interface with subtle shadows
- **App Idea**: A simple task management app where users can create, organize, and track their daily tasks with categories and priorities
- **Target Users**: Busy professionals
- **Selected Tool**: Lovable

Generate a detailed UI/UX design plan for this app."""

    app_details = {
        'app_name': 'TaskFlow',
        'platform': 'Web',
        'design_style': 'Minimal',
        'style_description': 'Clean, modern interface with subtle shadows',
        'app_idea': 'A simple task management app where users can create, organize, and track their daily tasks with categories and priorities',
        'target_users': 'Busy professionals',
        'selected_tool': 'lovable'
    }
    
    print("\n🚀 Generating UI/UX design...")
    print("📝 Test App: TaskFlow (Task Management)")
    
    try:
        # Generate response
        result = generator.generate_ui_response(test_prompt, app_details)
        
        if result['success']:
            print("✅ LLM generation successful!")
            print(f"📊 Model used: {result['model_used']}")
            print(f"📏 Prompt length: {result['prompt_length']} characters")
            print(f"📏 Response length: {result['response_length']} characters")
            
            # Validate quality
            quality = generator.validate_response_quality(result['generated_ui_design'])
            print(f"🎯 Quality score: {quality['overall_quality_score']:.2f}")
            print(f"📱 Pages designed: {quality['estimated_pages']}")
            print(f"⭐ Quality rating: {quality['quality_rating']}")
            
            # Show first 500 characters of response
            response_preview = result['generated_ui_design'][:500]
            print(f"\n📄 Response Preview (first 500 chars):")
            print("-" * 50)
            print(response_preview)
            if len(result['generated_ui_design']) > 500:
                print("... (truncated)")
            print("-" * 50)
            
            return True
        else:
            print(f"❌ LLM generation failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR during generation: {e}")
        return False

def main():
    """Main test function"""
    print("🎨 LLM UI/UX Generator Test Suite")
    print("=" * 50)
    
    success = test_llm_generation()
    
    if success:
        print("\n🎉 All tests passed!")
        print("✅ Your LLM integration is working correctly")
        print("🚀 You can now run your Flask app with: python app.py")
    else:
        print("\n❌ Tests failed!")
        print("🔧 Please check your Google API key and internet connection")

if __name__ == "__main__":
    main()
