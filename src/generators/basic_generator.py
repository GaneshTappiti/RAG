"""
Enhanced Multi-Tool RAG Prompt Generator
Author: Enhanced RAG System  
Description: Multi-stage prompt generator supporting various AI development tools with RAG retrieval
"""

import os
import yaml
import json
from typing import Dict, List, Optional, Any, Tuple
from src.core.types import (
    TaskContext, ProjectInfo, ToolProfile, PromptResult,
    PromptStage, SupportedTool, AppStructure, PageSpec, FlowConnection
)
from jinja2 import Template, Environment, FileSystemLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class MultiToolPromptGenerator:
    """Enhanced prompt generator supporting multiple AI development tools with stage-based generation"""
    
    def __init__(self, base_chroma_path: str = "chroma_multi_tool"):
        self.base_chroma_path = base_chroma_path
        self.tool_profiles: Dict[SupportedTool, ToolProfile] = {}
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_stores: Dict[SupportedTool, Chroma] = {}
        self.template_env = Environment(
            loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Initialize all supported tools
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize all supported tools and their configurations"""
        for tool in SupportedTool:
            try:
                self.tool_profiles[tool] = self._load_tool_profile(tool)
                self._initialize_tool_vector_store(tool)
            except Exception as e:
                print(f"Warning: Could not initialize {tool.value}: {e}")
                # Continue with other tools
    
    def _load_tool_profile(self, tool: SupportedTool) -> ToolProfile:
        """Load tool-specific configuration"""
        config_file = f"{tool.value}.yaml"
        
        try:
            with open(config_file, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                
            return ToolProfile(
                tool_name=config.get('tool_name', tool.value.title()),
                format=config.get('format', 'markdown'),
                tone=config.get('tone', 'professional'),
                preferred_use_cases=config.get('preferred_use_cases', []),
                few_shot_examples=config.get('few_shot_examples', []),
                prompting_guidelines=config.get('prompting_guidelines', {}),
                categories=config.get('categories', []),
                stage_templates=self._get_stage_templates(tool),
                vector_namespace=f"{tool.value}_docs"
            )
        except FileNotFoundError:
            print(f"Config file {config_file} not found, using defaults for {tool.value}")
            return self._get_default_tool_profile(tool)
    
    def _get_stage_templates(self, tool: SupportedTool) -> Dict[PromptStage, str]:
        """Get stage-specific template mappings"""
        return {
            PromptStage.APP_SKELETON: "stage_app_skeleton.md",
            PromptStage.PAGE_UI: "stage_page_ui.md", 
            PromptStage.FLOW_CONNECTIONS: "stage_flow_connections.md",
            PromptStage.FEATURE_SPECIFIC: "stage_feature_specific.md",
            PromptStage.DEBUGGING: "stage_debugging.md",
            PromptStage.OPTIMIZATION: "stage_optimization.md"
        }
    
    def _get_default_tool_profile(self, tool: SupportedTool) -> ToolProfile:
        """Return default configuration for a tool"""
        return ToolProfile(
            tool_name=tool.value.title(),
            format="markdown",
            tone="professional and helpful",
            preferred_use_cases=["app development", "ui design", "prototyping"],
            few_shot_examples=[],
            prompting_guidelines={
                "structure": ["Be clear and specific", "Include context", "Define requirements"],
                "best_practices": ["Use modern patterns", "Consider accessibility", "Optimize performance"],
                "avoid": ["Vague instructions", "Missing context", "Overly complex requests"]
            },
            categories=["development", "design", "prototype"],
            stage_templates=self._get_stage_templates(tool),
            vector_namespace=f"{tool.value}_docs"
        )
    
    def _initialize_tool_vector_store(self, tool: SupportedTool):
        """Initialize vector store for a specific tool"""
        tool_chroma_path = f"{self.base_chroma_path}_{tool.value}"
        
        if os.path.exists(tool_chroma_path):
            # Load existing vector store
            self.vector_stores[tool] = Chroma(
                persist_directory=tool_chroma_path,
                embedding_function=self.embeddings,
                collection_name=self.tool_profiles[tool].vector_namespace
            )
        else:
            # Create new vector store
            self._create_tool_vector_store(tool)
    
    def _create_tool_vector_store(self, tool: SupportedTool):
        """Create vector store for tool-specific documentation"""
        tool_docs_path = f"data/{tool.value}_docs"
        tool_chroma_path = f"{self.base_chroma_path}_{tool.value}"
        
        if not os.path.exists(tool_docs_path):
            print(f"Documentation directory {tool_docs_path} not found for {tool.value}")
            return
        
        try:
            # Load tool-specific documents
            loader = DirectoryLoader(tool_docs_path, glob="*.md")
            documents = loader.load()
            
            if not documents:
                print(f"No documents found in {tool_docs_path}")
                return
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100,
                length_function=len,
                add_start_index=True,
            )
            chunks = text_splitter.split_documents(documents)
            
            # Add tool and category metadata
            for chunk in chunks:
                chunk.metadata.update({
                    'tool': tool.value,
                    'namespace': self.tool_profiles[tool].vector_namespace
                })
            
            # Create vector store
            self.vector_stores[tool] = Chroma.from_documents(
                chunks,
                self.embeddings,
                persist_directory=tool_chroma_path,
                collection_name=self.tool_profiles[tool].vector_namespace
            )
            
            print(f"Created vector store for {tool.value} with {len(chunks)} chunks")
            
        except Exception as e:
            print(f"Error creating vector store for {tool.value}: {e}")
    
    def get_relevant_context(self, 
                           tool: SupportedTool, 
                           stage: PromptStage,
                           query: str, 
                           task_type: str = "") -> List[Document]:
        """Get relevant context from tool-specific vector store"""
        
        if tool not in self.vector_stores:
            print(f"Vector store not available for {tool.value}")
            return []
        
        # Enhance query with stage and task context
        enhanced_query = f"{stage.value} {task_type} {query}".strip()
        
        try:
            # Search tool-specific vector store
            results = self.vector_stores[tool].similarity_search_with_relevance_scores(
                enhanced_query, 
                k=5
            )
            
            # Filter by relevance threshold
            relevant_docs = [doc for doc, score in results if score > 0.6]
            
            return relevant_docs
            
        except Exception as e:
            print(f"Error retrieving context for {tool.value}: {e}")
            return []
    
    def generate_prompt(self, 
                       task_context: TaskContext, 
                       project_info: ProjectInfo,
                       stage: Optional[PromptStage] = None,
                       tool: Optional[SupportedTool] = None) -> PromptResult:
        """Generate optimized prompt for specific tool and stage"""
        
        # Use context values or defaults
        target_tool = tool or task_context.target_tool
        target_stage = stage or task_context.stage
        
        if target_tool not in self.tool_profiles:
            raise ValueError(f"Tool {target_tool.value} not supported")
        
        tool_profile = self.tool_profiles[target_tool]
        
        # Get relevant context from RAG
        context_query = f"{task_context.task_type} {task_context.description}"
        context_docs = self.get_relevant_context(
            target_tool, 
            target_stage,
            context_query, 
            task_context.task_type
        )
        
        # Select appropriate template
        template_name = tool_profile.stage_templates.get(target_stage, "lovable_task_template.md")
        
        try:
            template = self.template_env.get_template(template_name)
        except Exception as e:
            print(f"Template {template_name} not found, using fallback: {e}")
            return self._generate_fallback_prompt(task_context, project_info, target_tool, target_stage)
        
        # Prepare template context
        template_context = {
            'task_context': task_context,
            'project_info': project_info,
            'tool_profile': tool_profile,
            'context_docs': context_docs,
            'guidelines': self._extract_guidelines(context_docs),
            'examples': self._get_relevant_examples(tool_profile, task_context.task_type),
            'stage': target_stage,
            'page_spec': task_context.page_spec,
            'app_structure': task_context.app_structure,
            'flow_connections': task_context.flow_connections
        }
        
        # Generate prompt
        try:
            prompt = template.render(**template_context)
            
            # Calculate confidence score
            confidence = self._calculate_confidence_score(context_docs, task_context, tool_profile)
            
            # Determine next suggested stage
            next_stage = self._suggest_next_stage(target_stage, task_context)
            
            return PromptResult(
                prompt=prompt,
                stage=target_stage,
                tool=target_tool,
                confidence_score=confidence,
                sources=[doc.metadata.get('source', 'unknown') for doc in context_docs],
                next_suggested_stage=next_stage,
                regeneration_context={
                    'task_context': task_context.__dict__,
                    'project_info': project_info.__dict__,
                    'used_template': template_name,
                    'context_count': len(context_docs)
                }
            )
            
        except Exception as e:
            print(f"Error generating prompt: {e}")
            return self._generate_fallback_prompt(task_context, project_info, target_tool, target_stage)
    
    def _extract_guidelines(self, context_docs: List[Document]) -> str:
        """Extract and combine guidelines from context documents"""
        guidelines = []
        
        for doc in context_docs:
            content = doc.page_content.lower()
            if any(keyword in content for keyword in ['guideline', 'best practice', 'recommendation']):
                # Extract relevant sentences
                sentences = doc.page_content.split('.')
                for sentence in sentences:
                    if any(keyword in sentence.lower() for keyword in ['should', 'must', 'recommend', 'avoid']):
                        guidelines.append(sentence.strip())
        
        return '\n'.join(f"- {guideline}" for guideline in guidelines[:5] if guideline)
    
    def _get_relevant_examples(self, tool_profile: ToolProfile, task_type: str) -> List[Dict[str, str]]:
        """Get relevant examples from tool profile"""
        relevant_examples = []
        
        for example in tool_profile.few_shot_examples:
            if task_type.lower() in example.get('input', '').lower():
                relevant_examples.append(example)
        
        # If no specific examples found, return first few examples
        if not relevant_examples:
            relevant_examples = tool_profile.few_shot_examples[:2]
        
        return relevant_examples
    
    def _calculate_confidence_score(self, 
                                   context_docs: List[Document], 
                                   task_context: TaskContext, 
                                   tool_profile: ToolProfile) -> float:
        """Calculate confidence score for the generated prompt"""
        score = 0.5  # Base score
        
        # Context availability
        if context_docs:
            score += 0.2
            if len(context_docs) >= 3:
                score += 0.1
        
        # Tool-task alignment
        if task_context.task_type.lower() in [use_case.lower() for use_case in tool_profile.preferred_use_cases]:
            score += 0.2
        
        # Completeness of task context
        if task_context.technical_requirements:
            score += 0.1
        if task_context.ui_requirements:
            score += 0.1
        
        return min(1.0, score)
    
    def _suggest_next_stage(self, current_stage: PromptStage, task_context: TaskContext) -> Optional[PromptStage]:
        """Suggest the next logical stage in the development process"""
        stage_progression = {
            PromptStage.APP_SKELETON: PromptStage.PAGE_UI,
            PromptStage.PAGE_UI: PromptStage.FLOW_CONNECTIONS,
            PromptStage.FLOW_CONNECTIONS: PromptStage.FEATURE_SPECIFIC,
            PromptStage.FEATURE_SPECIFIC: PromptStage.OPTIMIZATION,
            PromptStage.DEBUGGING: PromptStage.OPTIMIZATION,
            PromptStage.OPTIMIZATION: None  # Final stage
        }
        
        return stage_progression.get(current_stage)
    
    def _generate_fallback_prompt(self, 
                                 task_context: TaskContext, 
                                 project_info: ProjectInfo,
                                 tool: SupportedTool,
                                 stage: PromptStage) -> PromptResult:
        """Generate a fallback prompt when templates or RAG fail"""
        
        tool_profile = self.tool_profiles.get(tool, self._get_default_tool_profile(tool))
        
        fallback_prompt = f"""# {task_context.task_type.title()} - {project_info.name}

**Tool:** {tool_profile.tool_name}
**Stage:** {stage.value.title().replace('_', ' ')}

## Project Overview
{project_info.description}

**Technology Stack:** {', '.join(project_info.tech_stack)}
**Target Audience:** {project_info.target_audience}

## Task Description
{task_context.description}

## Requirements

### Technical Requirements
{chr(10).join(f'- {req}' for req in task_context.technical_requirements)}

### UI/UX Requirements  
{chr(10).join(f'- {req}' for req in task_context.ui_requirements)}

### Constraints
{chr(10).join(f'- {constraint}' for constraint in task_context.constraints)}

## Implementation Guidelines

- Follow {tool_profile.tool_name} best practices
- Ensure responsive design for all devices
- Implement proper error handling and loading states
- Focus on user experience and accessibility
- Use modern development patterns

## Success Criteria

- Functional implementation that meets requirements
- Clean, maintainable code structure
- Responsive design across device sizes
- Accessible interface following WCAG guidelines
- Performance optimized for target users

---

Please implement this using {tool_profile.tool_name} following the {tool_profile.tone} approach with {tool_profile.format} output."""

        return PromptResult(
            prompt=fallback_prompt,
            stage=stage,
            tool=tool,
            confidence_score=0.4,  # Lower confidence for fallback
            sources=[],
            next_suggested_stage=self._suggest_next_stage(stage, task_context),
            regeneration_context={
                'fallback': True,
                'task_context': task_context.__dict__,
                'project_info': project_info.__dict__
            }
        )
    
    def get_supported_tools(self) -> List[SupportedTool]:
        """Get list of currently supported tools"""
        return list(self.tool_profiles.keys())
    
    def get_available_stages(self) -> List[PromptStage]:
        """Get list of available prompt stages"""
        return list(PromptStage)
    
    def validate_prompt_result(self, result: PromptResult) -> Dict[str, Any]:
        """Validate the generated prompt result"""
        issues = []
        score = 0
        
        # Check prompt length
        if 200 <= len(result.prompt) <= 4000:
            score += 25
        else:
            issues.append("Prompt length outside optimal range")
        
        # Check confidence score
        if result.confidence_score >= 0.7:
            score += 25
        elif result.confidence_score >= 0.5:
            score += 15
        else:
            issues.append("Low confidence score")
        
        # Check sources
        if result.sources:
            score += 20
        else:
            issues.append("No source references found")
        
        # Check stage progression
        if result.next_suggested_stage:
            score += 15
        
        # Check completeness
        required_sections = ['overview', 'requirements', 'implementation']
        found_sections = sum(1 for section in required_sections 
                           if section.lower() in result.prompt.lower())
        score += (found_sections / len(required_sections)) * 15
        
        return {
            'score': min(100, score),
            'is_valid': score >= 70,
            'issues': issues,
            'confidence': result.confidence_score,
            'has_sources': bool(result.sources),
            'next_stage_available': result.next_suggested_stage is not None
        }

def main():
    """Demo usage of the multi-tool prompt generator"""
    generator = MultiToolPromptGenerator()
    
    # Example task context
    task_context = TaskContext(
        task_type="build complete application",
        project_name="TaskMaster Pro",
        description="A comprehensive task management application with team collaboration",
        stage=PromptStage.APP_SKELETON,
        technical_requirements=[
            "Next.js 14 with App Router",
            "TypeScript for type safety", 
            "Prisma ORM with PostgreSQL",
            "Real-time updates with WebSocket"
        ],
        ui_requirements=[
            "Clean, modern interface design",
            "Drag and drop task management",
            "Mobile-responsive layout",
            "Dark mode support"
        ],
        constraints=[
            "Load time under 2 seconds",
            "WCAG 2.1 accessibility compliance"
        ],
        target_tool=SupportedTool.LOVABLE
    )
    
    project_info = ProjectInfo(
        name="TaskMaster Pro",
        description="Professional task management platform for teams",
        tech_stack=["Next.js", "TypeScript", "Prisma", "PostgreSQL"],
        target_audience="Business professionals and project managers",
        requirements=[],
        industry="Productivity Software",
        complexity_level="medium"
    )
    
    # Generate prompt
    result = generator.generate_prompt(task_context, project_info)
    
    # Display results
    print("=" * 60)
    print(f"Generated Prompt for {result.tool.value} - {result.stage.value}")
    print("=" * 60)
    print(result.prompt)
    print("\n" + "=" * 60)
    print(f"Confidence Score: {result.confidence_score:.2f}")
    print(f"Sources: {len(result.sources)}")
    if result.next_suggested_stage:
        print(f"Next Stage: {result.next_suggested_stage.value}")
    
    # Validate result
    validation = generator.validate_prompt_result(result)
    print(f"Validation Score: {validation['score']}/100")
    if validation['issues']:
        print("Issues:", validation['issues'])

if __name__ == "__main__":
    main()
