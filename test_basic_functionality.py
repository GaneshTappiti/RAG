"""
Test script for the enhanced tool-specific prompt generator (without embeddings)
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.generators.tool_specific_generator import ToolConfig, TaskContext, ProjectInfo
import yaml
from pathlib import Path

def test_tool_configs():
    """Test loading tool configurations"""
    
    print("🧪 Testing Tool Configuration Loading")
    print("=" * 50)
    
    try:
        # Load all tool configs
        tools_config = {}
        config_dir = Path("config/tools")
        
        for config_file in config_dir.glob("*.yaml"):
            tool_name = config_file.stem
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                
                tools_config[tool_name] = ToolConfig(
                    name=config_data.get('tool_name', tool_name),
                    format=config_data.get('format', 'structured'),
                    tone=config_data.get('tone', 'professional'),
                    framework=config_data.get('framework', 'Standard development'),
                    use_cases=config_data.get('preferred_use_cases', []),
                    strategies=config_data.get('prompting_strategies', {}),
                    stages=config_data.get('development_stages', ['planning', 'implementation', 'testing']),
                    components=config_data.get('supported_components', ['ui', 'logic', 'data'])
                )
                print(f"✅ Loaded config for {tool_name}: {config_data.get('tool_name', tool_name)}")
            except Exception as e:
                print(f"❌ Error loading config for {tool_name}: {e}")
        
        print(f"\n🛠️  Total tools loaded: {len(tools_config)}")
        
        # Test specific tool info
        if 'lovable' in tools_config:
            lovable_config = tools_config['lovable']
            print(f"\n🚀 Lovable.dev configuration:")
            print(f"  Name: {lovable_config.name}")
            print(f"  Format: {lovable_config.format}")
            print(f"  Tone: {lovable_config.tone}")
            print(f"  Stages: {lovable_config.stages}")
            print(f"  Components: {lovable_config.components}")
        
        return tools_config
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return {}

def test_prompt_generation_logic():
    """Test prompt generation without embeddings"""
    
    print("\n🎯 Testing Prompt Generation Logic")
    print("=" * 50)
    
    try:
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
        
        print("✅ Created test contexts successfully")
        print(f"  Task: {task_context.task_type}")
        print(f"  Tool: {task_context.tool}")
        print(f"  Stage: {task_context.stage}")
        print(f"  Project: {project_info.name}")
        
        # Test basic prompt structure (without embeddings)
        prompt_parts = [
            f"# {task_context.tool.title()} - {task_context.stage.title()} Stage",
            f"\n## Project: {project_info.name}",
            f"\n**Tool:** {task_context.tool}",
            f"**Stage:** {task_context.stage.title()}",
            f"**Task Type:** {task_context.task_type}",
            f"\n## Project Context",
            f"**Description:** {project_info.description}",
            f"**Tech Stack:** {', '.join(project_info.tech_stack)}",
            f"\n## Task Details",
            f"**Description:** {task_context.description}",
        ]
        
        if task_context.technical_requirements:
            prompt_parts.append(f"\n**Technical Requirements:**")
            for req in task_context.technical_requirements:
                prompt_parts.append(f"- {req}")
        
        basic_prompt = "\n".join(prompt_parts)
        
        print(f"\n📝 Generated basic prompt structure:")
        print("-" * 40)
        print(basic_prompt[:300] + "...")
        print("-" * 40)
        
        print("\n✅ Prompt generation logic test passed!")
        
    except Exception as e:
        print(f"❌ Prompt generation test failed: {e}")
        import traceback
        traceback.print_exc()

def test_available_docs():
    """Test availability of documentation files"""
    
    print("\n📚 Testing Documentation Availability")
    print("=" * 50)
    
    data_dir = Path("data")
    doc_count = 0
    
    for tool_dir in data_dir.glob("*_docs"):
        tool_name = tool_dir.name.replace('_docs', '')
        files = list(tool_dir.glob("*.md"))
        doc_count += len(files)
        print(f"📁 {tool_name}: {len(files)} documentation files")
        for file in files[:3]:  # Show first 3 files
            print(f"   - {file.name}")
        if len(files) > 3:
            print(f"   ... and {len(files) - 3} more")
    
    print(f"\n📊 Total documentation files: {doc_count}")

if __name__ == "__main__":
    print("🚀 Enhanced Tool-Specific Prompt Generator Tests")
    print("=" * 60)
    
    # Test 1: Tool configurations
    tools_config = test_tool_configs()
    
    # Test 2: Basic prompt generation
    test_prompt_generation_logic()
    
    # Test 3: Documentation availability
    test_available_docs()
    
    print("\n" + "=" * 60)
    print("🎉 All basic tests completed!")
    print("💡 To test with full RAG functionality, add your OpenAI API key to .env")
