#!/usr/bin/env python3
"""
Final validation and usage guide for the enhanced RAG system 
with AI tools documentation.

This script validates the integration and provides usage examples.

Author: Ganesh Tappiti
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import sys
from datetime import datetime

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    print("ChromaDB not installed. Please run: pip install chromadb")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGSystemValidator:
    def __init__(self, base_dir: str):
        """Initialize the validator."""
        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / "data"
        self.config_dir = self.base_dir / "config"
        self.storage_dir = self.base_dir / "storage"
        
        # Initialize ChromaDB client
        self.db_path = self.storage_dir / "chroma_ai_tools"
        if self.db_path.exists():
            self.client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(anonymized_telemetry=False)
            )
            try:
                self.collection = self.client.get_collection("ai_tools_documentation")
            except:
                self.collection = None
        else:
            self.client = None
            self.collection = None
    
    def validate_file_structure(self) -> Dict[str, bool]:
        """Validate that all required files and directories exist."""
        validation_results = {}
        
        # Check main directories
        required_dirs = [
            self.data_dir,
            self.config_dir / "tools",
            self.storage_dir,
            self.base_dir / "external_ai_tools_data"
        ]
        
        for dir_path in required_dirs:
            validation_results[f"Directory: {dir_path.name}"] = dir_path.exists()
        
        # Check key files
        required_files = [
            self.data_dir / "ai_tools_index.json",
            self.data_dir / "extraction_summary.md",
            self.data_dir / "integration_summary.md",
            self.data_dir / "comprehensive_documentation_index.json",
            self.data_dir / "database_update_summary.md"
        ]
        
        for file_path in required_files:
            validation_results[f"File: {file_path.name}"] = file_path.exists()
        
        # Check database
        validation_results["ChromaDB Database"] = (
            self.client is not None and 
            self.collection is not None
        )
        
        return validation_results
    
    def validate_tool_configurations(self) -> Dict[str, Dict[str, Any]]:
        """Validate tool configuration files."""
        tools_dir = self.config_dir / "tools"
        results = {}
        
        if not tools_dir.exists():
            return {"error": {"message": "Tools configuration directory not found"}}
        
        for config_file in tools_dir.glob("*.yaml"):
            tool_name = config_file.stem
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic validation
                has_name = "name:" in content
                has_description = "description:" in content
                has_documentation = "documentation:" in content
                
                results[tool_name] = {
                    "file_exists": True,
                    "has_name": has_name,
                    "has_description": has_description,
                    "has_documentation": has_documentation,
                    "valid": has_name and has_description and has_documentation
                }
                
            except Exception as e:
                results[tool_name] = {
                    "file_exists": True,
                    "error": str(e),
                    "valid": False
                }
        
        return results
    
    def test_database_queries(self) -> Dict[str, Any]:
        """Test database functionality with various queries."""
        if not self.collection:
            return {"error": "Database collection not available"}
        
        test_results = {}
        
        # Test queries for different use cases
        test_queries = {
            "react_development": "How to create React components with modern frameworks",
            "code_generation": "AI code generation best practices and prompts",
            "debugging": "Debugging tools and techniques for development",
            "web_development": "Web development tools and frameworks",
            "ai_agents": "AI agent capabilities and system prompts",
            "typescript": "TypeScript development and type safety",
            "testing": "Testing strategies and tools for software development",
            "deployment": "Deployment and production best practices"
        }
        
        for query_name, query_text in test_queries.items():
            try:
                results = self.collection.query(
                    query_texts=[query_text],
                    n_results=5
                )
                
                if results and 'documents' in results and results['documents']:
                    docs = results['documents'][0]
                    metadatas_list = results.get('metadatas', [[]])
                    metadatas = metadatas_list[0] if metadatas_list else []
                    
                    # Analyze results
                    tool_coverage = set()
                    file_types = set()
                    
                    for metadata in metadatas:
                        if isinstance(metadata, dict):
                            tool_coverage.add(metadata.get('tool_name', 'unknown'))
                            file_types.add(metadata.get('file_type', 'unknown'))
                    
                    test_results[query_name] = {
                        "success": True,
                        "result_count": len(docs),
                        "tools_covered": list(tool_coverage),
                        "file_types": list(file_types),
                        "sample_result": docs[0][:200] + "..." if docs else None
                    }
                else:
                    test_results[query_name] = {
                        "success": False,
                        "error": "No results found"
                    }
                    
            except Exception as e:
                test_results[query_name] = {
                    "success": False,
                    "error": str(e)
                }
        
        return test_results
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        stats = {}
        
        # Load tools index
        try:
            with open(self.data_dir / "ai_tools_index.json", 'r', encoding='utf-8') as f:
                tools_index = json.load(f)
                
            stats["tools"] = {
                "total_tools": len(tools_index.get("tools", {})),
                "total_files": sum(
                    tool.get("file_count", 0) 
                    for tool in tools_index.get("tools", {}).values()
                ),
                "extraction_date": tools_index.get("extraction_date"),
                "source_repository": tools_index.get("source_repository")
            }
            
        except Exception as e:
            stats["tools"] = {"error": str(e)}
        
        # Database statistics
        if self.collection:
            try:
                collection_count = self.collection.count()
                stats["database"] = {
                    "total_documents": collection_count,
                    "database_path": str(self.db_path),
                    "collection_name": "ai_tools_documentation"
                }
            except Exception as e:
                stats["database"] = {"error": str(e)}
        else:
            stats["database"] = {"error": "Database not available"}
        
        # Configuration files
        tools_dir = self.config_dir / "tools"
        if tools_dir.exists():
            config_files = list(tools_dir.glob("*.yaml"))
            stats["configurations"] = {
                "total_configs": len(config_files),
                "config_files": [f.stem for f in config_files]
            }
        else:
            stats["configurations"] = {"error": "Configuration directory not found"}
        
        return stats
    
    def create_usage_guide(self) -> str:
        """Create a comprehensive usage guide."""
        guide_content = f"""# Enhanced RAG System with AI Tools Documentation - Usage Guide

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This Enhanced RAG (Retrieval-Augmented Generation) system now includes comprehensive documentation for 21+ AI development tools, providing you with access to system prompts, best practices, and tool-specific guidance for generating optimized prompts.

## 🚀 Quick Start

### 1. Basic Usage
```bash
# Run the main Streamlit application
streamlit run src/apps/streamlit_app.py

# Or run the Gemini-powered version
streamlit run src/apps/streamlit_app_gemini.py
```

### 2. Available AI Tools

The system now includes documentation for:

**Code Generators:**
- Lovable.dev - AI-powered web application builder
- v0 by Vercel - AI interface designer  
- Bolt.new - Full-stack application generator

**IDEs & Editors:**
- Cursor - AI-powered code editor
- VS Code Agent - AI assistant for Visual Studio Code
- Windsurf - AI-powered development environment

**AI Agents:**
- Devin AI - Autonomous software engineer
- Manus Agent - Advanced AI coding assistant
- Trae - AI development assistant

**Development Platforms:**
- Replit - Cloud-based collaborative IDE
- Same.dev - AI-powered development platform
- Orchids.app - Application development platform

**And many more...**

## 📊 Database Information

The system uses ChromaDB for efficient document retrieval with:
- **Database Path:** `{self.db_path}`
- **Collection:** `ai_tools_documentation`
- **Documents:** Chunked for optimal embedding and retrieval

## 🔧 Advanced Usage

### 1. Custom Queries

You can query specific tool documentation:

```python
import chromadb
from chromadb.config import Settings

# Connect to database
client = chromadb.PersistentClient(
    path="{self.db_path}",
    settings=Settings(anonymized_telemetry=False)
)
collection = client.get_collection("ai_tools_documentation")

# Query for specific information
results = collection.query(
    query_texts=["React component generation best practices"],
    n_results=5,
    where={{"tool_name": "lovable"}}  # Filter by specific tool
)
```

### 2. Tool-Specific Configurations

Each tool has a YAML configuration file in `config/tools/` with:
- Tool metadata and descriptions
- Supported languages and frameworks
- Key features and capabilities
- Documentation file references

### 3. Prompt Generation Workflows

The system supports multiple prompt generation workflows:

1. **Tool-Specific Prompts:** Generate prompts optimized for specific AI tools
2. **Multi-Tool Comparison:** Compare approaches across different tools
3. **Best Practice Integration:** Incorporate proven patterns and practices
4. **Context-Aware Generation:** Leverage relevant documentation based on your needs

## 📁 File Structure

```
├── data/
│   ├── lovable_docs/          # Lovable.dev documentation
│   ├── cursor_docs/           # Cursor IDE documentation  
│   ├── v0_docs/              # v0 by Vercel documentation
│   ├── devin_docs/           # Devin AI documentation
│   ├── replit_docs/          # Replit documentation
│   ├── [other tool docs]/    # Additional tool documentation
│   ├── ai_tools_index.json   # Master index of all tools
│   └── *.md                  # Summary and status files
├── config/
│   └── tools/
│       ├── lovable.yaml      # Tool-specific configurations
│       ├── cursor.yaml
│       └── [other tools].yaml
├── storage/
│   └── chroma_ai_tools/      # ChromaDB database
└── external_ai_tools_data/   # Source documentation from GitHub
```

## 🎯 Use Cases

### 1. Web Development
Query for React, Vue, or Angular development practices:
```
"How to create responsive web components with modern frameworks"
```

### 2. AI Agent Development  
Find patterns for building AI agents:
```
"AI agent system prompts and interaction patterns"
```

### 3. Code Generation
Discover code generation best practices:
```
"Automated code generation strategies and templates"
```

### 4. Debugging & Testing
Get debugging and testing guidance:
```
"Debugging tools and testing strategies for development"
```

## 🔍 Search Tips

1. **Be Specific:** Include tool names, technologies, or specific features
2. **Use Context:** Mention your development context (web, mobile, backend)
3. **Combine Terms:** Use multiple relevant keywords for better results
4. **Filter by Tool:** Use metadata filters to focus on specific tools

## 🛠️ Maintenance

### Updating Documentation
To update with new AI tools documentation:

1. Add new documentation to `external_ai_tools_data/`
2. Run extraction: `python extract_ai_tools_documentation.py`
3. Run integration: `python integrate_ai_tools.py`  
4. Update database: `python update_rag_database.py`

### Database Management
- Database files are stored in `storage/chroma_ai_tools/`
- Backup regularly for data preservation
- Monitor database size and performance

## 📈 Performance Tips

1. **Chunking:** Large documents are automatically chunked for better retrieval
2. **Caching:** Results are cached for improved response times
3. **Indexing:** Documents are embedded and indexed for semantic search
4. **Filtering:** Use metadata filters to narrow search scope

## 🔗 Integration

The system integrates with:
- **Streamlit:** Web interface for interactive usage
- **ChromaDB:** Vector database for semantic search
- **Multiple AI APIs:** Support for various AI providers
- **YAML Configuration:** Flexible tool configuration system

## 📞 Support

For issues or questions:
1. Check the validation results below
2. Review log files for error details
3. Ensure all dependencies are installed
4. Verify file permissions and paths

---

*This guide is automatically generated based on your current system configuration.*
"""
        return guide_content
    
    def run_validation(self):
        """Run complete system validation."""
        logger.info("Starting system validation...")
        
        print("\n" + "="*80)
        print("🔍 ENHANCED RAG SYSTEM VALIDATION")
        print("="*80)
        
        # File structure validation
        print("\n📁 File Structure Validation:")
        file_results = self.validate_file_structure()
        for item, status in file_results.items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {item}")
        
        # Configuration validation  
        print("\n⚙️ Tool Configuration Validation:")
        config_results = self.validate_tool_configurations()
        if "error" in config_results:
            print(f"  ❌ {config_results['error']}")
        else:
            valid_configs = sum(1 for result in config_results.values() if result.get('valid', False))
            total_configs = len(config_results)
            print(f"  ✅ {valid_configs}/{total_configs} configurations valid")
            
            for tool_name, result in config_results.items():
                if not result.get('valid', False):
                    print(f"    ⚠️ {tool_name}: {result.get('error', 'Invalid configuration')}")
        
        # Database testing
        print("\n🗄️ Database Functionality Test:")
        if self.collection:
            query_results = self.test_database_queries()
            successful_queries = sum(1 for result in query_results.values() if result.get('success', False))
            total_queries = len(query_results)
            print(f"  ✅ {successful_queries}/{total_queries} test queries successful")
            
            for query_name, result in query_results.items():
                if result.get('success'):
                    tools = result.get('tools_covered', [])
                    print(f"    ✅ {query_name}: {result['result_count']} results from {len(tools)} tools")
                else:
                    print(f"    ❌ {query_name}: {result.get('error', 'Unknown error')}")
        else:
            print("  ❌ Database not available")
        
        # System statistics
        print("\n📊 System Statistics:")
        stats = self.get_system_statistics()
        
        if "tools" in stats and "error" not in stats["tools"]:
            tools_stats = stats["tools"]
            print(f"  📚 Tools: {tools_stats['total_tools']} tools, {tools_stats['total_files']} files")
            
        if "database" in stats and "error" not in stats["database"]:
            db_stats = stats["database"]
            print(f"  🗃️ Database: {db_stats['total_documents']} documents indexed")
            
        if "configurations" in stats and "error" not in stats["configurations"]:
            config_stats = stats["configurations"]
            print(f"  ⚙️ Configurations: {config_stats['total_configs']} tool configs")
        
        # Create usage guide
        print("\n📖 Creating Usage Guide...")
        usage_guide = self.create_usage_guide()
        guide_path = self.base_dir / "ENHANCED_RAG_USAGE_GUIDE.md"
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(usage_guide)
        
        print(f"  ✅ Usage guide created: {guide_path}")
        
        print("\n" + "="*80)
        print("🎉 VALIDATION COMPLETED!")
        print("="*80)
        print("Your Enhanced RAG System with AI Tools Documentation is ready!")
        print(f"📖 Usage Guide: {guide_path}")
        print("🚀 Start the system: streamlit run src/apps/streamlit_app.py")
        print("="*80)


def main():
    """Main execution function."""
    base_dir = Path(__file__).parent
    validator = RAGSystemValidator(str(base_dir))
    
    try:
        validator.run_validation()
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise


if __name__ == "__main__":
    main()
