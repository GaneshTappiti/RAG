"""
Lovable.dev Prompt Generator with Google Gemini
Author: Enhanced RAG System
Description: Generates optimized Lovable.dev prompts using RAG retrieval with Google Gemini embeddings
"""

import os
import yaml
import json
from typing import Dict, List, Optional, Any
from src.core.shared_types import TaskContext, ProjectInfo
from jinja2 import Template, Environment, FileSystemLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LovablePromptGeneratorGemini:
    """Main prompt generator for Lovable.dev using Google Gemini"""
    
    def __init__(self, config_path: str = "lovable.yaml", chroma_path: str = "chroma_lovable_gemini"):
        self.config_path = config_path
        self.chroma_path = chroma_path
        self.tool_profile = self._load_tool_profile()
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_store = None
        self.template_env = Environment(
            loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Initialize vector store
        self._initialize_vector_store()
    
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
    
    def _initialize_vector_store(self):
        """Initialize or load the vector store"""
        if os.path.exists(self.chroma_path):
            print("Loading existing Gemini vector store...")
            self.vector_store = Chroma(
                persist_directory=self.chroma_path,
                embedding_function=self.embeddings
            )
        else:
            print("Creating new Gemini vector store...")
            self._create_vector_store()
    
    def _create_vector_store(self):
        """Create vector store from Lovable docs using Gemini embeddings"""
        docs_path = "data/lovable_docs"
        
        if not os.path.exists(docs_path):
            print(f"Warning: {docs_path} not found. Vector store will be empty.")
            self.vector_store = Chroma(
                persist_directory=self.chroma_path,
                embedding_function=self.embeddings
            )
            return
        
        # Load documents
        loader = DirectoryLoader(docs_path, glob="*.md")
        documents = loader.load()
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        
        # Add metadata for better retrieval
        for chunk in chunks:
            # Extract category from filename or content
            filename = os.path.basename(chunk.metadata.get('source', ''))
            if 'prompting' in filename:
                chunk.metadata['category'] = 'prompting'
            elif 'ui_design' in filename:
                chunk.metadata['category'] = 'ui_design'
            elif 'api_integration' in filename:
                chunk.metadata['category'] = 'integration'
            elif 'debugging' in filename:
                chunk.metadata['category'] = 'debugging'
            else:
                chunk.metadata['category'] = 'general'
        
        # Create vector store with Gemini embeddings
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.chroma_path
        )
        
        print(f"Created Gemini vector store with {len(chunks)} document chunks")
    
    def get_relevant_context(self, task_type: str, query: str, category: Optional[str] = None) -> List[Document]:
        """Retrieve relevant context for the task"""
        if not self.vector_store:
            return []
        
        # Construct search query
        search_query = f"{task_type} {query}"
        
        # Get relevant documents
        if category:
            # Filter by category if specified
            results = self.vector_store.similarity_search(
                search_query,
                k=5,
                filter={"category": category}
            )
        else:
            results = self.vector_store.similarity_search(search_query, k=5)
        
        return results
    
    def generate_prompt(self, 
                       task_context: TaskContext, 
                       project_info: ProjectInfo) -> str:
        """Generate a Lovable.dev prompt based on task context and project info"""
        
        # Get relevant context from vector store
        context_docs = self.get_relevant_context(
            task_context.task_type,
            f"{task_context.description} {' '.join(task_context.technical_requirements)}"
        )
        
        # Extract guidelines from context
        guidelines = self._extract_guidelines(context_docs)
        
        # Get relevant few-shot examples
        relevant_examples = self._get_relevant_examples(task_context.task_type)
        
        # Load and render template
        template_data = {
            'tool_profile': self.tool_profile,
            'task_context': task_context,
            'project_info': project_info,
            'guidelines': guidelines,
            'examples': relevant_examples,
            'context_snippets': [doc.page_content[:200] + "..." for doc in context_docs[:3]]
        }
        
        try:
            template = self.template_env.get_template('lovable_task_template.md')
            return template.render(**template_data)
        except Exception as e:
            print(f"Template rendering failed: {e}")
            return self._generate_fallback_prompt(task_context, project_info)
    
    def _extract_guidelines(self, context_docs: List[Document]) -> str:
        """Extract and summarize guidelines from context documents"""
        if not context_docs:
            return "Follow Lovable.dev best practices for clean, modern web development."
        
        guidelines = []
        for doc in context_docs:
            content = doc.page_content
            # Extract key points (simple heuristic)
            lines = content.split('\n')
            for line in lines:
                if any(keyword in line.lower() for keyword in ['best practice', 'should', 'use', 'avoid', 'ensure']):
                    guidelines.append(line.strip())
        
        return '\n'.join(guidelines[:10])  # Limit to top 10 guidelines
    
    def _get_relevant_examples(self, task_type: str) -> List[Dict[str, str]]:
        """Get relevant few-shot examples for the task type"""
        examples = self.tool_profile.get('few_shot_examples', [])
        
        # Filter examples based on task type keywords
        task_keywords = task_type.lower().split()
        relevant_examples = []
        
        for example in examples:
            input_text = example.get('input', '').lower()
            if any(keyword in input_text for keyword in task_keywords):
                relevant_examples.append(example)
        
        # If no specific matches, return first few examples
        if not relevant_examples:
            relevant_examples = examples[:2]
        
        return relevant_examples
    
    def _generate_fallback_prompt(self, task_context: TaskContext, project_info: ProjectInfo) -> str:
        """Generate a basic prompt if template rendering fails"""
        tech_stack = ', '.join(project_info.tech_stack)
        tech_reqs = '\n'.join(f"- {req}" for req in task_context.technical_requirements)
        ui_reqs = '\n'.join(f"- {req}" for req in task_context.ui_requirements)
        constraints = '\n'.join(f"- {constraint}" for constraint in task_context.constraints)
        
        return f"""# {task_context.task_type.title()} for {project_info.name}

## Project Context
{project_info.description}

**Technology Stack:** {tech_stack}

## Task Description
{task_context.description}

## Requirements
### Technical Requirements
{tech_reqs}

### UI Requirements
{ui_reqs}

## Constraints
{constraints}

## Expected Output
Create a modern, responsive web application following Lovable.dev best practices.
Ensure clean code, proper error handling, and excellent user experience.
"""
    
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
    
    def validate_prompt(self, prompt: str) -> Dict[str, Any]:
        """Validate the generated prompt for completeness"""
        validation_results = {
            'is_valid': True,
            'score': 0,
            'issues': [],
            'suggestions': []
        }
        
        # Check for key components
        required_sections = ['context', 'requirements', 'technical', 'ui']
        score = 0
        
        for section in required_sections:
            if section.lower() in prompt.lower():
                score += 25
            else:
                validation_results['issues'].append(f"Missing {section} section")
        
        # Check prompt length
        if len(prompt) < 200:
            validation_results['issues'].append("Prompt is too short")
            score -= 10
        elif len(prompt) > 2000:
            validation_results['issues'].append("Prompt might be too long")
            score -= 5
        
        # Check for specificity
        vague_words = ['nice', 'good', 'better', 'improve', 'enhance']
        vague_count = sum(1 for word in vague_words if word in prompt.lower())
        if vague_count > 3:
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


def main():
    """Example usage of the Gemini prompt generator"""
    print("🚀 Lovable.dev Prompt Generator with Google Gemini")
    print("=" * 60)
    
    generator = LovablePromptGeneratorGemini()
    
    # Example task context
    task_context = TaskContext(
        task_type="build responsive dashboard",
        project_name="Analytics Pro",
        description="Create a modern analytics dashboard with real-time data visualization",
        technical_requirements=[
            "React Query for data fetching",
            "Chart.js for visualizations", 
            "WebSocket for real-time updates",
            "TypeScript for type safety"
        ],
        ui_requirements=[
            "Mobile-first responsive design",
            "Dark mode support",
            "Interactive charts and graphs",
            "Loading states and error handling"
        ],
        constraints=[
            "Performance under 2 seconds load time",
            "Accessibility WCAG 2.1 compliant",
            "Cross-browser compatibility",
            "SEO optimized"
        ]
    )
    
    # Example project info
    project_info = ProjectInfo(
        name="Analytics Pro",
        description="A comprehensive analytics platform for business intelligence",
        tech_stack=["Next.js 14", "React", "TypeScript", "Tailwind CSS", "Chart.js"],
        target_audience="Business analysts and data scientists",
        requirements=[]
    )
    
    # Generate prompt
    prompt = generator.generate_prompt(task_context, project_info)
    print("Generated Prompt:")
    print("=" * 60)
    print(prompt)
    
    # Validate prompt
    validation = generator.validate_prompt(prompt)
    print("\nValidation Results:")
    print("=" * 60)
    print(f"Valid: {validation['is_valid']}")
    print(f"Score: {validation['score']}/100")
    if validation['issues']:
        print("Issues:", ", ".join(validation['issues']))


if __name__ == "__main__":
    main()
