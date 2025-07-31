# Enhanced Multi-Tool Prompt Generator 🛠️

A powerful RAG-powered Streamlit application that generates tool-specific prompts for various no-code/low-code development tools with stage-wise development support.

## 🌟 Key Features

### ✅ Tool-Specific Metadata Embedding
- Each tool has dedicated configuration files with metadata
- Documentation is tagged during indexing with tool, stage, and component information
- RAG retrieval is filtered by tool and context for precise results

### ✅ Modular Templates  
- Individual YAML configurations for each tool (lovable.yaml, bolt.yaml, bubble.yaml, etc.)
- Tool-specific prompting strategies and frameworks
- Customizable development stages and supported components

### ✅ Enhanced RAG Core
- Filtered semantic search by tool, document type, and stage
- Tool-specific documentation retrieval and contextualization
- Intelligent prompt generation based on tool capabilities

### ✅ Structured Generation Loop
- Iterative prompt building through development stages
- Page-wise and component-wise prompt generation
- Stage-specific instructions and best practices

## 🛠️ Supported Tools

The system currently supports **12 no-code/low-code tools**:

| Tool | Focus Area | Stages | Components |
|------|------------|--------|------------|
| **Lovable.dev** | React/TypeScript Web Apps | 8 stages | UI, Forms, Auth, API |
| **Bolt.new** | Web Applications | 6 stages | Components, Modules, Styling |
| **Bubble** | Full-stack Web Apps | 6 stages | Data, Workflows, UI, APIs |
| **FlutterFlow** | Mobile Applications | - | Mobile UI, Navigation |
| **Framer** | Design & Prototyping | - | Components, Interactions |
| **Adalo** | Mobile Apps | - | Mobile Components |
| **Uizard** | UI Design | - | Design Elements |
| **V0** | UI Generation | - | React Components |
| **Cursor** | AI Code Editor | - | Code Generation |
| **Cline** | AI Assistant | - | Development Aid |
| **Devin** | AI Software Engineer | - | Full Development |
| **Windsurf** | Development Environment | - | Code Environment |

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd RAG

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Initialize Vector Database

```bash
# Run the basic test to ensure everything works
python test_basic_functionality.py

# For full RAG functionality, run:
python test_enhanced_generator.py
```

### 4. Launch the Enhanced App

```bash
# Run the enhanced Streamlit app
streamlit run src/apps/streamlit_app_enhanced.py
```

## 📖 How to Use

### 1. **Select Your Tool**
- Choose from 12 available no-code/low-code tools
- View tool-specific information, stages, and components
- Get tool-specific task suggestions

### 2. **Choose Development Stage**
- Select the current development stage (planning, implementation, testing, etc.)
- Each tool has customized stages based on its workflow
- Stage-specific instructions and best practices are included

### 3. **Define Your Project**
- Enter project details (name, description, tech stack)
- Specify task type and detailed description
- Add technical requirements, UI/UX needs, and constraints

### 4. **Generate Stage-Specific Prompts**
- Click "Generate Prompt" for tool and stage-specific results
- View formatted prompt with relevant documentation context
- Validate prompt quality with built-in scoring

### 5. **Export and Use**
- Export in Markdown, JSON, or Plain Text formats
- Include metadata for tracking and reuse
- Copy directly to your chosen development tool

## 🏗️ Architecture

### Core Components

```
src/
├── generators/
│   ├── tool_specific_generator.py    # Enhanced RAG generator
│   └── build_prompt.py              # Original Lovable generator
├── apps/
│   ├── streamlit_app_enhanced.py     # New multi-tool interface
│   └── streamlit_app.py              # Original interface
└── core/
    ├── types.py                      # Data structures
    └── shared_types.py               # Common types
```

### Configuration Structure

```
config/tools/
├── lovable.yaml          # Lovable.dev configuration
├── bolt.yaml            # Bolt.new configuration
├── bubble.yaml          # Bubble configuration
├── flutterflow.yaml     # FlutterFlow configuration
└── ...                  # Other tool configurations
```

### Documentation Database

```
data/
├── lovable_docs/        # Lovable.dev documentation
├── bubble_docs/         # Bubble documentation
├── flutterflow_docs/    # FlutterFlow documentation
├── framer_docs/         # Framer documentation
└── ...                  # Other tool documentation
```

## 🎯 Tool Configuration Format

Each tool configuration includes:

```yaml
tool_name: "Tool Name"
format: "prompt_format"
tone: "communication_tone"  
framework: "development_framework"

preferred_use_cases:
  - use_case_1
  - use_case_2

prompting_strategies:
  strategy_name:
    template: "prompt_template"
    use_cases: ["when_to_use"]
    effectiveness_score: 0.9

development_stages:
  - stage_1
  - stage_2

supported_components:
  - component_1
  - component_2
```

## 📊 Advanced Features

### **Intelligent RAG Retrieval**
- Tool-specific document filtering
- Stage-aware context retrieval  
- Component-focused documentation

### **Prompt Validation**
- Quality scoring (0-100)
- Tool-specific validation rules
- Improvement suggestions

### **Batch Generation** (Coming Soon)
- Generate prompts for all stages
- Multi-stage development workflows
- Template-based generation

### **Tool Comparison** (Coming Soon)
- Compare tools for your project type
- Feature compatibility analysis
- Recommendation engine

## 🔧 Customization

### Adding New Tools

1. **Create tool configuration:**
```bash
# Add config/tools/new_tool.yaml
cp config/tools/lovable.yaml config/tools/new_tool.yaml
# Edit with tool-specific settings
```

2. **Add documentation:**
```bash
# Create data/new_tool_docs/
mkdir data/new_tool_docs
# Add .md files with tool documentation
```

3. **Update generator:**
The system automatically detects new tools and documentation.

### Customizing Stages

Edit the `development_stages` section in tool YAML files:

```yaml
development_stages:
  - "custom_stage_1"
  - "custom_stage_2" 
  - "custom_stage_3"
```

### Adding Components

Edit the `supported_components` section:

```yaml
supported_components:
  - "custom_component_1"
  - "custom_component_2"
```

## 🧪 Testing

```bash
# Test tool configurations
python test_basic_functionality.py

# Test full RAG functionality (requires OpenAI API key)
python test_enhanced_generator.py

# Test specific tools
python -c "
from src.generators.tool_specific_generator import ToolSpecificPromptGenerator
gen = ToolSpecificPromptGenerator()
print('Available tools:', gen.get_available_tools())
"
```

## 📈 Performance Tips

1. **Vector Database**: Pre-built database loads faster than creating new embeddings
2. **API Usage**: RAG retrieval uses OpenAI embeddings - consider usage limits
3. **Documentation**: More comprehensive docs = better prompt quality
4. **Tool Selection**: Choose tools based on your specific use case

## 🤝 Contributing

1. Fork the repository
2. Add new tool configurations in `config/tools/`
3. Add corresponding documentation in `data/tool_docs/`
4. Test with `test_basic_functionality.py`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

- **Issues**: Report bugs and feature requests via GitHub issues
- **Documentation**: Check the `docs/` folder for detailed guides
- **Examples**: See example prompts in tool configuration files

---

**Built with ❤️ for the no-code/low-code development community**

*Generate better prompts, build better applications!* 🚀
