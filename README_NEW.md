# Enhanced Multi-Tool RAG Prompt Generator

A comprehensive system for generating optimized prompts for various AI development tools including Lovable.dev, Bolt.new, Cursor, v0, and many others.

Created by **Ganesh Tappiti** and Enhanced RAG Team

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the enhanced Streamlit app
streamlit run src/apps/streamlit_app.py

# Or run the Gemini version
streamlit run src/apps/streamlit_app_gemini.py
```

## 📁 Project Structure

```
├── src/                          # Source code
│   ├── core/                     # Core type definitions and utilities
│   │   ├── types.py             # Enhanced type definitions
│   │   └── shared_types.py      # Legacy shared types
│   ├── generators/              # Prompt generation engines
│   │   ├── enhanced_generator.py # Main enhanced generator
│   │   ├── basic_generator.py   # Legacy basic generator
│   │   ├── build_prompt.py      # Prompt building utilities
│   │   └── generate_prompt*.py  # Generation modules
│   ├── database/                # Database and embedding operations
│   │   ├── create_database*.py  # Database creation modules
│   │   ├── query_data*.py       # Data querying modules
│   │   └── compare_embeddings*.py # Embedding comparison
│   └── apps/                    # User interfaces and applications
│       ├── streamlit_app*.py    # Streamlit web applications
│       └── demo_prompt_generator*.py # Demo applications
├── config/                      # Configuration files
│   └── tools/                   # Tool-specific configurations
│       ├── lovable.yaml        # Lovable.dev configuration
│       ├── bolt.yaml           # Bolt.new configuration
│       ├── cursor.yaml         # Cursor IDE configuration
│       ├── v0.yaml             # v0 by Vercel configuration
│       └── *.yaml              # Other tool configurations
├── docs/                        # Documentation
│   ├── guides/                  # User guides and tutorials
│   │   ├── ENHANCED_PROMPTING_GUIDE.md
│   │   ├── SETUP_GUIDE*.md
│   │   └── DATA_UPLOAD_GUIDE.md
│   ├── INTEGRATION_SUMMARY.md   # Integration documentation
│   └── FINAL_INTEGRATION_SUMMARY.md
├── data/                        # Training data and documentation
│   ├── lovable_docs/           # Lovable.dev documentation
│   ├── bubble_docs/            # Bubble.io documentation
│   ├── adalo_docs/             # Adalo documentation
│   └── */                      # Other tool documentation
├── templates/                   # Prompt templates
│   ├── lovable_task_template.md
│   ├── stage_*.md              # Stage-specific templates
│   └── */
├── storage/                     # Data storage
│   └── chroma_gemini/          # ChromaDB storage
├── tests/                       # Test files (to be added)
├── scripts/                     # Utility scripts (to be added)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🛠️ Core Components

### Enhanced Generator (`src/generators/enhanced_generator.py`)
The main prompt generation engine that:
- Supports 15+ AI development tools
- Implements tool-specific optimization strategies
- Uses advanced prompting techniques (C.L.E.A.R. framework, meta-prompting)
- Provides quality scoring and validation

### Type System (`src/core/types.py`)
Comprehensive type definitions including:
- `PromptStage`: Development stage enumeration
- `SupportedTool`: All supported AI tools
- `TaskContext`: Enhanced context for tasks
- `ToolProfile`: Tool-specific configurations
- `PromptingStrategy`: Strategy definitions

### Database Operations (`src/database/`)
ChromaDB integration for:
- Document embedding and storage
- Semantic search and retrieval
- Multi-model support (OpenAI, Gemini)
- Embedding comparison and optimization

## 🎯 Supported Tools

- **Lovable.dev**: React/TypeScript with C.L.E.A.R. framework
- **Bolt.new**: Enhancement-driven development with WebContainer
- **Cursor**: Schema-driven development with parallel processing
- **v0 by Vercel**: Production-ready React components
- **Cline**: Step-by-step iterative development
- **Devin AI**: Autonomous planning with security focus
- **Windsurf**: Explanatory development with async handling
- **And many more...**

## 🚀 Usage Examples

### Basic Usage
```python
from src import EnhancedMultiToolGenerator, SupportedTool, PromptStage, TaskContext

# Create task context
context = TaskContext(
    task_type="web_application",
    project_name="Task Manager",
    description="A productivity app for small teams",
    stage=PromptStage.APP_SKELETON,
    target_tool=SupportedTool.LOVABLE
)

# Generate optimized prompt
generator = EnhancedMultiToolGenerator()
result = generator.generate_enhanced_prompt(context)
print(result.optimized_prompt)
```

### Advanced Usage with Multiple Tools
```python
# Compare strategies across tools
tools = [SupportedTool.LOVABLE, SupportedTool.CURSOR, SupportedTool.V0]
results = {}

for tool in tools:
    context.target_tool = tool
    result = generator.generate_enhanced_prompt(context)
    results[tool.value] = result

# Choose best strategy based on confidence score
best_tool = max(results, key=lambda k: results[k].confidence_score)
```

## 🧪 Running Applications

### Streamlit Web Interface
```bash
# Enhanced version with all tools
streamlit run src/apps/streamlit_app.py

# Gemini-optimized version
streamlit run src/apps/streamlit_app_gemini.py
```

### Demo Applications
```bash
# Basic prompt generator demo
python src/apps/demo_prompt_generator.py

# Gemini-enhanced demo
python src/apps/demo_prompt_generator_gemini.py
```

## 📊 Configuration

### Tool Configuration
Each tool has its own YAML configuration in `config/tools/`:
- Prompting strategies
- Optimization tips
- Constraints and limitations
- Examples and best practices

### Environment Setup
```bash
# Copy example environment file
cp .env.example .env

# Edit with your API keys
# OPENAI_API_KEY=your_openai_key
# GOOGLE_API_KEY=your_gemini_key
```

## 🤝 Contributing

1. Follow the established project structure
2. Add tests in the `tests/` directory
3. Update documentation in `docs/`
4. Follow Python best practices and type hints

## 📈 Performance

- Supports multiple embedding models (OpenAI, Gemini)
- Optimized ChromaDB operations
- Caching for repeated queries
- Parallel processing for independent operations

## 🔧 Development

### Setting up Development Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests (when available)
pytest tests/
```

### Adding New Tools
1. Create YAML configuration in `config/tools/`
2. Add tool enum to `src/core/types.py`
3. Implement tool-specific strategies
4. Update documentation

## 📚 Documentation

- **User Guides**: `docs/guides/` - Comprehensive usage guides
- **API Documentation**: `docs/api/` - Technical API reference
- **Integration Guides**: `docs/` - Tool integration documentation

## 🎯 Roadmap

- [ ] Add comprehensive test suite
- [ ] Implement CLI interface
- [ ] Add more AI development tools
- [ ] Performance optimization
- [ ] Advanced analytics and metrics
- [ ] Plugin architecture for custom tools

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Lovable.dev for the C.L.E.A.R. framework inspiration
- Bolt.new for enhancement-driven development patterns
- Open source AI tools community for best practices
- System prompts repository contributors
