"""
Enhanced Tool-Specific Prompt Generator with Google Gemini Embeddings
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
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Import our new embedding manager
import sys
sys.path.append(str(Path(__file__).parent.parent))
from core.embedding_manager import create_embedding_manager, EmbeddingProvider

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

class GeminiToolSpecificPromptGenerator:
    """Enhanced prompt generator with Google Gemini embeddings"""
    
    def __init__(self, 
                 chroma_path: str = "storage/chroma_gemini", 
                 embedding_provider: str = "google_gemini",
                 embedding_model: Optional[str] = None):
        """
        Initialize the generator with Gemini embeddings
        
        Args:
            chroma_path: Path to ChromaDB storage
            embedding_provider: Provider for embeddings ("google_gemini" or "openai")  
            embedding_model: Specific model name (optional)
        """
        self.chroma_path = chroma_path
        self.embedding_provider = embedding_provider
        self.embedding_model = embedding_model
        
        # Initialize embedding manager
        self.embedding_manager = create_embedding_manager(
            provider=embedding_provider,
            model_name=embedding_model
        )
        
        self.vector_store = None
        self.tools_config = self._load_all_tools_config()
        self.available_tools = list(self.tools_config.keys())
        
        # Initialize vector store
        self._initialize_vector_store()
    
    def _load_all_tools_config(self) -> Dict[str, ToolConfig]:
        """Load configuration for all available tools"""
        tools_config = {}
        config_dir = Path("config/tools")
        
        # Create default config if directory doesn't exist
        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)
            self._create_default_tools_config(config_dir)
        
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
    
    def _create_default_tools_config(self, config_dir: Path):
        """Create default tool configurations"""
        default_tools = {
            "lovable": {
                "tool_name": "Lovable",
                "format": "structured",
                "tone": "friendly_professional",
                "framework": "React/Next.js",
                "preferred_use_cases": ["web_apps", "prototypes", "mvp"],
                "prompting_strategies": {
                    "step_by_step": True,
                    "context_first": True,
                    "examples": True
                },
                "development_stages": ["planning", "design", "implementation", "testing"],
                "supported_components": ["ui", "routing", "state", "api"]
            },
            "cursor": {
                "tool_name": "Cursor",
                "format": "conversational",
                "tone": "technical",
                "framework": "Multi-language IDE",
                "preferred_use_cases": ["code_editing", "refactoring", "debugging"],
                "prompting_strategies": {
                    "context_aware": True,
                    "incremental": True,
                    "file_aware": True
                },
                "development_stages": ["coding", "testing", "debugging", "optimization"],
                "supported_components": ["code", "tests", "documentation", "configs"]
            }
        }
        
        for tool_name, config in default_tools.items():
            config_file = config_dir / f"{tool_name}.yaml"
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False)
    
    def _initialize_vector_store(self):
        """Initialize or load the vector store with Gemini embeddings"""
        if os.path.exists(self.chroma_path):
            # Load existing vector store
            try:
                self.vector_store = Chroma(
                    persist_directory=self.chroma_path,
                    embedding_function=self.embedding_manager.get_embedding_model()
                )
                print(f"Loaded existing vector store from {self.chroma_path}")
                print(f"Using {self.embedding_provider} embeddings with model: {self.embedding_manager.config.model_name}")
            except Exception as e:
                print(f"Error loading vector store: {e}")
                print("Creating new vector store...")
                self._create_vector_store()
        else:
            self._create_vector_store()
    
    def _create_vector_store(self):
        """Create new vector store from documentation"""
        documents = self._load_documents()
        
        if not documents:
            print("No documents found. Creating empty vector store.")
            self.vector_store = Chroma(
                persist_directory=self.chroma_path,
                embedding_function=self.embedding_manager.get_embedding_model()
            )
            return
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embedding_manager.get_embedding_model(),
            persist_directory=self.chroma_path
        )
        
        print(f"Created vector store with {len(splits)} document chunks")
        print(f"Using {self.embedding_provider} embeddings")
    
    def _load_documents(self) -> List[Document]:
        """Load documents from various sources"""
        documents = []
        
        # Load from data directory if it exists
        data_dir = Path("data")
        if data_dir.exists():
            for doc_folder in data_dir.iterdir():
                if doc_folder.is_dir() and doc_folder.name.endswith('_docs'):
                    try:
                        loader = DirectoryLoader(
                            str(doc_folder),
                            glob="**/*.{txt,md,json}",
                            loader_cls=TextLoader,
                            loader_kwargs={'encoding': 'utf-8'}
                        )
                        folder_docs = loader.load()
                        
                        # Add metadata
                        tool_name = doc_folder.name.replace('_docs', '')
                        for doc in folder_docs:
                            doc.metadata.update({
                                'tool': tool_name,
                                'source_type': 'documentation'
                            })
                        
                        documents.extend(folder_docs)
                        print(f"Loaded {len(folder_docs)} documents from {doc_folder}")
                        
                    except Exception as e:
                        print(f"Error loading documents from {doc_folder}: {e}")
        
        return documents
    
    def get_relevant_context(self, query: str, tool: str, k: int = 5) -> List[str]:
        """Get relevant documentation context for a query"""
        if not self.vector_store:
            return []
        
        try:
            # Enhanced query with tool context
            enhanced_query = f"{tool} {query}"
            
            # Search for relevant documents
            docs = self.vector_store.similarity_search(
                enhanced_query,
                k=k,
                filter={"tool": tool} if tool in self.available_tools else None
            )
            
            # Extract context
            context = []
            for doc in docs:
                context.append(doc.page_content)
            
            return context
            
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []
    
    def generate_prompt(self, project_info: ProjectInfo, task_context: TaskContext) -> str:
        """Generate enhanced prompt using RAG and tool-specific configuration"""
        
        # Get tool configuration
        tool_config = self.tools_config.get(task_context.tool)
        if not tool_config:
            tool_config = self._get_default_tool_config(task_context.tool)
        
        # Get relevant context from vector store
        context_query = f"{task_context.description} {task_context.task_type}"
        relevant_context = self.get_relevant_context(
            context_query, 
            task_context.tool, 
            k=3
        )
        
        # Build prompt sections
        prompt_sections = []
        
        # Tool-specific header
        prompt_sections.append(self._build_tool_header(tool_config, task_context))
        
        # Project context
        prompt_sections.append(self._build_project_context(project_info))
        
        # Task context
        prompt_sections.append(self._build_task_context(task_context))
        
        # Relevant documentation context
        if relevant_context:
            prompt_sections.append(self._build_documentation_context(relevant_context))
        
        # Tool-specific strategies
        prompt_sections.append(self._build_strategy_section(tool_config, task_context))
        
        # Output format
        prompt_sections.append(self._build_output_format(tool_config))
        
        return "\n\n".join(prompt_sections)
    
    def _get_default_tool_config(self, tool_name: str) -> ToolConfig:
        """Get default configuration for unknown tools"""
        return ToolConfig(
            name=tool_name.title(),
            format="structured",
            tone="professional",
            framework="General development",
            use_cases=["general_development"],
            strategies={"step_by_step": True},
            stages=["planning", "implementation", "testing"],
            components=["ui", "logic", "data"]
        )
    
    def _build_tool_header(self, tool_config: ToolConfig, task_context: TaskContext) -> str:
        """Build tool-specific header"""
        return f"""# {tool_config.name} Prompt Generator

**Tool**: {tool_config.name}
**Framework**: {tool_config.framework}
**Task Type**: {task_context.task_type}
**Stage**: {task_context.stage}

---"""
    
    def _build_project_context(self, project_info: ProjectInfo) -> str:
        """Build project context section"""
        tech_stack = ", ".join(project_info.tech_stack) if project_info.tech_stack else "Not specified"
        requirements = "\n".join([f"- {req}" for req in project_info.requirements])
        
        return f"""## Project Information

**Name**: {project_info.name}
**Description**: {project_info.description}
**Tech Stack**: {tech_stack}
**Target Audience**: {project_info.target_audience}

**Requirements**:
{requirements}"""
    
    def _build_task_context(self, task_context: TaskContext) -> str:
        """Build task context section"""
        tech_reqs = "\n".join([f"- {req}" for req in task_context.technical_requirements])
        ui_reqs = "\n".join([f"- {req}" for req in task_context.ui_requirements])
        constraints = "\n".join([f"- {constraint}" for constraint in task_context.constraints])
        
        return f"""## Task Context

**Description**: {task_context.description}

**Technical Requirements**:
{tech_reqs}

**UI Requirements**:
{ui_reqs}

**Constraints**:
{constraints}"""
    
    def _build_documentation_context(self, context: List[str]) -> str:
        """Build documentation context section"""
        context_text = "\n\n".join([f"### Context {i+1}\n{ctx}" for i, ctx in enumerate(context)])
        
        return f"""## Relevant Documentation

{context_text}"""
    
    def _build_strategy_section(self, tool_config: ToolConfig, task_context: TaskContext) -> str:
        """Build tool-specific strategy section"""
        strategies = []
        
        if tool_config.strategies.get("step_by_step"):
            strategies.append("- Break down the task into clear, actionable steps")
        
        if tool_config.strategies.get("context_first"):
            strategies.append("- Provide full context before implementation details")
        
        if tool_config.strategies.get("examples"):
            strategies.append("- Include relevant examples and code snippets")
        
        if tool_config.strategies.get("incremental"):
            strategies.append("- Focus on incremental improvements and iterations")
        
        strategy_text = "\n".join(strategies) if strategies else "- Follow standard development practices"
        
        return f"""## Implementation Strategy

{strategy_text}

**Tone**: {tool_config.tone}
**Supported Components**: {", ".join(tool_config.components)}"""
    
    def _build_output_format(self, tool_config: ToolConfig) -> str:
        """Build output format section"""
        return f"""## Expected Output

Please provide a {tool_config.format} response that includes:

1. **Implementation Plan**: Step-by-step approach
2. **Code Structure**: File organization and architecture
3. **Key Components**: Main features and functionality
4. **Integration Points**: How components work together
5. **Testing Strategy**: Validation and quality assurance
6. **Next Steps**: Immediate actions to take

Format your response in a clear, {tool_config.tone} tone suitable for {tool_config.name}."""
    
    def update_vector_store(self, new_documents: List[Document]):
        """Update vector store with new documents"""
        if not self.vector_store:
            self._create_vector_store()
            return
        
        try:
            # Split new documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(new_documents)
            
            # Add to vector store
            self.vector_store.add_documents(splits)
            
            print(f"Added {len(splits)} new document chunks to vector store")
            
        except Exception as e:
            print(f"Error updating vector store: {e}")
    
    def get_embedding_info(self) -> Dict[str, Any]:
        """Get information about the current embedding configuration"""
        return self.embedding_manager.get_provider_info()


# Example usage
if __name__ == "__main__":
    # Test the enhanced generator
    try:
        # Initialize with Gemini embeddings
        generator = GeminiToolSpecificPromptGenerator(
            embedding_provider="google_gemini",
            embedding_model="models/embedding-001"
        )
        
        print("✓ Generator initialized successfully!")
        print(f"Embedding info: {generator.get_embedding_info()}")
        
        # Test prompt generation
        project = ProjectInfo(
            name="Test App",
            description="A simple test application",
            tech_stack=["React", "Node.js"],
            target_audience="Developers",
            requirements=["Fast loading", "Responsive design"],
            tool="lovable"
        )
        
        task = TaskContext(
            task_type="ui_development",
            project_name="Test App",
            description="Create a landing page",
            tool="lovable",
            stage="implementation",
            technical_requirements=["React components", "CSS styling"],
            ui_requirements=["Modern design", "Mobile responsive"],
            constraints=["Single page application"]
        )
        
        prompt = generator.generate_prompt(project, task)
        print(f"\n✓ Generated prompt ({len(prompt)} characters)")
        
    except Exception as e:
        print(f"✗ Error testing generator: {e}")
        print("Make sure GOOGLE_API_KEY is set in your environment")
