# Migration Guide: From Single-Tool to Multi-Tool Generator

## Overview

This guide helps you migrate from the original Lovable.dev-specific prompt generator to the new enhanced multi-tool system.

## What's New

### 🆕 Multi-Tool Support
- **Before**: Only Lovable.dev
- **Now**: 12 tools including Lovable.dev, Bolt.new, Bubble, FlutterFlow, and more

### 🆕 Stage-Specific Prompts
- **Before**: Generic prompts
- **Now**: Development stage-aware prompts (planning, implementation, testing, etc.)

### 🆕 Enhanced RAG
- **Before**: Simple document retrieval
- **Now**: Tool-specific, filtered semantic search with metadata

### 🆕 Better UI
- **Before**: Basic form interface
- **Now**: Modern interface with tool selection, validation, and export options

## Migration Steps

### 1. File Updates

#### Old Files (Keep for Reference)
- `src/apps/streamlit_app.py` - Original app
- `src/generators/build_prompt.py` - Original generator

#### New Files (Use These)
- `src/apps/streamlit_app_enhanced.py` - Enhanced multi-tool app
- `src/generators/tool_specific_generator.py` - New enhanced generator

### 2. Running the New System

#### Start Enhanced App
```bash
# Instead of:
streamlit run src/apps/streamlit_app.py

# Use:
streamlit run src/apps/streamlit_app_enhanced.py
```

#### Import Changes
```python
# Instead of:
from src.generators.build_prompt import LovablePromptGenerator

# Use:
from src.generators.tool_specific_generator import ToolSpecificPromptGenerator
```

### 3. API Changes

#### Generator Initialization
```python
# Old way:
generator = LovablePromptGenerator()

# New way:
generator = ToolSpecificPromptGenerator()
```

#### Prompt Generation
```python
# Old way:
prompt = generator.generate_prompt(task_context, project_info)

# New way:
# First, update your TaskContext to include tool and stage
task_context = TaskContext(
    task_type="build login page",
    project_name="My App",
    description="...",
    tool="lovable",          # NEW: specify tool
    stage="implementation",  # NEW: specify stage
    technical_requirements=[...],
    ui_requirements=[...],
    constraints=[...]
)

# Add tool to ProjectInfo
project_info = ProjectInfo(
    name="My App",
    description="...",
    tech_stack=[...],
    target_audience="...",
    requirements=[],
    tool="lovable"  # NEW: specify tool
)

# Generate stage-specific prompt
prompt = generator.generate_stage_prompt(task_context, project_info)
```

### 4. Feature Mapping

| Old Feature | New Feature | Notes |
|-------------|-------------|-------|
| `generate_prompt()` | `generate_stage_prompt()` | Now requires tool and stage |
| `get_task_suggestions()` | `get_tool_suggestions()` | Tool-specific suggestions |
| `validate_prompt()` | `validate_prompt()` | Enhanced with tool-specific rules |
| `get_relevant_context()` | `get_relevant_context()` | Now filtered by tool |
| N/A | `get_available_tools()` | List all supported tools |
| N/A | `get_tool_info()` | Get tool configuration |
| N/A | `get_tool_stages()` | Get tool-specific stages |

### 5. Configuration Updates

#### Tool Selection
The new system requires you to specify which tool you're using:

```python
# Available tools:
tools = generator.get_available_tools()
# ['lovable', 'bolt', 'bubble', 'flutterflow', 'framer', ...]

# Tool information:
info = generator.get_tool_info('lovable')
# Returns tool configuration, stages, components
```

#### Development Stages
Each tool has specific stages:

```python
# Get stages for a tool:
stages = generator.get_tool_stages('lovable')
# ['planning', 'architecture', 'component_design', 'implementation', ...]

# Use in TaskContext:
task_context.stage = 'implementation'
```

## Example Migration

### Before (Old System)
```python
from src.generators.build_prompt import LovablePromptGenerator, TaskContext, ProjectInfo

generator = LovablePromptGenerator()

task_context = TaskContext(
    task_type="build dashboard",
    project_name="Analytics App",
    description="Create a data visualization dashboard",
    technical_requirements=["Chart.js", "API integration"],
    ui_requirements=["Responsive design", "Dark theme"],
    constraints=["Use TypeScript"]
)

project_info = ProjectInfo(
    name="Analytics App",
    description="Business analytics platform",
    tech_stack=["React", "TypeScript"],
    target_audience="Business users",
    requirements=[]
)

prompt = generator.generate_prompt(task_context, project_info)
```

### After (New System)
```python
from src.generators.tool_specific_generator import ToolSpecificPromptGenerator, TaskContext, ProjectInfo

generator = ToolSpecificPromptGenerator()

task_context = TaskContext(
    task_type="build dashboard",
    project_name="Analytics App", 
    description="Create a data visualization dashboard",
    tool="lovable",                    # NEW: specify tool
    stage="implementation",            # NEW: specify stage
    technical_requirements=["Chart.js", "API integration"],
    ui_requirements=["Responsive design", "Dark theme"],
    constraints=["Use TypeScript"]
)

project_info = ProjectInfo(
    name="Analytics App",
    description="Business analytics platform", 
    tech_stack=["React", "TypeScript"],
    target_audience="Business users",
    requirements=[],
    tool="lovable"                     # NEW: specify tool
)

# NEW: Generate stage-specific prompt
prompt = generator.generate_stage_prompt(task_context, project_info)
```

## Benefits of Migration

### 1. **Tool Flexibility**
- Switch between tools easily
- Compare different tools for the same project
- Use tool-specific best practices

### 2. **Better Prompts**
- Stage-aware prompt generation
- Tool-specific documentation context
- Enhanced validation and scoring

### 3. **Improved Workflow**
- Structured development stages
- Component-focused prompts
- Better export options

### 4. **Future-Proof**
- Easy to add new tools
- Extensible architecture
- Continuous improvements

## Troubleshooting

### Common Issues

#### 1. Import Errors
```python
# Error: ModuleNotFoundError
# Solution: Check file paths and ensure new files exist
```

#### 2. Missing Tool Configuration
```python
# Error: Tool 'xyz' not supported
# Solution: Check available tools with generator.get_available_tools()
```

#### 3. Stage Not Found
```python
# Error: Invalid stage
# Solution: Use generator.get_tool_stages('tool_name') to see valid stages
```

## Backward Compatibility

### Keep Old System Running
You can run both systems simultaneously:
- Old system: `streamlit run src/apps/streamlit_app.py`
- New system: `streamlit run src/apps/streamlit_app_enhanced.py`

### Gradual Migration
1. **Week 1**: Test new system with Lovable.dev projects
2. **Week 2**: Try other tools (Bolt.new, Bubble)
3. **Week 3**: Migrate all projects to new system
4. **Week 4**: Fully switch to enhanced system

## Next Steps

1. **Test the enhanced system** with your existing projects
2. **Explore new tools** available in the system
3. **Experiment with stages** for better prompt quality
4. **Provide feedback** for further improvements

## Support

- **Issues**: Create GitHub issues for bugs or questions
- **Documentation**: Check `README_ENHANCED.md` for detailed usage
- **Examples**: Run `test_basic_functionality.py` for examples

---

*Happy prompting with the enhanced multi-tool system!* 🚀
