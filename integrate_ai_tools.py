#!/usr/bin/env python3
"""
Integrate extracted AI tools documentation into the RAG system database.

This script processes the extracted documentation and creates embeddings
for enhanced prompt generation capabilities.

Author: Ganesh Tappiti
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIToolsIntegrator:
    def __init__(self, data_dir: str, config_dir: str):
        """
        Initialize the integrator.
        
        Args:
            data_dir: Path to data directory with extracted documentation
            config_dir: Path to config directory for tool configurations
        """
        self.data_dir = Path(data_dir)
        self.config_dir = Path(config_dir)
        self.tools_index_file = self.data_dir / "ai_tools_index.json"
        
        # Load tools index
        self.tools_index = self._load_tools_index()
        
    def _load_tools_index(self) -> Dict:
        """Load the AI tools index."""
        if not self.tools_index_file.exists():
            raise FileNotFoundError(f"Tools index not found: {self.tools_index_file}")
        
        with open(self.tools_index_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_tool_configurations(self):
        """Create YAML configuration files for each AI tool."""
        tools_config_dir = self.config_dir / "tools"
        tools_config_dir.mkdir(parents=True, exist_ok=True)
        
        for tool_name, tool_info in self.tools_index["tools"].items():
            config_file = tools_config_dir / f"{tool_name}.yaml"
            
            # Extract tool capabilities and features from documentation
            capabilities = self._extract_tool_capabilities(tool_name, tool_info)
            
            config_content = self._generate_tool_config(tool_name, tool_info, capabilities)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_content)
            
            logger.info(f"Created configuration for {tool_name}: {config_file}")
    
    def _extract_tool_capabilities(self, tool_name: str, tool_info: Dict) -> Dict:
        """Extract capabilities and features from tool documentation."""
        capabilities = {
            "primary_use_cases": [],
            "supported_languages": [],
            "key_features": [],
            "tool_types": [],
            "platforms": [],
            "integration_methods": []
        }
        
        # Read primary files to extract capabilities
        tool_folder = self.data_dir / tool_info["folder"]
        
        for file_name in tool_info.get("primary_files", []):
            file_path = tool_folder / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        
                    # Extract capabilities based on content analysis
                    capabilities.update(self._analyze_tool_content(content, tool_name))
                except Exception as e:
                    logger.warning(f"Failed to read {file_path}: {e}")
        
        return capabilities
    
    def _analyze_tool_content(self, content: str, tool_name: str) -> Dict:
        """Analyze tool content to extract capabilities."""
        capabilities = {
            "primary_use_cases": [],
            "supported_languages": [],
            "key_features": [],
            "tool_types": [],
            "platforms": [],
            "integration_methods": []
        }
        
        # Use case patterns
        use_case_indicators = {
            "web development": ["web", "html", "css", "javascript", "react", "vue", "angular"],
            "backend development": ["backend", "api", "server", "database", "node.js", "python"],
            "mobile development": ["mobile", "ios", "android", "flutter", "react native"],
            "ai development": ["ai", "machine learning", "llm", "neural", "embedding"],
            "code generation": ["generate", "create", "build", "scaffold", "template"],
            "code analysis": ["analyze", "review", "debug", "optimize", "refactor"],
            "documentation": ["document", "readme", "guide", "tutorial", "explanation"],
            "testing": ["test", "unit test", "integration", "qa", "quality"]
        }
        
        # Language patterns
        language_indicators = {
            "javascript": ["javascript", "js", "node", "npm", "react", "vue"],
            "typescript": ["typescript", "ts", "tsx"],
            "python": ["python", "py", "pip", "django", "flask"],
            "java": ["java", "kotlin", "android", "spring"],
            "csharp": ["c#", "csharp", ".net", "dotnet"],
            "go": ["golang", "go"],
            "rust": ["rust", "cargo"],
            "php": ["php", "laravel", "symfony"],
            "swift": ["swift", "ios", "xcode"],
            "dart": ["dart", "flutter"]
        }
        
        # Feature patterns
        feature_indicators = {
            "real-time collaboration": ["collaboration", "real-time", "live", "shared"],
            "code completion": ["completion", "autocomplete", "suggestions", "intellisense"],
            "debugging": ["debug", "breakpoint", "inspect", "trace"],
            "version control": ["git", "github", "version", "commit", "branch"],
            "deployment": ["deploy", "production", "hosting", "cloud"],
            "testing": ["test", "unit", "integration", "e2e"],
            "refactoring": ["refactor", "optimize", "improve", "clean"],
            "documentation generation": ["docs", "documentation", "readme", "api docs"]
        }
        
        # Analyze content for patterns
        for category, patterns in use_case_indicators.items():
            if any(pattern in content for pattern in patterns):
                capabilities["primary_use_cases"].append(category)
        
        for language, patterns in language_indicators.items():
            if any(pattern in content for pattern in patterns):
                capabilities["supported_languages"].append(language)
        
        for feature, patterns in feature_indicators.items():
            if any(pattern in content for pattern in patterns):
                capabilities["key_features"].append(feature)
        
        # Tool type classification
        if tool_name in ["cursor", "vscode"]:
            capabilities["tool_types"].append("ide")
        elif tool_name in ["lovable", "bolt", "v0"]:
            capabilities["tool_types"].append("code_generator")
        elif tool_name in ["devin", "manus"]:
            capabilities["tool_types"].append("ai_agent")
        elif tool_name in ["replit", "codespace"]:
            capabilities["tool_types"].append("cloud_ide")
        
        return capabilities
    
    def _generate_tool_config(self, tool_name: str, tool_info: Dict, capabilities: Dict) -> str:
        """Generate YAML configuration for a tool."""
        
        # Tool-specific descriptions
        descriptions = {
            "lovable": "Lovable.dev - AI-powered web application builder with React and modern frameworks",
            "cursor": "Cursor - AI-powered code editor with intelligent code completion",
            "v0": "v0 by Vercel - AI interface designer and React component generator",
            "devin": "Devin AI - Autonomous AI software engineer for complex coding tasks",
            "replit": "Replit - Cloud-based IDE with collaborative coding features",
            "windsurf": "Windsurf - AI-powered development environment",
            "vscode": "VS Code Agent - AI assistant for Visual Studio Code",
            "same": "Same.dev - AI-powered development platform",
            "manus": "Manus Agent - AI coding assistant with advanced capabilities",
            "bolt": "Bolt.new - AI-powered full-stack application generator",
            "cline": "Cline - AI coding assistant with command-line integration",
            "perplexity": "Perplexity - AI-powered search and research tool",
            "spawn": "Spawn - AI game development platform",
            "orchids": "Orchids.app - AI-powered application development platform"
        }
        
        description = descriptions.get(tool_name, f"{tool_name.title()} - AI development tool")
        
        config = f"""# {tool_name.title()} Configuration
# Generated from extracted documentation

tool:
  name: "{tool_name}"
  display_name: "{tool_name.title()}"
  description: "{description}"
  
  # Tool classification
  type: "{capabilities.get('tool_types', ['general'])[0] if capabilities.get('tool_types') else 'general'}"
  category: "ai_development_tool"
  
  # Capabilities
  primary_use_cases:
{self._format_yaml_list(capabilities.get('primary_use_cases', []))}
  
  supported_languages:
{self._format_yaml_list(capabilities.get('supported_languages', []))}
  
  key_features:
{self._format_yaml_list(capabilities.get('key_features', []))}
  
  # Documentation files
  documentation:
    folder: "{tool_info['folder']}"
    primary_files:
{self._format_yaml_list(tool_info.get('primary_files', []))}
    all_files:
{self._format_yaml_list(tool_info.get('files', []))}
  
  # Prompt generation settings
  prompt_generation:
    include_system_prompts: true
    include_examples: true
    include_best_practices: true
    context_window_size: 4000
    
  # Integration settings
  integration:
    api_available: false
    web_interface: true
    cli_available: false
    
  # Metadata
  metadata:
    extraction_date: "{self.tools_index['extraction_date']}"
    source_repository: "{self.tools_index['source_repository']}"
    file_count: {tool_info['file_count']}
"""
        
        return config
    
    def _format_yaml_list(self, items: List[str]) -> str:
        """Format a list for YAML output."""
        if not items:
            return "    []"
        
        return "\n".join(f"    - \"{item}\"" for item in items)
    
    def create_documentation_index(self):
        """Create a comprehensive documentation index."""
        index = {
            "ai_tools_documentation": {
                "version": "1.0",
                "extraction_date": self.tools_index["extraction_date"],
                "source_repository": self.tools_index["source_repository"],
                "total_tools": len(self.tools_index["tools"]),
                "total_files": sum(tool["file_count"] for tool in self.tools_index["tools"].values()),
                "tools": {}
            }
        }
        
        for tool_name, tool_info in self.tools_index["tools"].items():
            tool_folder = self.data_dir / tool_info["folder"]
            
            # Analyze each file
            file_analysis = {}
            for file_name in tool_info["files"]:
                file_path = tool_folder / file_name
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        file_analysis[file_name] = {
                            "size_bytes": len(content.encode('utf-8')),
                            "line_count": len(content.splitlines()),
                            "char_count": len(content),
                            "file_type": self._classify_file_type(file_name, content),
                            "contains_examples": "example" in content.lower() or "```" in content,
                            "contains_prompts": "prompt" in file_name.lower() or "system" in content.lower()
                        }
                    except Exception as e:
                        logger.warning(f"Failed to analyze {file_path}: {e}")
                        file_analysis[file_name] = {"error": str(e)}
            
            index["ai_tools_documentation"]["tools"][tool_name] = {
                **tool_info,
                "file_analysis": file_analysis
            }
        
        # Save index
        index_path = self.data_dir / "comprehensive_documentation_index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created comprehensive documentation index: {index_path}")
        
        return index
    
    def _classify_file_type(self, file_name: str, content: str) -> str:
        """Classify the type of documentation file."""
        file_name_lower = file_name.lower()
        content_lower = content.lower()
        
        if "prompt" in file_name_lower:
            return "system_prompt"
        elif "tools" in file_name_lower and file_name.endswith('.json'):
            return "tool_definitions"
        elif "agent" in file_name_lower:
            return "agent_configuration"
        elif "memory" in file_name_lower:
            return "memory_system"
        elif file_name.endswith('.json'):
            return "json_configuration"
        elif "readme" in file_name_lower:
            return "documentation"
        elif "instruction" in file_name_lower:
            return "instructions"
        else:
            return "general_documentation"
    
    def create_integration_summary(self):
        """Create a summary of the integration process."""
        summary_path = self.data_dir / "integration_summary.md"
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# AI Tools Integration Summary\n\n")
            f.write(f"Integration completed on: {self.tools_index['extraction_date']}\n\n")
            
            f.write("## Tools Integrated\n\n")
            for tool_name, tool_info in self.tools_index["tools"].items():
                f.write(f"### {tool_name.title()}\n")
                f.write(f"- **Files:** {tool_info['file_count']}\n")
                f.write(f"- **Folder:** `{tool_info['folder']}`\n")
                f.write(f"- **Primary files:** {', '.join(f'`{f}`' for f in tool_info.get('primary_files', []))}\n")
                f.write(f"- **Configuration:** `config/tools/{tool_name}.yaml`\n\n")
            
            f.write("## Next Steps\n\n")
            f.write("1. **Update RAG Database**: Run the database update script to index the new documentation\n")
            f.write("2. **Test Prompt Generation**: Verify that the new tools appear in prompt generation options\n")
            f.write("3. **Configure Embeddings**: Ensure all documentation is properly embedded for retrieval\n")
            f.write("4. **Update UI**: Add new tools to the web interface selection options\n\n")
            
            f.write("## Files Created\n\n")
            f.write("- `ai_tools_index.json` - Index of all extracted tools\n")
            f.write("- `comprehensive_documentation_index.json` - Detailed analysis of all files\n")
            f.write("- `config/tools/*.yaml` - Configuration files for each tool\n")
            f.write("- Individual tool documentation in respective folders\n\n")
        
        logger.info(f"Created integration summary: {summary_path}")
    
    def run_integration(self):
        """Run the complete integration process."""
        logger.info("Starting AI tools integration...")
        
        # Create tool configurations
        self.create_tool_configurations()
        
        # Create comprehensive index
        self.create_documentation_index()
        
        # Create integration summary
        self.create_integration_summary()
        
        logger.info("Integration completed successfully!")
        
        print("\n" + "="*60)
        print("AI TOOLS INTEGRATION COMPLETED!")
        print("="*60)
        print(f"Tools integrated: {len(self.tools_index['tools'])}")
        print(f"Configuration files created: {len(self.tools_index['tools'])}")
        print(f"Documentation files indexed: {sum(tool['file_count'] for tool in self.tools_index['tools'].values())}")
        print("\nNext steps:")
        print("1. Run database update to index the new documentation")
        print("2. Test the enhanced prompt generation with new tools")
        print("3. Update the web interface to include new tool options")


def main():
    """Main execution function."""
    
    # Set up paths
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    config_dir = base_dir / "config"
    
    # Initialize and run integrator
    integrator = AIToolsIntegrator(str(data_dir), str(config_dir))
    
    try:
        integrator.run_integration()
        
    except Exception as e:
        logger.error(f"Integration failed: {e}")
        raise


if __name__ == "__main__":
    main()
