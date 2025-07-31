"""
Test script for the enhanced tool-specific prompt generator
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.generators.tool_specific_generator import ToolSpecificPromptGenerator, TaskContext, ProjectInfo

def test_generator():
    """Test the enhanced generator with different tools"""
    
    print("🧪 Testing Enhanced Tool-Specific Prompt Generator")
    print("=" * 60)
    
    try:
        # Initialize generator
        print("📚 Initializing generator...")
        generator = ToolSpecificPromptGenerator()
        
        # Test available tools
        print(f"🛠️  Available tools: {generator.get_available_tools()}")
        
        # Test with Lovable.dev
        print("\n🚀 Testing with Lovable.dev...")
        tool_info = generator.get_tool_info('lovable')
        print(f"Tool info: {tool_info}")
        
        # Create test context
        task_context = TaskContext(
            task_type="build login page",
            project_name="Task Manager Pro",
            description="Create a secure login page with email/password authentication and social login options",
            tool="lovable",
            stage="implementation",
            technical_requirements=["NextAuth.js integration", "Form validation", "Error handling"],
            ui_requirements=["Clean modern design", "Mobile responsive", "Dark mode support"],
            constraints=["Use Tailwind CSS", "Follow security best practices"]
        )
        
        project_info = ProjectInfo(
            name="Task Manager Pro",
            description="A modern task management application for teams",
            tech_stack=["React", "Next.js", "TypeScript", "Tailwind CSS"],
            target_audience="Professional teams",
            requirements=[],
            tool="lovable"
        )
        
        # Generate prompt
        print("🎯 Generating prompt...")
        prompt = generator.generate_stage_prompt(task_context, project_info)
        
        print(f"\n📝 Generated prompt (first 500 chars):")
        print("-" * 50)
        print(prompt[:500] + "...")
        print("-" * 50)
        
        # Test validation
        print("\n🔍 Testing validation...")
        validation = generator.validate_prompt(prompt, 'lovable')
        print(f"Validation result: {validation}")
        
        # Test suggestions
        print("\n💡 Testing suggestions...")
        suggestions = generator.get_tool_suggestions('lovable', 'web_app')
        print(f"Suggestions: {suggestions}")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_generator()
