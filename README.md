# RAG Prompt Generator

A Flask web application for generating optimized prompts for various AI development tools including Lovable.dev, Bolt.new, Cursor, v0, and many others using RAG (Retrieval-Augmented Generation) with Google Gemini embeddings.

**Created by Ganesh Tappiti**

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
# Run setup script to install dependencies
python scripts/setup.py

# Start development server
python scripts/server.py --mode dev
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env
# Edit .env and add your Google API key

# Start development server
python scripts/server.py --mode dev

# Or use batch/PowerShell scripts
start_server.bat           # Windows Batch
start_server.ps1          # PowerShell
```

### Option 3: Production Mode
```bash
# Start production server
python scripts/server.py --mode prod --host 0.0.0.0 --port 8000
```

## 📁 Project Structure

```
rag-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── azure.yaml            # Azure deployment configuration
├── README.md             # This file
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore patterns
│
├── src/                  # Source code
│   ├── core/            # Core type definitions and utilities
│   │   ├── types.py     # Enhanced type definitions
│   │   └── shared_types.py  # Legacy shared types
│   ├── generators/      # Prompt generation engines
│   │   ├── enhanced_generator.py  # Main enhanced generator
│   │   ├── basic_generator.py     # Legacy basic generator
│   │   ├── build_prompt.py       # Prompt building utilities
│   │   └── llm_generator.py      # LLM integration
│   └── utils/           # Utility functions
│
├── static/              # Static web assets (CSS, JS, images)
├── templates/           # HTML templates
├── data/               # Documentation and data indices
├── storage/            # Database storage (ChromaDB)
├── chroma_*/           # ChromaDB instances
│
├── scripts/            # Utility scripts
│   ├── server.py       # Unified server launcher
│   └── setup.py        # Setup and installation script
│
└── tests/              # Test suite
    ├── __init__.py
    └── test_app.py     # Main test file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```bash
# Required: Google Gemini API Key
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional: Flask settings
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secret_key_here
```

### Dependencies

The application requires Python 3.8+ and the following packages:
- Flask (web framework)
- ChromaDB (vector database)
- LangChain + Google Gemini (AI/embeddings)
- Additional dependencies in `requirements.txt`

## 🌐 Usage

1. **Access the web interface**: http://127.0.0.1:5000
2. **Select an AI tool** from the supported tools list
3. **Enter your project details** and requirements
4. **Generate optimized prompts** for your selected tool
5. **Copy and use** the generated prompts in your AI tool

### Supported AI Tools
- Lovable.dev, Bolt.new, Cursor, v0
- Replit, CodeSandbox, StackBlitz
- And many more...

## 🧪 Testing

```bash
# Run tests
python tests/test_app.py

# Test specific functionality
python -m pytest tests/
```

## 🐳 Docker Support

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "scripts/server.py", "--mode", "prod"]
```

## 🔧 Development

### Server Options
```bash
# Development mode (auto-reload, debug)
python scripts/server.py --mode dev

# Production mode
python scripts/server.py --mode prod

# Custom host/port
python scripts/server.py --host 0.0.0.0 --port 8080

# Install dependencies
python scripts/server.py --install-deps
```

### Project Management
- Use `scripts/setup.py` for initial setup
- Use `scripts/server.py` for all server operations
- Keep source code in `src/` directory
- Store tests in `tests/` directory

## 📝 API Documentation

The Flask application provides a web interface with the following main routes:
- `/` - Main application interface
- `/generate` - Prompt generation endpoint
- `/tools` - Supported tools information

## 🚀 Deployment

### Azure Deployment
The project includes `azure.yaml` for Azure deployment:
```bash
az webapp up --name your-app-name
```

### Manual Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables
3. Run: `python scripts/server.py --mode prod`

## 🛠️ Troubleshooting

### Common Issues
1. **Import Errors**: Run `python scripts/setup.py` to install dependencies
2. **Port Conflicts**: Use `--port` flag to specify different port
3. **Windows Socket Errors**: Use the provided batch/PowerShell scripts

### Getting Help
- Check the test suite: `python tests/test_app.py`
- Review logs for error details
- Ensure all dependencies are installed

## 📄 License

This project is created by Ganesh Tappiti. Please check with the author for licensing terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python tests/test_app.py`
5. Submit a pull request

---

For more detailed information, check the source code documentation in the `src/` directory.
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
