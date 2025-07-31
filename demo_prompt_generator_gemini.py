"""
Simple Lovable.dev Prompt Generator Demo with Google Gemini
Description: Standalone demo that works with existing Gemini setup and chroma_gemini database
"""

import os
import sys
from dataclasses import dataclass
from typing import List, Dict, Any

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

class SimpleLovablePromptGeneratorGemini:
    """Simple prompt generator that works with existing Gemini setup"""
    
    def __init__(self):
        self.examples = {
            "authentication": {
                "context": "Secure user authentication with modern best practices",
                "guidelines": [
                    "Use NextAuth.js for authentication flow",
                    "Implement proper session management",
                    "Add password strength validation",
                    "Include social login options",
                    "Ensure secure token handling"
                ]
            },
            "dashboard": {
                "context": "Interactive dashboard with data visualization",
                "guidelines": [
                    "Use responsive grid layout",
                    "Implement real-time data updates",
                    "Add interactive charts and graphs",
                    "Include filtering and search",
                    "Optimize for mobile viewing"
                ]
            },
            "ecommerce": {
                "context": "E-commerce platform with modern UX",
                "guidelines": [
                    "Implement product catalog with search",
                    "Add shopping cart functionality",
                    "Include secure payment processing",
                    "Optimize for conversion",
                    "Mobile-first responsive design"
                ]
            }
        }
    
    def generate_prompt(self, task_context: TaskContext, project_info: ProjectInfo) -> str:
        """Generate a Lovable.dev prompt based on task context and project info"""
        
        # Get relevant guidelines
        guidelines = self._get_relevant_guidelines(task_context.task_type)
        
        # Generate structured prompt
        tech_stack = ', '.join(project_info.tech_stack)
        tech_reqs = '\n'.join(f"- {req}" for req in task_context.technical_requirements)
        ui_reqs = '\n'.join(f"- {req}" for req in task_context.ui_requirements)
        constraints = '\n'.join(f"- {constraint}" for constraint in task_context.constraints)
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

## 📝 Implementation Notes
Please implement this step by step:

1. **Setup & Structure**: Initialize project with proper folder structure
2. **Core Components**: Build main UI components with TypeScript
3. **Functionality**: Implement core business logic
4. **Styling**: Apply responsive design with Tailwind CSS
5. **Testing**: Add proper error handling and validation
6. **Optimization**: Performance and accessibility improvements

Focus on clean, production-ready code that follows modern web development best practices."""

        return prompt
    
    def _get_relevant_guidelines(self, task_type: str) -> List[str]:
        """Get relevant guidelines based on task type"""
        task_lower = task_type.lower()
        
        # Find matching example
        for key, example in self.examples.items():
            if key in task_lower:
                return example["guidelines"]
        
        # Default guidelines
        return [
            "Follow modern web development best practices",
            "Ensure responsive design for all devices",
            "Implement proper error handling",
            "Use TypeScript for type safety",
            "Optimize for performance and accessibility"
        ]
    
    def validate_prompt(self, prompt: str) -> Dict[str, Any]:
        """Validate the generated prompt for completeness"""
        validation_results = {
            'is_valid': True,
            'score': 0,
            'issues': [],
            'suggestions': []
        }
        
        # Check for key components
        required_sections = ['overview', 'description', 'requirements', 'technical', 'ui', 'deliverables']
        score = 0
        
        for section in required_sections:
            if section.lower() in prompt.lower():
                score += 15
            else:
                validation_results['issues'].append(f"Missing {section} section")
        
        # Check for specific elements
        if 'technology stack' in prompt.lower():
            score += 10
        if 'success criteria' in prompt.lower():
            score += 10
        if 'implementation' in prompt.lower():
            score += 10
        
        # Check prompt length
        if len(prompt) < 300:
            validation_results['issues'].append("Prompt is too short")
        elif len(prompt) > 3000:
            validation_results['issues'].append("Prompt might be too long")
        else:
            score += 10
        
        # Check for specificity
        specific_words = ['typescript', 'responsive', 'accessibility', 'performance', 'component']
        specific_count = sum(1 for word in specific_words if word in prompt.lower())
        score += min(specific_count * 2, 10)
        
        validation_results['score'] = min(100, score)
        validation_results['is_valid'] = validation_results['score'] >= 80
        
        if not validation_results['is_valid']:
            validation_results['suggestions'] = [
                "Add more technical specifications",
                "Include UI/UX requirements",
                "Define clear success criteria",
                "Add implementation guidelines"
            ]
        
        return validation_results

def run_demo():
    """Run the demonstration"""
    print("🚀 Lovable.dev Prompt Generator Demo with Google Gemini")
    print("=" * 65)
    print("Generating sample prompts for different project types...")
    print()
    
    generator = SimpleLovablePromptGeneratorGemini()
    
    # Demo scenarios
    scenarios = [
        {
            "name": "E-commerce Product Page",
            "task_context": TaskContext(
                task_type="build ecommerce product showcase",
                project_name="StyleHub Store",
                description="Modern e-commerce product page with interactive features",
                technical_requirements=[
                    "Next.js 14 with App Router",
                    "TypeScript for type safety", 
                    "Zustand for cart state management",
                    "Stripe payment integration",
                    "Image optimization with Next/Image"
                ],
                ui_requirements=[
                    "Product image gallery with zoom",
                    "Size and color variant selection",
                    "Add to cart with animations",
                    "Related products section",
                    "Mobile-optimized checkout flow"
                ],
                constraints=[
                    "Page load time under 2 seconds",
                    "Mobile-first responsive design",
                    "SEO optimized for product pages",
                    "WCAG 2.1 accessibility compliance"
                ]
            ),
            "project_info": ProjectInfo(
                name="StyleHub Store",
                description="A premium fashion e-commerce platform targeting style-conscious millennials",
                tech_stack=["Next.js 14", "TypeScript", "Tailwind CSS", "Stripe", "Vercel"],
                target_audience="Fashion-conscious millennials aged 25-35",
                requirements=[]
            )
        },
        {
            "name": "Task Management Authentication",
            "task_context": TaskContext(
                task_type="implement secure authentication system",
                project_name="TaskFlow Pro",
                description="Secure authentication system for a professional task management platform",
                technical_requirements=[
                    "NextAuth.js with multiple providers",
                    "JWT token management",
                    "Role-based access control",
                    "Session persistence",
                    "Password strength validation"
                ],
                ui_requirements=[
                    "Clean login/signup forms",
                    "Social login buttons",
                    "Password strength indicator",
                    "Remember me functionality",
                    "Forgot password flow"
                ],
                constraints=[
                    "GDPR compliance for user data",
                    "Multi-factor authentication support",
                    "Secure session management",
                    "Rate limiting for login attempts"
                ]
            ),
            "project_info": ProjectInfo(
                name="TaskFlow Pro",
                description="Professional task management platform for teams and organizations",
                tech_stack=["Next.js", "NextAuth.js", "Prisma", "PostgreSQL", "TypeScript"],
                target_audience="Business professionals and project managers",
                requirements=[]
            )
        }
    ]
    
    # Generate prompts for each scenario
    for i, scenario in enumerate(scenarios, 1):
        print(f"📋 Scenario {i}: {scenario['name']}")
        print("-" * 50)
        
        # Generate prompt
        prompt = generator.generate_prompt(
            scenario["task_context"], 
            scenario["project_info"]
        )
        
        # Validate prompt
        validation = generator.validate_prompt(prompt)
        
        print(f"✅ Generated prompt ({len(prompt)} characters)")
        print(f"🎯 Quality Score: {validation['score']}/100")
        print(f"📊 Status: {'Valid' if validation['is_valid'] else 'Needs Review'}")
        
        if validation['issues']:
            print(f"⚠️  Issues: {', '.join(validation['issues'])}")
        
        print("\n📄 Generated Prompt:")
        print("─" * 50)
        print(prompt)
        print("\n" + "=" * 65 + "\n")
    
    print("🎉 Demo completed! Both prompts are optimized for Lovable.dev")
    print("\n💡 Tips:")
    print("- Copy any prompt above and paste it into Lovable.dev")
    print("- Modify the requirements to match your specific needs")
    print("- Use the Streamlit interface for interactive generation")
    print(f"- Run: streamlit run streamlit_app_gemini.py")

if __name__ == "__main__":
    run_demo()
