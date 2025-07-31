"""
Enhanced Data Integration Script for AI Tools System Prompts
Integrates comprehensive system prompts and models from external repository
"""

import os
import json
import yaml
import shutil
from pathlib import Path
from typing import Dict, List, Any
import re

class AIToolsDataIntegrator:
    """Integrates external AI tools data into our RAG system"""
    
    def __init__(self, external_repo_path: str = "external_ai_tools_data", target_data_dir: str = "data"):
        self.external_repo_path = Path(external_repo_path)
        self.target_data_dir = Path(target_data_dir)
        self.processed_tools = {}
        
    def extract_and_integrate_all_tools(self):
        """Main method to extract and integrate all AI tools data"""
        print("🚀 Starting AI Tools Data Integration...")
        
        # Tool mapping from external repo to our system
        tool_mappings = {
            "Lovable": "lovable",
            "Cursor Prompts": "cursor", 
            "v0 Prompts and Tools": "v0",
            "Windsurf": "windsurf",
            "Devin AI": "devin",
            "Replit": "replit",
            "VSCode Agent": "vscode",
            "Same.dev": "same",
            "Manus Agent Tools & Prompt": "manus",
            "dia": "dia",
            "Trae": "trae",
            "Cluely": "cluely",
            "Xcode": "xcode",
            "Perplexity": "perplexity",
            "Orchids.app": "orchids",
            "Warp.dev": "warp",
            "-Spawn": "spawn",
            "Z.ai Code": "zai",
            "Open Source prompts/Bolt": "bolt",
            "Open Source prompts/Cline": "cline",
            "Open Source prompts/Codex CLI": "codex",
            "Open Source prompts/Lumo": "lumo",
            "Open Source prompts/RooCode": "roocode",
        }
        
        for external_name, internal_name in tool_mappings.items():
            self._process_tool(external_name, internal_name)
        
        # Create enhanced configurations
        self._create_enhanced_tool_configs()
        
        # Update existing data with new comprehensive prompts
        self._update_existing_documentation()
        
        print(f"✅ Integration complete! Processed {len(self.processed_tools)} tools")
        self._print_integration_summary()
    
    def _process_tool(self, external_name: str, internal_name: str):
        """Process a specific tool's data"""
        if "/" in external_name:
            # Handle nested paths like "Open Source prompts/Bolt"
            external_path = self.external_repo_path
            for part in external_name.split("/"):
                external_path = external_path / part
        else:
            external_path = self.external_repo_path / external_name
        
        if not external_path.exists():
            print(f"⚠️  Path not found: {external_path}")
            return
        
        print(f"📁 Processing {internal_name} from {external_path}")
        
        # Create target directory
        target_dir = self.target_data_dir / f"{internal_name}_docs"
        target_dir.mkdir(exist_ok=True)
        
        # Extract prompts and documentation
        extracted_data = self._extract_prompts_and_docs(external_path)
        
        # Save extracted data
        self._save_extracted_data(target_dir, internal_name, extracted_data)
        
        # Store for configuration generation
        self.processed_tools[internal_name] = extracted_data
    
    def _extract_prompts_and_docs(self, tool_path: Path) -> Dict[str, Any]:
        """Extract prompts and documentation from a tool directory"""
        extracted = {
            'prompts': {},
            'tools': {},
            'metadata': {
                'source_path': str(tool_path),
                'files_processed': []
            }
        }
        
        for file_path in tool_path.rglob("*"):
            if file_path.is_file():
                file_extension = file_path.suffix.lower()
                relative_path = file_path.relative_to(tool_path)
                
                try:
                    if file_extension == '.txt':
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        self._process_text_file(content, str(relative_path), extracted)
                    elif file_extension == '.json':
                        content = json.loads(file_path.read_text(encoding='utf-8', errors='ignore'))
                        extracted['tools'][str(relative_path)] = content
                    elif file_extension == '.md':
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        extracted['prompts'][f"docs_{relative_path.stem}"] = content
                    
                    extracted['metadata']['files_processed'].append(str(relative_path))
                except Exception as e:
                    print(f"⚠️  Error processing {file_path}: {e}")
        
        return extracted
    
    def _process_text_file(self, content: str, filename: str, extracted: Dict[str, Any]):
        """Process text files and categorize content"""
        filename_lower = filename.lower()
        
        if 'prompt' in filename_lower:
            # This is a system prompt
            if 'agent' in filename_lower:
                extracted['prompts']['agent_prompt'] = content
            elif 'chat' in filename_lower:
                extracted['prompts']['chat_prompt'] = content
            elif 'memory' in filename_lower:
                extracted['prompts']['memory_prompt'] = content
            else:
                extracted['prompts']['main_prompt'] = content
        else:
            # General documentation
            extracted['prompts'][f"doc_{filename.replace('.txt', '')}"] = content
    
    def _save_extracted_data(self, target_dir: Path, tool_name: str, extracted_data: Dict[str, Any]):
        """Save extracted data to target directory"""
        
        # Save main system prompt as comprehensive guide
        if extracted_data['prompts']:
            main_content = self._create_comprehensive_guide(tool_name, extracted_data)
            
            with open(target_dir / "comprehensive_system_prompt.md", 'w', encoding='utf-8') as f:
                f.write(main_content)
        
        # Save individual prompt files
        for prompt_name, content in extracted_data['prompts'].items():
            filename = f"{prompt_name}.md"
            with open(target_dir / filename, 'w', encoding='utf-8') as f:
                f.write(self._format_as_markdown(content, prompt_name, tool_name))
        
        # Save tools configuration if available
        if extracted_data['tools']:
            with open(target_dir / "tools_config.json", 'w', encoding='utf-8') as f:
                json.dump(extracted_data['tools'], f, indent=2)
        
        # Save metadata
        with open(target_dir / "extraction_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(extracted_data['metadata'], f, indent=2)
    
    def _create_comprehensive_guide(self, tool_name: str, extracted_data: Dict[str, Any]) -> str:
        """Create a comprehensive guide combining all prompts and documentation"""
        
        content = [
            f"# {tool_name.title()} - Comprehensive System Prompt Guide",
            "",
            f"This document contains the complete system prompts and documentation for {tool_name.title()}, extracted from the comprehensive AI tools repository.",
            "",
            "## Table of Contents",
            ""
        ]
        
        # Add table of contents
        sections = []
        if 'main_prompt' in extracted_data['prompts'] or 'agent_prompt' in extracted_data['prompts']:
            sections.append("- [Main System Prompt](#main-system-prompt)")
        if 'chat_prompt' in extracted_data['prompts']:
            sections.append("- [Chat Prompt](#chat-prompt)")
        if 'memory_prompt' in extracted_data['prompts']:
            sections.append("- [Memory Management](#memory-management)")
        if extracted_data['tools']:
            sections.append("- [Available Tools](#available-tools)")
        
        content.extend(sections)
        content.extend(["", "---", ""])
        
        # Add main system prompt
        main_prompt = extracted_data['prompts'].get('main_prompt') or extracted_data['prompts'].get('agent_prompt')
        if main_prompt:
            content.extend([
                "## Main System Prompt",
                "",
                "```",
                main_prompt,
                "```",
                ""
            ])
        
        # Add specialized prompts
        for prompt_type in ['chat_prompt', 'memory_prompt']:
            if prompt_type in extracted_data['prompts']:
                section_name = prompt_type.replace('_', ' ').title()
                content.extend([
                    f"## {section_name}",
                    "",
                    "```",
                    extracted_data['prompts'][prompt_type],
                    "```",
                    ""
                ])
        
        # Add tools information
        if extracted_data['tools']:
            content.extend([
                "## Available Tools",
                "",
                "```json",
                json.dumps(extracted_data['tools'], indent=2),
                "```",
                ""
            ])
        
        # Add other documentation
        for key, doc_content in extracted_data['prompts'].items():
            if key not in ['main_prompt', 'agent_prompt', 'chat_prompt', 'memory_prompt']:
                section_name = key.replace('_', ' ').title()
                content.extend([
                    f"## {section_name}",
                    "",
                    doc_content,
                    ""
                ])
        
        return "\n".join(content)
    
    def _format_as_markdown(self, content: str, prompt_name: str, tool_name: str) -> str:
        """Format content as proper markdown"""
        
        formatted = [
            f"# {tool_name.title()} - {prompt_name.replace('_', ' ').title()}",
            "",
            f"**Source:** Extracted from comprehensive AI tools system prompts repository",
            f"**Tool:** {tool_name.title()}",
            f"**Type:** {prompt_name.replace('_', ' ').title()}",
            "",
            "---",
            "",
            content
        ]
        
        return "\n".join(formatted)
    
    def _create_enhanced_tool_configs(self):
        """Create enhanced tool configurations based on extracted data"""
        config_dir = Path("config/tools")
        config_dir.mkdir(exist_ok=True)
        
        for tool_name, data in self.processed_tools.items():
            config_path = config_dir / f"{tool_name}.yaml"
            
            # Create enhanced configuration
            config = self._generate_tool_config(tool_name, data)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            print(f"📝 Created enhanced config for {tool_name}")
    
    def _generate_tool_config(self, tool_name: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tool configuration based on extracted data"""
        
        # Analyze prompts to extract capabilities and strategies
        main_prompt = extracted_data['prompts'].get('main_prompt') or extracted_data['prompts'].get('agent_prompt', '')
        
        # Extract capabilities
        capabilities = self._extract_capabilities(main_prompt)
        use_cases = self._extract_use_cases(main_prompt)
        constraints = self._extract_constraints(main_prompt)
        
        # Determine development stages based on tool type
        stages = self._determine_stages(tool_name, main_prompt)
        components = self._determine_components(tool_name, main_prompt)
        
        config = {
            'tool_name': tool_name.title(),
            'format': self._determine_format(main_prompt),
            'tone': self._determine_tone(main_prompt),
            'framework': self._determine_framework(tool_name, main_prompt),
            'preferred_use_cases': use_cases,
            'prompting_strategies': self._extract_strategies(main_prompt),
            'development_stages': stages,
            'supported_components': components,
            'capabilities': capabilities,
            'constraints': constraints,
            'documentation_sources': [
                f"data/{tool_name}_docs/comprehensive_system_prompt.md"
            ],
            'extracted_metadata': {
                'source': 'comprehensive_ai_tools_repository',
                'files_processed': len(extracted_data['metadata']['files_processed']),
                'has_tools_config': bool(extracted_data['tools'])
            }
        }
        
        return config
    
    def _extract_capabilities(self, prompt: str) -> List[str]:
        """Extract capabilities from system prompt"""
        capabilities = []
        
        # Common capability patterns
        patterns = [
            r"You can (.*?)(?:\.|,|$)",
            r"able to (.*?)(?:\.|,|$)",
            r"supports? (.*?)(?:\.|,|$)",
            r"provides? (.*?)(?:\.|,|$)"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, prompt, re.IGNORECASE)
            capabilities.extend([match.strip() for match in matches if len(match.strip()) < 100])
        
        return list(set(capabilities))[:10]  # Limit to 10 most relevant
    
    def _extract_use_cases(self, prompt: str) -> List[str]:
        """Extract use cases from system prompt"""
        use_cases = []
        
        # Look for common use case indicators
        if 'web' in prompt.lower():
            use_cases.append('web_development')
        if 'mobile' in prompt.lower():
            use_cases.append('mobile_development')
        if 'code' in prompt.lower():
            use_cases.append('code_generation')
        if 'debug' in prompt.lower():
            use_cases.append('debugging')
        if 'test' in prompt.lower():
            use_cases.append('testing')
        if 'api' in prompt.lower():
            use_cases.append('api_integration')
        
        return use_cases
    
    def _extract_constraints(self, prompt: str) -> List[str]:
        """Extract constraints from system prompt"""
        constraints = []
        
        # Look for constraint patterns
        constraint_patterns = [
            r"cannot (.*?)(?:\.|,|$)",
            r"don't (.*?)(?:\.|,|$)", 
            r"must not (.*?)(?:\.|,|$)",
            r"limited to (.*?)(?:\.|,|$)",
            r"only (.*?)(?:\.|,|$)"
        ]
        
        for pattern in constraint_patterns:
            matches = re.findall(pattern, prompt, re.IGNORECASE)
            constraints.extend([match.strip() for match in matches if len(match.strip()) < 100])
        
        return list(set(constraints))[:8]  # Limit to 8 most relevant
    
    def _determine_stages(self, tool_name: str, prompt: str) -> List[str]:
        """Determine development stages based on tool type"""
        
        # Tool-specific stage mappings
        stage_mappings = {
            'cursor': ['analysis', 'coding', 'debugging', 'optimization'],
            'v0': ['design', 'component_creation', 'styling', 'testing'],
            'bolt': ['prototyping', 'development', 'enhancement', 'deployment'],
            'lovable': ['planning', 'architecture', 'implementation', 'integration', 'testing'],
            'devin': ['planning', 'implementation', 'testing', 'deployment', 'maintenance'],
            'windsurf': ['exploration', 'development', 'collaboration', 'optimization'],
            'replit': ['setup', 'coding', 'testing', 'deployment'],
            'vscode': ['coding', 'debugging', 'refactoring', 'testing'],
        }
        
        return stage_mappings.get(tool_name, ['planning', 'implementation', 'testing', 'deployment'])
    
    def _determine_components(self, tool_name: str, prompt: str) -> List[str]:
        """Determine supported components based on tool type"""
        
        component_mappings = {
            'cursor': ['code_files', 'functions', 'classes', 'modules'],
            'v0': ['ui_components', 'layouts', 'styling', 'interactions'],
            'bolt': ['web_apps', 'components', 'apis', 'databases'],
            'lovable': ['react_components', 'pages', 'apis', 'database_models'],
            'devin': ['full_applications', 'microservices', 'apis', 'databases'],
            'windsurf': ['collaborative_code', 'reviews', 'documentation'],
            'replit': ['scripts', 'applications', 'apis', 'databases'],
            'vscode': ['code_files', 'extensions', 'debugging_tools'],
        }
        
        return component_mappings.get(tool_name, ['code', 'documentation', 'tests'])
    
    def _determine_format(self, prompt: str) -> str:
        """Determine format based on prompt characteristics"""
        if 'structured' in prompt.lower():
            return 'structured_prompts'
        elif 'conversational' in prompt.lower():
            return 'conversational'
        elif 'command' in prompt.lower():
            return 'command_based'
        else:
            return 'natural_language'
    
    def _determine_tone(self, prompt: str) -> str:
        """Determine tone based on prompt characteristics"""
        if 'expert' in prompt.lower():
            return 'expert_technical'
        elif 'friendly' in prompt.lower():
            return 'friendly_helpful'
        elif 'professional' in prompt.lower():
            return 'professional'
        else:
            return 'balanced_technical'
    
    def _determine_framework(self, tool_name: str, prompt: str) -> str:
        """Determine framework based on tool and prompt"""
        
        frameworks = {
            'cursor': 'Agentic AI pair programming with Claude integration',
            'v0': 'Component-driven UI generation with Next.js',
            'bolt': 'WebContainer-based full-stack development',
            'lovable': 'React/TypeScript web application development',
            'devin': 'Autonomous software engineering',
            'windsurf': 'Collaborative AI-assisted development',
            'replit': 'Cloud-based development environment',
            'vscode': 'Integrated development with Copilot assistance',
        }
        
        return frameworks.get(tool_name, 'AI-assisted development')
    
    def _extract_strategies(self, prompt: str) -> Dict[str, Any]:
        """Extract prompting strategies from system prompt"""
        
        strategies = {}
        
        # Default strategy based on prompt content
        if 'step' in prompt.lower() and 'by' in prompt.lower():
            strategies['step_by_step'] = {
                'template': 'Step 1: {analysis} Step 2: {implementation} Step 3: {validation}',
                'use_cases': ['complex_tasks', 'debugging'],
                'effectiveness_score': 0.9
            }
        
        if 'tool' in prompt.lower() and 'call' in prompt.lower():
            strategies['tool_based'] = {
                'template': 'Use {tool_name} to {action} for {objective}',
                'use_cases': ['automated_tasks', 'integrations'],
                'effectiveness_score': 0.85
            }
        
        if 'context' in prompt.lower():
            strategies['context_aware'] = {
                'template': 'Given context: {context}, implement {requirement} ensuring {constraints}',
                'use_cases': ['contextual_development', 'adaptive_solutions'],
                'effectiveness_score': 0.8
            }
        
        return strategies
    
    def _update_existing_documentation(self):
        """Update existing documentation with new comprehensive data"""
        print("📚 Updating existing documentation...")
        
        # Update existing tool docs that were enhanced
        existing_tools = ['lovable', 'bolt', 'cursor', 'v0']
        
        for tool in existing_tools:
            existing_dir = self.target_data_dir / f"{tool}_docs"
            if existing_dir.exists() and tool in self.processed_tools:
                # Add comprehensive system prompt
                new_data = self.processed_tools[tool]
                if new_data['prompts']:
                    comprehensive_guide = self._create_comprehensive_guide(tool, new_data)
                    
                    with open(existing_dir / "comprehensive_system_prompt.md", 'w', encoding='utf-8') as f:
                        f.write(comprehensive_guide)
                    
                    print(f"📝 Enhanced {tool} with comprehensive system prompts")
    
    def _print_integration_summary(self):
        """Print integration summary"""
        print("\n" + "="*60)
        print("🎉 AI TOOLS DATA INTEGRATION SUMMARY")
        print("="*60)
        
        print(f"✅ Total tools processed: {len(self.processed_tools)}")
        print(f"📁 Data directories created: {len(list(self.target_data_dir.glob('*_docs')))}")
        print(f"⚙️  Configuration files created: {len(list(Path('config/tools').glob('*.yaml')))}")
        
        print("\n📊 Tools with comprehensive data:")
        for tool_name, data in self.processed_tools.items():
            prompt_count = len(data['prompts'])
            tool_count = len(data['tools'])
            print(f"  • {tool_name.title()}: {prompt_count} prompts, {tool_count} tool configs")
        
        print(f"\n🚀 Enhanced RAG system now supports {len(self.processed_tools)} AI tools!")
        print("   Run the enhanced Streamlit app to see the improvements.")
        print("="*60)

if __name__ == "__main__":
    integrator = AIToolsDataIntegrator()
    integrator.extract_and_integrate_all_tools()
