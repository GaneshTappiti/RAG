"""
Enhanced Tool-Specific Prompt Generator
Supports multiple no-code/low-code tools with RAG-powered documentation retrieval
"""

import os
import yaml
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
import glob

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ToolConfig:
    """Configuration for a specific tool"""
    name: str
    format: str
    tone: str
    framework: str
    use_cases: List[str]
    strategies: Dict[str, Any]
    stages: List[str]
    components: List[str]

@dataclass
class TaskContext:
    """Enhanced task context with tool-specific information"""
    task_type: str
    project_name: str
    description: str
    tool: str
    stage: str
    technical_requirements: List[str]
    ui_requirements: List[str]
    constraints: List[str]
    page_type: Optional[str] = None
    component_type: Optional[str] = None

@dataclass
class ProjectInfo:
    """Project information structure"""
    name: str
    description: str
    tech_stack: List[str]
    target_audience: str
    requirements: List[str]
    tool: str

class ToolSpecificPromptGenerator:
    """Enhanced prompt generator supporting multiple tools"""
    
    def __init__(self, chroma_path: str = "storage/chroma_multi_tool"):
        self.chroma_path = chroma_path
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        self.tools_config = self._load_all_tools_config()
        self.available_tools = list(self.tools_config.keys())
        
        # Initialize vector store
        self._initialize_vector_store()
    
    def _load_all_tools_config(self) -> Dict[str, ToolConfig]:
        """Load configuration for all available tools"""
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
            except Exception as e:
                print(f"Error loading config for {tool_name}: {e}")
        
        return tools_config
    
    def _initialize_vector_store(self):
        """Initialize or load the vector store with tool-specific metadata"""
        if os.path.exists(self.chroma_path):
            self.vector_store = Chroma(
                persist_directory=self.chroma_path,
                embedding_function=self.embeddings
            )
        else:
            self._create_vector_store()
    
    def _create_vector_store(self):
        """Create vector store with tool-specific documentation"""
        documents = []
        data_dir = Path("data")
        
        # Load documents for each tool
        for tool_dir in data_dir.glob("*_docs"):
            tool_name = tool_dir.name.replace('_docs', '')
            
            # Load all markdown files in the tool directory
            for doc_file in tool_dir.glob("*.md"):
                try:
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Determine document type
                    doc_type = self._determine_doc_type(doc_file.name)
                    
                    # Create document with enhanced metadata
                    doc = Document(
                        page_content=content,
                        metadata={
                            'source': str(doc_file),
                            'tool': tool_name,
                            'doc_type': doc_type,
                            'filename': doc_file.name,
                            'comprehensive_prompt': 'comprehensive_system_prompt' in doc_file.name
                        }
                    )
                    documents.append(doc)
                except Exception as e:
                    print(f"Error loading {doc_file}: {e}")
        
        if not documents:
            raise ValueError("No documents found for indexing")
        
        print(f"📚 Loading {len(documents)} documents from {len(list(data_dir.glob('*_docs')))} tools")
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        split_docs = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            persist_directory=self.chroma_path
        )
        
        print(f"✅ Created vector store with {len(split_docs)} document chunks")
    
    def _determine_doc_type(self, filename: str) -> str:
        """Determine document type from filename"""
        filename_lower = filename.lower()
        
        if 'comprehensive' in filename_lower:
            return 'comprehensive_guide'
        elif 'prompt' in filename_lower:
            return 'system_prompt'
        elif 'tool' in filename_lower:
            return 'tool_config'
        elif 'guide' in filename_lower:
            return 'user_guide'
        elif 'pattern' in filename_lower:
            return 'design_patterns'
        elif 'api' in filename_lower:
            return 'api_docs'
        else:
            return 'documentation'
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        return self.available_tools
    
    def get_tool_info(self, tool: str) -> Dict[str, Any]:
        """Get information about a specific tool"""
        if tool not in self.tools_config:
            return {}
        
        config = self.tools_config[tool]
        return {
            'name': config.name,
            'format': config.format,
            'tone': config.tone,
            'framework': config.framework,
            'use_cases': config.use_cases,
            'stages': config.stages,
            'components': config.components
        }
    
    def get_tool_stages(self, tool: str) -> List[str]:
        """Get development stages for a specific tool"""
        if tool not in self.tools_config:
            return ['planning', 'implementation', 'testing']
        return self.tools_config[tool].stages
    
    def get_tool_components(self, tool: str) -> List[str]:
        """Get supported components for a specific tool"""
        if tool not in self.tools_config:
            return ['ui', 'logic', 'data']
        return self.tools_config[tool].components
    
    def get_relevant_context(self, tool: str, task_type: str, description: str, 
                           stage: Optional[str] = None, num_docs: int = 5) -> List[Document]:
        """Get relevant context for tool-specific prompt generation"""
        if not self.vector_store:
            return []
        
        # Build search query
        search_query = f"{task_type} {description}"
        if stage:
            search_query += f" {stage}"
        
        # Create filter for tool-specific documents
        filter_dict = {"tool": tool}
        
        try:
            # Perform similarity search with metadata filtering
            docs = self.vector_store.similarity_search(
                search_query,
                k=num_docs,
                filter=filter_dict
            )
            return docs
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []
    
    def generate_stage_prompt(self, task_context: TaskContext, 
                            project_info: ProjectInfo) -> str:
        """Generate a stage-specific prompt for the selected tool"""
        tool = task_context.tool
        stage = task_context.stage
        
        if tool not in self.tools_config:
            return f"Tool '{tool}' not supported"
        
        config = self.tools_config[tool]
        
        # Get relevant documentation
        context_docs = self.get_relevant_context(
            tool=tool,
            task_type=task_context.task_type,
            description=task_context.description,
            stage=stage
        )
        
        # Build context from retrieved documents
        context_content = ""
        if context_docs:
            context_content = "\n\n".join([
                f"**{doc.metadata.get('doc_type', 'Documentation')}:**\n{doc.page_content}"
                for doc in context_docs[:3]
            ])
        
        # Select appropriate prompting strategy
        strategy = self._select_strategy(config, task_context)
        
        # Generate the prompt
        prompt = self._build_stage_prompt(
            config=config,
            strategy=strategy,
            task_context=task_context,
            project_info=project_info,
            context_content=context_content
        )
        
        return prompt
    
    def _select_strategy(self, config: ToolConfig, task_context: TaskContext) -> Dict[str, Any]:
        """Select the best prompting strategy for the given context"""
        strategies = config.strategies
        
        # Default strategy selection logic
        if task_context.stage in ['planning', 'architecture']:
            return strategies.get('structured', strategies.get('enhanced', {}))
        elif task_context.stage in ['implementation', 'development']:
            return strategies.get('incremental', strategies.get('conversational', {}))
        elif task_context.stage in ['testing', 'debugging']:
            return strategies.get('meta', strategies.get('structured', {}))
        else:
            # Return the first available strategy
            return next(iter(strategies.values()), {})
    
    def _build_stage_prompt(self, config: ToolConfig, strategy: Dict[str, Any],
                          task_context: TaskContext, project_info: ProjectInfo,
                          context_content: str) -> str:
        """Build the final stage-specific prompt"""
        
        # Base prompt structure
        prompt_parts = [
            f"# {config.name} - {task_context.stage.title()} Stage",
            f"\n## Project: {project_info.name}",
            f"\n**Tool:** {config.name}",
            f"**Stage:** {task_context.stage.title()}",
            f"**Task Type:** {task_context.task_type}",
            f"**Framework:** {config.framework}",
        ]
        
        # Add project context
        prompt_parts.extend([
            f"\n## Project Context",
            f"**Description:** {project_info.description}",
            f"**Tech Stack:** {', '.join(project_info.tech_stack)}",
            f"**Target Audience:** {project_info.target_audience}",
        ])
        
        # Add task details
        prompt_parts.extend([
            f"\n## Task Details",
            f"**Description:** {task_context.description}",
        ])
        
        if task_context.technical_requirements:
            prompt_parts.append(f"**Technical Requirements:**")
            for req in task_context.technical_requirements:
                prompt_parts.append(f"- {req}")
        
        if task_context.ui_requirements:
            prompt_parts.append(f"\n**UI/UX Requirements:**")
            for req in task_context.ui_requirements:
                prompt_parts.append(f"- {req}")
        
        if task_context.constraints:
            prompt_parts.append(f"\n**Constraints:**")
            for constraint in task_context.constraints:
                prompt_parts.append(f"- {constraint}")
        
        # Add relevant documentation context
        if context_content:
            prompt_parts.extend([
                f"\n## Relevant Documentation",
                context_content
            ])
        
        # Add tool-specific guidelines
        prompt_parts.extend([
            f"\n## {config.name} Guidelines",
            f"**Tone:** {config.tone}",
            f"**Format:** {config.format}",
        ])
        
        # Add strategy-specific template
        if strategy and 'template' in strategy:
            template = strategy['template']
            prompt_parts.extend([
                f"\n## Implementation Strategy",
                f"**Strategy:** {template}",
            ])
        
        # Add stage-specific instructions
        stage_instructions = self._get_stage_instructions(task_context.stage, config.name)
        if stage_instructions:
            prompt_parts.extend([
                f"\n## {task_context.stage.title()} Stage Instructions",
                stage_instructions
            ])
        
        # Final call to action
        prompt_parts.extend([
            f"\n## Action Required",
            f"Please {task_context.task_type} for the {task_context.stage} stage of {project_info.name} using {config.name}.",
            f"Focus on delivering high-quality, {config.tone} results that align with the {config.framework} approach."
        ])
        
        return "\n".join(prompt_parts)
    
    def _get_stage_instructions(self, stage: str, tool_name: str) -> str:
        """Get stage-specific instructions"""
        instructions = {
            'planning': f"Focus on architecture, user stories, and technical planning for {tool_name}",
            'design': f"Create detailed UI/UX designs and component specifications for {tool_name}",
            'implementation': f"Build the actual functionality using {tool_name} best practices",
            'testing': f"Implement testing strategies and quality assurance for {tool_name}",
            'deployment': f"Prepare for deployment and production setup using {tool_name}",
            'optimization': f"Optimize performance and user experience in {tool_name}"
        }
        
        return instructions.get(stage, f"Complete the {stage} phase using {tool_name}")
    
    def validate_prompt(self, prompt: str, tool: str) -> Dict[str, Any]:
        """Validate the generated prompt for the specific tool"""
        validation = {
            'score': 0,
            'is_valid': False,
            'issues': [],
            'suggestions': []
        }
        
        # Basic validation checks
        if len(prompt) < 100:
            validation['issues'].append("Prompt is too short")
        elif len(prompt) > 5000:
            validation['issues'].append("Prompt might be too long")
        else:
            validation['score'] += 30
        
        # Check for tool-specific elements
        if tool in prompt:
            validation['score'] += 20
        else:
            validation['issues'].append(f"Tool name '{tool}' not mentioned in prompt")
        
        # Check for structure
        required_sections = ['Project', 'Task', 'Guidelines']
        for section in required_sections:
            if section in prompt:
                validation['score'] += 15
            else:
                validation['suggestions'].append(f"Consider adding '{section}' section")
        
        # Check for technical details
        if any(word in prompt.lower() for word in ['requirements', 'constraints', 'specifications']):
            validation['score'] += 15
        else:
            validation['suggestions'].append("Add more technical specifications")
        
        validation['is_valid'] = validation['score'] >= 70
        
        return validation
    
    def get_tool_suggestions(self, tool: str, project_type: str) -> List[str]:
        """Get task suggestions for a specific tool and project type"""
        if tool not in self.tools_config:
            return []
        
        config = self.tools_config[tool]
        base_suggestions = config.use_cases
        
        # Add project-type specific suggestions
        project_suggestions = {
            'web_app': ['landing page', 'dashboard', 'user authentication', 'responsive design'],
            'mobile_app': ['navigation', 'user profile', 'data sync', 'offline functionality'],
            'ecommerce': ['product catalog', 'shopping cart', 'payment integration', 'order management'],
            'blog': ['article layout', 'comment system', 'content management', 'SEO optimization']
        }
        
        suggestions = base_suggestions.copy()
        if project_type in project_suggestions:
            suggestions.extend(project_suggestions[project_type])
        
        return suggestions[:8]  # Limit to 8 suggestions
