#!/usr/bin/env python3
"""
CLI for Lovable.dev Prompt Generator
Usage: python generate_prompt.py --tool lovable --task "build login page" --project "Task Manager App"
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.generators.build_prompt import LovablePromptGenerator, TaskContext, ProjectInfo

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate optimized Lovable.dev prompts using RAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_prompt.py --tool lovable --task "build login page" --project "Task Manager App"
  python generate_prompt.py --tool lovable --task "responsive dashboard" --project "Analytics Platform" --tech "React,Next.js,Tailwind"
  python generate_prompt.py --interactive
        """
    )
    
    parser.add_argument(
        '--tool',
        default='lovable',
        help='Tool to generate prompts for (default: lovable)'
    )
    
    parser.add_argument(
        '--task',
        help='Task description (e.g., "build login page")'
    )
    
    parser.add_argument(
        '--project',
        help='Project name'
    )
    
    parser.add_argument(
        '--description',
        help='Project description'
    )
    
    parser.add_argument(
        '--tech',
        help='Technology stack (comma-separated)'
    )
    
    parser.add_argument(
        '--requirements',
        help='Technical requirements (comma-separated)'
    )
    
    parser.add_argument(
        '--ui-requirements',
        help='UI/UX requirements (comma-separated)'
    )
    
    parser.add_argument(
        '--constraints',
        help='Project constraints (comma-separated)'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate the generated prompt'
    )
    
    parser.add_argument(
        '--suggestions',
        action='store_true',
        help='Get task suggestions for project type'
    )
    
    return parser.parse_args()

def interactive_mode():
    """Run the generator in interactive mode"""
    print("🚀 Lovable.dev Prompt Generator - Interactive Mode")
    print("=" * 50)
    
    # Get project information
    project_name = input("Project Name: ").strip()
    project_description = input("Project Description: ").strip()
    
    # Get technology stack
    tech_input = input("Technology Stack (comma-separated, e.g., React,Next.js,Tailwind): ").strip()
    tech_stack = [tech.strip() for tech in tech_input.split(',') if tech.strip()]
    
    target_audience = input("Target Audience (optional): ").strip() or "General users"
    
    # Get task information
    print("\n📋 Task Information")
    print("-" * 20)
    task_type = input("Task Type (e.g., build login page, create dashboard): ").strip()
    task_description = input("Task Description: ").strip()
    
    # Get requirements
    tech_reqs_input = input("Technical Requirements (comma-separated): ").strip()
    tech_requirements = [req.strip() for req in tech_reqs_input.split(',') if req.strip()]
    
    ui_reqs_input = input("UI/UX Requirements (comma-separated): ").strip()
    ui_requirements = [req.strip() for req in ui_reqs_input.split(',') if req.strip()]
    
    constraints_input = input("Constraints (comma-separated): ").strip()
    constraints = [constraint.strip() for constraint in constraints_input.split(',') if constraint.strip()]
    
    return {
        'project_name': project_name,
        'project_description': project_description,
        'tech_stack': tech_stack,
        'target_audience': target_audience,
        'task_type': task_type,
        'task_description': task_description,
        'tech_requirements': tech_requirements,
        'ui_requirements': ui_requirements,
        'constraints': constraints
    }

def get_task_suggestions(generator, project_type):
    """Get and display task suggestions"""
    suggestions = generator.get_task_suggestions(project_type)
    
    print(f"\n💡 Task Suggestions for {project_type}:")
    print("-" * 40)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
    
    return suggestions

def main():
    """Main CLI function"""
    args = parse_arguments()
    
    # Initialize generator
    try:
        generator = LovablePromptGenerator()
        print("✅ Prompt generator initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize generator: {e}")
        sys.exit(1)
    
    # Handle suggestions mode
    if args.suggestions:
        project_type = input("Enter project type (web_app, mobile_app, ecommerce, blog): ").strip()
        get_task_suggestions(generator, project_type)
        return
    
    # Get input data
    if args.interactive:
        data = interactive_mode()
    else:
        if not args.task or not args.project:
            print("❌ Error: --task and --project are required (or use --interactive)")
            sys.exit(1)
        
        data = {
            'project_name': args.project,
            'project_description': args.description or f"A modern web application: {args.project}",
            'tech_stack': args.tech.split(',') if args.tech else ['React', 'Next.js', 'Tailwind CSS'],
            'target_audience': 'General users',
            'task_type': args.task,
            'task_description': args.task,
            'tech_requirements': args.requirements.split(',') if args.requirements else [],
            'ui_requirements': args.ui_requirements.split(',') if args.ui_requirements else [],
            'constraints': args.constraints.split(',') if args.constraints else []
        }
    
    # Create context objects
    task_context = TaskContext(
        task_type=data['task_type'],
        project_name=data['project_name'],
        description=data['task_description'],
        technical_requirements=data['tech_requirements'],
        ui_requirements=data['ui_requirements'],
        constraints=data['constraints']
    )
    
    project_info = ProjectInfo(
        name=data['project_name'],
        description=data['project_description'],
        tech_stack=data['tech_stack'],
        target_audience=data['target_audience'],
        requirements=[]
    )
    
    # Generate prompt
    print("\n⚡ Generating prompt...")
    try:
        prompt = generator.generate_prompt(task_context, project_info)
        
        # Validate if requested
        if args.validate:
            print("\n🔍 Validating prompt...")
            validation = generator.validate_prompt(prompt)
            
            print(f"Validation Score: {validation['score']}/100")
            print(f"Valid: {'✅' if validation['is_valid'] else '❌'}")
            
            if validation['issues']:
                print("Issues found:")
                for issue in validation['issues']:
                    print(f"  - {issue}")
            
            if validation['suggestions']:
                print("Suggestions:")
                for suggestion in validation['suggestions']:
                    print(f"  - {suggestion}")
            print()
        
        # Output prompt
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(prompt)
            print(f"✅ Prompt saved to {args.output}")
        else:
            print("\n" + "=" * 80)
            print("GENERATED LOVABLE.DEV PROMPT")
            print("=" * 80)
            print(prompt)
            print("=" * 80)
            
    except Exception as e:
        print(f"❌ Failed to generate prompt: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
