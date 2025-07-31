#!/usr/bin/env python3
"""
Demo script for Lovable.dev Prompt Generator without requiring API keys
Usage: python demo_prompt_generator.py
"""

import os
import yaml
from typing import Dict, List, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TaskContext:
    """Context for a specific task type"""
    task_type: str
    project_name: str
    description: str
    technical_requirements: List[str]
    ui_requirements: List[str]
    constraints: List[str]

@dataclass
class ProjectInfo:
    """Project information structure"""
    name: str
    description: str
    tech_stack: List[str]
    target_audience: str
    requirements: List[str]

class SimpleLovablePromptGenerator:
    """Simplified prompt generator for demo purposes"""
    
    def __init__(self, config_path: str = "lovable.yaml"):
        self.config_path = config_path
        self.tool_profile = self._load_tool_profile()
    
    def _load_tool_profile(self) -> Dict[str, Any]:
        """Load the Lovable.dev tool profile configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Warning: {self.config_path} not found. Using default configuration.")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration if yaml file is not found"""
        return {
            'tool_name': 'Lovable.dev',
            'format': 'markdown',
            'tone': 'official yet casual',
            'preferred_use_cases': [
                'project kickoff',
                'UI scaffolding',
                'responsiveness',
                'API integrations'
            ],
            'few_shot_examples': [
                {
                    'input': 'Start a task management app',
                    'output': 'Build a Next.js + Tailwind app with task CRUD, due dates, and a dashboard.'
                }
            ]
        }
    
    def get_mock_guidelines(self, task_type: str) -> str:
        """Get mock guidelines based on task type"""
        guidelines_map = {
            'login': "Follow authentication best practices, use secure session management, implement proper validation.",
            'dashboard': "Create responsive layouts, use component-based architecture, ensure data visualization is clear.",
            'api': "Implement proper error handling, use authentication tokens, follow REST principles.",
            'ui': "Follow modern design patterns, ensure accessibility, use responsive design principles.",
            'default': "Follow Lovable.dev best practices for clean, modern web development."
        }
        
        for key in guidelines_map:
            if key in task_type.lower():
                return guidelines_map[key]
        
        return guidelines_map['default']
    
    def get_relevant_examples(self, task_type: str) -> List[Dict[str, str]]:
        """Get relevant examples based on task type"""
        all_examples = self.tool_profile.get('few_shot_examples', [])
        
        # Add more examples based on task type
        additional_examples = {
            'login': {
                'input': 'Create user authentication',
                'output': 'Implement NextAuth.js with Google/GitHub providers, add login/logout components with error handling.'
            },
            'dashboard': {
                'input': 'Build analytics dashboard',
                'output': 'Create responsive dashboard with charts, real-time data, and filtering capabilities using React and Chart.js.'
            },
            'api': {
                'input': 'Add API integration',
                'output': 'Set up Axios client with interceptors, implement error handling, and add loading states for all API calls.'
            }
        }
        
        # Find relevant examples
        relevant_examples = all_examples.copy()
        for key, example in additional_examples.items():
            if key in task_type.lower():
                relevant_examples.append(example)
        
        return relevant_examples[:3]  # Limit to 3 examples
    
    def generate_prompt(self, task_context: TaskContext, project_info: ProjectInfo) -> str:
        """Generate a Lovable.dev prompt"""
        
        # Get guidelines and examples
        guidelines = self.get_mock_guidelines(task_context.task_type)
        examples = self.get_relevant_examples(task_context.task_type)
        
        # Generate the prompt
        prompt = self._build_prompt(task_context, project_info, guidelines, examples)
        
        return prompt
    
    def _build_prompt(self, task_context: TaskContext, project_info: ProjectInfo, 
                     guidelines: str, examples: List[Dict[str, str]]) -> str:
        """Build the formatted prompt"""
        
        tech_stack = ', '.join(project_info.tech_stack)
        tech_reqs = '\n'.join(f"- {req}" for req in task_context.technical_requirements)
        ui_reqs = '\n'.join(f"- {req}" for req in task_context.ui_requirements)
        constraints = '\n'.join(f"- {constraint}" for constraint in task_context.constraints)
        
        examples_text = ""
        for i, example in enumerate(examples, 1):
            examples_text += f"\n**Example {i}:**\n"
            examples_text += f"Input: {example['input']}\n"
            examples_text += f"Output: {example['output']}\n"
        
        prompt = f"""# {task_context.task_type.title()} - {project_info.name}

You are a skilled AI development assistant on **{self.tool_profile['tool_name']}**.

**Tone:** {self.tool_profile['tone']}
**Output Format:** {self.tool_profile['format']}

## Project Overview
**Name:** {project_info.name}
**Description:** {project_info.description}
**Technology Stack:** {tech_stack}
**Target Audience:** {project_info.target_audience}

## Task Details
**Type:** {task_context.task_type}
**Description:** {task_context.description}

### Technical Requirements
{tech_reqs}

### UI/UX Requirements
{ui_reqs}

### Constraints
{constraints}

## Guidelines Summary
{guidelines}

## Expected Output
Provide a clear, formatted Lovable prompt that:
- Defines the context and scope clearly
- Gives specific, actionable requirements
- Includes responsive design considerations
- Follows accessibility best practices
- Avoids vague language and ensures structure is clean
- Includes proper error handling and loading states

## Examples for Reference
{examples_text}

**Remember:** Follow {self.tool_profile['tool_name']}'s best practices for modern web development. Be specific, actionable, and comprehensive in your response.
"""
        
        return prompt
    
    def validate_prompt(self, prompt: str) -> Dict[str, Any]:
        """Validate the generated prompt"""
        validation_results = {
            'is_valid': True,
            'score': 0,
            'issues': [],
            'suggestions': []
        }
        
        # Check for key components
        required_sections = ['project overview', 'task details', 'requirements', 'expected output']
        score = 0
        
        for section in required_sections:
            if section.lower() in prompt.lower():
                score += 25
            else:
                validation_results['issues'].append(f"Missing {section} section")
        
        # Check prompt length
        if len(prompt) < 300:
            validation_results['issues'].append("Prompt is too short")
            score -= 10
        elif len(prompt) > 3000:
            validation_results['issues'].append("Prompt might be too long")
            score -= 5
        
        # Check for specificity
        specific_terms = ['specific', 'implement', 'create', 'build', 'use', 'follow']
        specific_count = sum(1 for term in specific_terms if term in prompt.lower())
        if specific_count >= 3:
            score += 10
        
        # Check for vague language
        vague_words = ['nice', 'good', 'better', 'improve', 'enhance']
        vague_count = sum(1 for word in vague_words if word in prompt.lower())
        if vague_count > 2:
            validation_results['issues'].append("Prompt contains vague language")
            score -= 10
        
        validation_results['score'] = max(0, min(100, score))
        validation_results['is_valid'] = validation_results['score'] >= 60
        
        if not validation_results['is_valid']:
            validation_results['suggestions'] = [
                "Be more specific about requirements",
                "Include technical stack details",
                "Add UI/UX specifications",
                "Define success criteria"
            ]
        
        return validation_results
    
    def get_task_suggestions(self, project_type: str) -> List[str]:
        """Get suggested task types based on project type"""
        suggestions = {
            'web_app': [
                'project kickoff',
                'authentication setup',
                'dashboard creation',
                'responsive design',
                'API integration'
            ],
            'mobile_app': [
                'mobile-first design',
                'touch interactions',
                'offline functionality',
                'push notifications'
            ],
            'ecommerce': [
                'product catalog',
                'shopping cart',
                'payment integration',
                'order management'
            ],
            'blog': [
                'content management',
                'blog layout',
                'SEO optimization',
                'commenting system'
            ]
        }
        
        return suggestions.get(project_type, suggestions['web_app'])

def main():
    """Demo the prompt generator"""
    print("🚀 Lovable.dev Prompt Generator Demo")
    print("=" * 50)
    
    # Initialize generator
    generator = SimpleLovablePromptGenerator()
    
    # Demo 1: Task Management App Login
    print("\n📋 Demo 1: Task Management App - User Authentication")
    print("-" * 50)
    
    task_context = TaskContext(
        task_type="user authentication setup",
        project_name="TaskFlow Pro",
        description="Create a secure authentication system with multiple login options",
        technical_requirements=[
            "NextAuth.js integration",
            "OAuth providers (Google, GitHub)",
            "JWT token management",
            "Session persistence",
            "Password reset functionality"
        ],
        ui_requirements=[
            "Clean login/signup forms",
            "Loading states for auth actions",
            "Error message display",
            "Mobile responsive design",
            "Dark mode support"
        ],
        constraints=[
            "Use TypeScript for type safety",
            "Follow OWASP security guidelines",
            "Implement rate limiting",
            "Ensure GDPR compliance"
        ]
    )
    
    project_info = ProjectInfo(
        name="TaskFlow Pro",
        description="A modern task management application for professional teams",
        tech_stack=["Next.js 14", "React", "TypeScript", "Tailwind CSS", "NextAuth.js"],
        target_audience="Professional teams and project managers",
        requirements=[]
    )
    
    prompt = generator.generate_prompt(task_context, project_info)
    print(prompt)
    
    # Validate the prompt
    validation = generator.validate_prompt(prompt)
    print(f"\n🔍 Validation Score: {validation['score']}/100")
    print(f"✅ Valid: {validation['is_valid']}")
    if validation['issues']:
        print("Issues:", ", ".join(validation['issues']))
    
    # Demo 2: E-commerce Product Page
    print("\n\n🛍️ Demo 2: E-commerce - Product Page")
    print("-" * 50)
    
    task_context2 = TaskContext(
        task_type="product page development",
        project_name="StyleHub Store",
        description="Build a modern product page with image gallery and purchase options",
        technical_requirements=[
            "Image zoom functionality",
            "Product variant selection",
            "Add to cart API integration",
            "Stock level checking",
            "Reviews and ratings system"
        ],
        ui_requirements=[
            "Image carousel with thumbnails",
            "Responsive product grid",
            "Clear pricing display",
            "Mobile-optimized checkout flow",
            "Accessibility compliance"
        ],
        constraints=[
            "Page load time under 3 seconds",
            "SEO optimized structure",
            "Analytics tracking",
            "Cross-browser compatibility"
        ]
    )
    
    project_info2 = ProjectInfo(
        name="StyleHub Store",
        description="Modern fashion e-commerce platform",
        tech_stack=["Next.js", "React", "Tailwind CSS", "Stripe", "Prisma"],
        target_audience="Fashion-conscious consumers",
        requirements=[]
    )
    
    prompt2 = generator.generate_prompt(task_context2, project_info2)
    print(prompt2)
    
    validation2 = generator.validate_prompt(prompt2)
    print(f"\n🔍 Validation Score: {validation2['score']}/100")
    print(f"✅ Valid: {validation2['is_valid']}")
    
    # Show task suggestions
    print("\n\n💡 Task Suggestions for Web Apps:")
    print("-" * 50)
    suggestions = generator.get_task_suggestions('web_app')
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
    
    print("\n🎉 Demo complete! This demonstrates the Lovable.dev prompt generator.")
    print("💡 To use with full RAG capabilities, set up your OpenAI API key in .env file.")

if __name__ == "__main__":
    main()
