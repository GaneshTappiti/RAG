"""
Enhanced CLI Interface for Multi-Tool Prompt Generator with Google Gemini
Description: Command-line interface for generating optimized prompts for various AI development tools using Gemini RAG
"""

import argparse
import sys
import os
import json

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.core.types import TaskContext, ProjectInfo, PromptStage, SupportedTool, AppStructure, PageSpec, FlowConnection
from typing import List, Dict, Any, Literal

def interactive_mode():
    """Interactive prompt generation mode"""
    print("🚀 Multi-Tool Prompt Generator - Interactive Mode")
    print("=" * 60)
    
    # Tool Selection
    print("\n🛠️ AI Development Tool Selection")
    print("Available tools:")
    tools = {
        "1": SupportedTool.LOVABLE,
        "2": SupportedTool.UIZARD,
        "3": SupportedTool.ADALO,
        "4": SupportedTool.FLUTTERFLOW,
        "5": SupportedTool.FRAMER,
        "6": SupportedTool.BUBBLE
    }
    
    for key, tool in tools.items():
        print(f"{key}. {tool.value.title()}")
    
    tool_choice = input("Select development tool (1-6): ").strip()
    target_tool = tools.get(tool_choice, SupportedTool.LOVABLE)
    print(f"Selected: {target_tool.value.title()}")
    
    # Stage Selection
    print("\n📋 Development Stage")
    print("Available stages:")
    stages = {
        "1": PromptStage.APP_SKELETON,
        "2": PromptStage.PAGE_UI,
        "3": PromptStage.FLOW_CONNECTIONS,
        "4": PromptStage.FEATURE_SPECIFIC,
        "5": PromptStage.DEBUGGING,
        "6": PromptStage.OPTIMIZATION
    }
    
    for key, stage in stages.items():
        stage_name = stage.value.replace('_', ' ').title()
        print(f"{key}. {stage_name}")
    
    stage_choice = input("Select development stage (1-6): ").strip()
    target_stage = stages.get(stage_choice, PromptStage.APP_SKELETON)
    print(f"Selected: {target_stage.value.replace('_', ' ').title()}")
    
    # Project Information
    print("\n📋 Project Information")
    project_name = input("Project Name: ").strip() or "MyApp"
    project_description = input("Project Description: ").strip() or "A modern web application"
    target_audience = input("Target Audience: ").strip() or "General users"
    industry = input("Industry (optional): ").strip() or None
    
    complexity_input = input("Complexity Level (simple/medium/complex): ").strip().lower()
    complexity_level: Literal["simple", "medium", "complex"]
    if complexity_input in ["simple", "medium", "complex"]:
        complexity_level = complexity_input  # type: ignore
    else:
        complexity_level = "medium"
    
    # Technology Stack
    print("\nTechnology Stack (comma-separated):")
    print("Examples: Next.js, React, TypeScript, Tailwind CSS")
    tech_input = input("Tech Stack: ").strip()
    tech_stack = [tech.strip() for tech in tech_input.split(',') if tech.strip()] or ["Next.js", "React"]
    
    # Task Configuration
    print("\n🎯 Task Configuration")
    print("Available task types:")
    print("1. build complete application")
    print("2. create responsive dashboard")
    print("3. implement authentication")
    print("4. add payment integration")
    print("5. optimize performance")
    print("6. enhance accessibility")
    print("7. debug and refactor")
    print("8. custom")
    
    task_choice = input("Select task type (1-8): ").strip()
    task_types = {
        "1": "build complete application",
        "2": "create responsive dashboard", 
        "3": "implement authentication",
        "4": "add payment integration",
        "5": "optimize performance",
        "6": "enhance accessibility",
        "7": "debug and refactor"
    }
    
    if task_choice in task_types:
        task_type = task_types[task_choice]
    elif task_choice == "8":
        task_type = input("Enter custom task type: ").strip()
    else:
        task_type = "build complete application"
    
    task_description = input("Task Description: ").strip() or f"Create a modern {task_type}"
    
    # Requirements
    print("\n📝 Requirements (press Enter twice to finish each section)")
    
    print("Technical Requirements:")
    tech_requirements = []
    while True:
        req = input("- ").strip()
        if not req:
            break
        tech_requirements.append(req)
    
    print("UI/UX Requirements:")
    ui_requirements = []
    while True:
        req = input("- ").strip()
        if not req:
            break
        ui_requirements.append(req)
    
    print("Constraints:")
    constraints = []
    while True:
        constraint = input("- ").strip()
        if not constraint:
            break
        constraints.append(constraint)
    
    # Stage-specific data collection
    app_structure = None
    page_spec = None
    flow_connections = None
    
    if target_stage == PromptStage.APP_SKELETON:
        print("\n🏗️ App Structure (optional)")
        pages_input = input("Main pages (comma-separated): ").strip()
        if pages_input:
            pages = [page.strip() for page in pages_input.split(',')]
            features_input = input("Key features (comma-separated): ").strip()
            features = [feature.strip() for feature in features_input.split(',') if feature.strip()]
            
            app_structure = AppStructure(
                pages=pages,
                components=[],  # Can be filled later
                features=features,
                navigation_flow={}  # Can be defined later
            )
    
    elif target_stage == PromptStage.PAGE_UI:
        print("\n🎨 Page Specification")
        page_name = input("Page name: ").strip() or "Main Page"
        layout_type = input("Layout type (dashboard/form/list/custom): ").strip() or "custom"
        
        components_input = input("Required components (comma-separated): ").strip()
        components = [comp.strip() for comp in components_input.split(',') if comp.strip()]
        
        interactions_input = input("Key interactions (comma-separated): ").strip()
        interactions = [inter.strip() for inter in interactions_input.split(',') if inter.strip()]
        
        page_spec = PageSpec(
            page_name=page_name,
            layout_type=layout_type,
            components=components,
            interactions=interactions,
            data_requirements=[]  # Can be expanded
        )
    
    # Create data structures
    task_context = TaskContext(
        task_type=task_type,
        project_name=project_name,
        description=task_description,
        stage=target_stage,
        technical_requirements=tech_requirements,
        ui_requirements=ui_requirements,
        constraints=constraints,
        target_tool=target_tool,
        app_structure=app_structure,
        page_spec=page_spec,
        flow_connections=flow_connections
    )
    
    project_info = ProjectInfo(
        name=project_name,
        description=project_description,
        tech_stack=tech_stack,
        target_audience=target_audience,
        requirements=[],
        industry=industry,
        complexity_level=complexity_level
    )
    
    return task_context, project_info

def batch_mode(config_file: str):
    """Batch mode using JSON configuration file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Parse tool and stage
        tool_name = config.get('target_tool', 'lovable')
        stage_name = config.get('stage', 'app_skeleton')
        
        try:
            target_tool = SupportedTool(tool_name)
        except ValueError:
            target_tool = SupportedTool.LOVABLE
            
        try:
            target_stage = PromptStage(stage_name)
        except ValueError:
            target_stage = PromptStage.APP_SKELETON
        
        task_context_data = config['task_context']
        task_context_data['target_tool'] = target_tool
        task_context_data['stage'] = target_stage
        
        task_context = TaskContext(**task_context_data)
        project_info = ProjectInfo(**config['project_info'])
        
        return task_context, project_info
    
    except FileNotFoundError:
        print(f"❌ Configuration file {config_file} not found!")
        return None, None
    except KeyError as e:
        print(f"❌ Missing required field in configuration: {e}")
        return None, None
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return None, None

def generate_prompt_simple(task_context: TaskContext, project_info: ProjectInfo) -> str:
    """Generate a prompt using simple template approach"""
    
    tech_stack = ', '.join(project_info.tech_stack)
    tech_reqs = '\n'.join(f"- {req}" for req in task_context.technical_requirements)
    ui_reqs = '\n'.join(f"- {req}" for req in task_context.ui_requirements)
    constraints = '\n'.join(f"- {constraint}" for constraint in task_context.constraints)
    
    # Task-specific guidelines
    guidelines = get_task_guidelines(task_context.task_type)
    guidelines_text = '\n'.join(f"- {guideline}" for guideline in guidelines)
    
    prompt = f"""# {task_context.task_type.title()} - {project_info.name}

## 🎯 Project Overview
{project_info.description}

**Target Audience:** {project_info.target_audience}
**Technology Stack:** {tech_stack}

## 📋 Task Description
{task_context.description}

## ⚙️ Technical Requirements
{tech_reqs}

## 🎨 UI/UX Requirements
{ui_reqs}

## 🔒 Constraints & Guidelines
{constraints}

## 🚀 Implementation Guidelines
{guidelines_text}

## 📦 Expected Deliverables

### Core Features
- Fully functional {task_context.task_type.lower()}
- Responsive design that works on all devices
- Clean, modern UI following current design trends
- Proper error handling and loading states

### Technical Implementation
- Type-safe code with TypeScript
- Component-based architecture
- Proper state management
- API integration with error handling
- Performance optimizations

### Quality Standards
- WCAG 2.1 accessibility compliance
- SEO optimization
- Cross-browser compatibility
- Mobile-first responsive design
- Performance metrics (Core Web Vitals)

## 🎯 Success Criteria
- Application loads in under 2 seconds
- Responsive across all device sizes (mobile, tablet, desktop)
- Passes accessibility audits
- Clean, maintainable code structure
- Working deployment with proper CI/CD

## 📝 Implementation Steps
1. **Setup & Structure**: Initialize project with proper folder structure
2. **Core Components**: Build main UI components with TypeScript
3. **Functionality**: Implement core business logic
4. **Styling**: Apply responsive design with Tailwind CSS
5. **Testing**: Add proper error handling and validation
6. **Optimization**: Performance and accessibility improvements

Please implement this step by step, ensuring each component is thoroughly tested before moving to the next."""

    return prompt

def get_task_guidelines(task_type: str) -> List[str]:
    """Get specific guidelines based on task type"""
    guidelines_map = {
        "authentication": [
            "Use NextAuth.js for secure authentication",
            "Implement proper session management",
            "Add password strength validation",
            "Include social login options",
            "Ensure secure token handling"
        ],
        "dashboard": [
            "Use responsive grid layout",
            "Implement real-time data updates",
            "Add interactive charts and graphs",
            "Include filtering and search capabilities",
            "Optimize for mobile viewing"
        ],
        "ecommerce": [
            "Implement product catalog with search",
            "Add shopping cart functionality",
            "Include secure payment processing",
            "Optimize for conversion rates",
            "Mobile-first responsive design"
        ],
        "payment": [
            "Use Stripe or similar secure payment processor",
            "Implement proper error handling for failed payments",
            "Add receipt generation and email confirmation",
            "Ensure PCI compliance",
            "Include subscription and recurring payment support"
        ]
    }
    
    task_lower = task_type.lower()
    for key, guidelines in guidelines_map.items():
        if key in task_lower:
            return guidelines
    
    # Default guidelines
    return [
        "Follow modern web development best practices",
        "Ensure responsive design for all devices",
        "Implement proper error handling",
        "Use TypeScript for type safety",
        "Optimize for performance and accessibility"
    ]

def validate_prompt(prompt: str) -> Dict[str, Any]:
    """Validate the generated prompt"""
    score = 0
    issues = []
    
    # Check required sections
    required_sections = ['overview', 'description', 'requirements', 'technical', 'deliverables']
    for section in required_sections:
        if section.lower() in prompt.lower():
            score += 20
        else:
            issues.append(f"Missing {section} section")
    
    # Length check
    if 500 <= len(prompt) <= 3000:
        score += 10
    elif len(prompt) < 500:
        issues.append("Prompt is too short")
    else:
        issues.append("Prompt might be too long")
    
    return {
        'score': min(100, score),
        'is_valid': score >= 80,
        'issues': issues
    }

def save_example_config():
    """Save example configuration file"""
    example_config = {
        "target_tool": "lovable",
        "stage": "app_skeleton",
        "task_context": {
            "task_type": "build complete application",
            "project_name": "TaskMaster Pro",
            "description": "A comprehensive task management application with team collaboration features",
            "stage": "app_skeleton",
            "target_tool": "lovable",
            "technical_requirements": [
                "Next.js 14 with App Router",
                "TypeScript for type safety",
                "Prisma ORM with PostgreSQL",
                "NextAuth.js for authentication",
                "Real-time updates with WebSocket"
            ],
            "ui_requirements": [
                "Clean, modern interface design",
                "Drag and drop task management",
                "Mobile-responsive layout",
                "Dark mode support",
                "Interactive kanban board"
            ],
            "constraints": [
                "Load time under 2 seconds",
                "WCAG 2.1 accessibility compliance",
                "Cross-browser compatibility",
                "SEO optimized"
            ],
            "app_structure": {
                "pages": ["Landing", "Dashboard", "Tasks", "Team", "Settings"],
                "components": ["TaskCard", "KanbanBoard", "UserProfile"],
                "features": ["Task Management", "Team Collaboration", "Real-time Updates"],
                "navigation_flow": {
                    "Landing": ["Dashboard", "Login"],
                    "Dashboard": ["Tasks", "Team", "Settings"],
                    "Tasks": ["Dashboard", "Task Details"]
                }
            }
        },
        "project_info": {
            "name": "TaskMaster Pro",
            "description": "Professional task management platform for teams and organizations",
            "tech_stack": ["Next.js", "TypeScript", "Prisma", "PostgreSQL", "Tailwind CSS"],
            "target_audience": "Business professionals and project managers",
            "requirements": [],
            "industry": "Productivity Software",
            "complexity_level": "medium"
        }
    }
    
    with open('example_config.json', 'w', encoding='utf-8') as f:
        json.dump(example_config, f, indent=2)
    
    print("📄 Example configuration saved to 'example_config.json'")
    print("💡 This shows the new multi-tool, multi-stage structure")

def main():
    """Main CLI application"""
    parser = argparse.ArgumentParser(
        description="Generate optimized prompts for AI development tools using Google Gemini RAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_prompt_gemini.py                    # Interactive mode
  python generate_prompt_gemini.py -c config.json    # Batch mode
  python generate_prompt_gemini.py --example          # Save example config
  python generate_prompt_gemini.py -o prompt.md       # Save to file
  python generate_prompt_gemini.py --rag              # Use RAG retrieval
        """
    )
    
    parser.add_argument('-c', '--config', 
                       help='JSON configuration file for batch mode')
    parser.add_argument('-o', '--output', 
                       help='Output file to save the generated prompt')
    parser.add_argument('--example', action='store_true',
                       help='Save example configuration file')
    parser.add_argument('--validate', action='store_true', default=True,
                       help='Validate the generated prompt (default: True)')
    parser.add_argument('--rag', action='store_true',
                       help='Use RAG retrieval (requires vector database)')
    
    args = parser.parse_args()
    
    # Handle example config generation
    if args.example:
        save_example_config()
        return
    
    # Get task and project info
    if args.config:
        print("📋 Batch Mode - Loading configuration...")
        task_context, project_info = batch_mode(args.config)
        if not task_context or not project_info:
            sys.exit(1)
    else:
        task_context, project_info = interactive_mode()
    
    # Generate prompt
    print("\n🎨 Generating prompt...")
    
    if args.rag and os.path.exists("chroma_multi_tool_lovable"):
        print("🔍 Using Multi-Tool RAG retrieval...")
        try:
            from src.generators.enhanced_generator import EnhancedMultiToolGenerator
            generator = EnhancedMultiToolGenerator()
            result = generator.generate_enhanced_prompt(task_context)
            prompt = result.prompt
            
            # Display additional information
            print(f"🎯 Tool: {result.tool.value.title()}")
            print(f"📋 Stage: {result.stage.value.replace('_', ' ').title()}")
            print(f"📊 Confidence: {result.confidence_score:.2f}")
            if result.sources:
                print(f"📚 Sources: {len(result.sources)} references")
            if result.next_suggested_stage:
                print(f"➡️ Next Stage: {result.next_suggested_stage.value.replace('_', ' ').title()}")
                
        except ImportError as e:
            print(f"⚠️ Multi-tool generator unavailable: {e}")
            print("🔄 Falling back to simple generation...")
            prompt = generate_prompt_simple(task_context, project_info)
    else:
        prompt = generate_prompt_simple(task_context, project_info)
    
    # Validate prompt
    if args.validate:
        validation = validate_prompt(prompt)
        print(f"\n✅ Validation Score: {validation['score']}/100")
        if validation['issues']:
            print("⚠️ Issues found:")
            for issue in validation['issues']:
                print(f"  - {issue}")
    
    # Output prompt
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"\n💾 Prompt saved to: {args.output}")
    else:
        print("\n📄 Generated Prompt:")
        print("=" * 60)
        print(prompt)
    
    print(f"\n🎉 Prompt generated successfully! ({len(prompt)} characters)")
    print("📋 Copy the prompt above and paste it into your chosen AI development tool")
    if hasattr(task_context, 'target_tool'):
        print(f"🛠️ Target Tool: {task_context.target_tool.value.title()}")
        print(f"📋 Stage: {task_context.stage.value.replace('_', ' ').title()}")

if __name__ == "__main__":
    main()
