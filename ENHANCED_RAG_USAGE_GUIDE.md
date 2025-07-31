# Enhanced RAG System with AI Tools Documentation - Usage Guide

Generated on: 2025-07-31 18:00:16

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
- **Database Path:** `C:\Users\2005g\Downloads\RAG\storage\chroma_ai_tools`
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
    path="C:\Users\2005g\Downloads\RAG\storage\chroma_ai_tools",
    settings=Settings(anonymized_telemetry=False)
)
collection = client.get_collection("ai_tools_documentation")

# Query for specific information
results = collection.query(
    query_texts=["React component generation best practices"],
    n_results=5,
    where={"tool_name": "lovable"}  # Filter by specific tool
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
