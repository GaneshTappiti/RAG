# Lovable.dev Prompt Generator with RAG

A comprehensive Retrieval-Augmented Generation (RAG) system for generating optimized prompts for Lovable.dev. This system uses vector embeddings to retrieve relevant context from Lovable.dev documentation and best practices to create highly effective, context-aware prompts.

## 🌟 Features

- **RAG-Powered Context Retrieval**: Automatically retrieves relevant documentation snippets
- **Template-Based Generation**: Uses Jinja2 templates for consistent, structured prompts
- **Multi-Interface Support**: CLI, Streamlit web interface, and Python API
- **Prompt Validation**: Built-in validation with scoring and suggestions
- **Category-Based Retrieval**: Optimized retrieval for different task types
- **Export Options**: Multiple export formats (Markdown, JSON, Plain Text)

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Web Interface](#web-interface)
  - [Python API](#python-api)
- [Configuration](#configuration)
- [Documentation Structure](#documentation-structure)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for embeddings)

### Setup

1. **Clone or download the repository**:
   ```bash
   git clone <your-repo-url>
   cd RAG
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install "unstructured[md]"
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Create the vector database**:
   ```bash
   python create_lovable_database.py
   ```

## ⚡ Quick Start

### Command Line Usage

```bash
# Basic usage
python generate_prompt.py --tool lovable --task "build login page" --project "Task Manager App"

# With additional parameters
python generate_prompt.py \
  --tool lovable \
  --task "responsive dashboard" \
  --project "Analytics Platform" \
  --tech "React,Next.js,Tailwind" \
  --requirements "Real-time data,Charts,Export functionality" \
  --ui-requirements "Dark mode,Mobile responsive,Accessibility" \
  --constraints "Use TypeScript,Follow WCAG guidelines" \
  --validate
```

### Web Interface

```bash
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

## 📖 Usage

### Command Line Interface

The CLI provides a powerful way to generate prompts from the command line:

#### Basic Commands

```bash
# Interactive mode - guided prompts
python generate_prompt.py --interactive

# Get task suggestions
python generate_prompt.py --suggestions

# Generate and validate
python generate_prompt.py --tool lovable --task "create user profile" --project "Social App" --validate

# Save to file
python generate_prompt.py --tool lovable --task "API integration" --project "Weather App" --output prompt.md
```

#### Available Options

- `--tool`: Tool name (default: lovable)
- `--task`: Task description (required)
- `--project`: Project name (required)
- `--description`: Project description
- `--tech`: Technology stack (comma-separated)
- `--requirements`: Technical requirements (comma-separated)
- `--ui-requirements`: UI/UX requirements (comma-separated)
- `--constraints`: Project constraints (comma-separated)
- `--interactive`: Run in interactive mode
- `--output`: Output file path
- `--validate`: Validate the generated prompt
- `--suggestions`: Get task suggestions

### Web Interface

The Streamlit web interface provides an intuitive GUI:

1. **Project Information**: Enter basic project details
2. **Task Details**: Specify what you want to build
3. **Requirements**: Add technical and UI requirements
4. **Generate**: Click to create the optimized prompt
5. **Validate**: Optional validation with scoring
6. **Export**: Download in various formats

Features:
- Real-time validation
- Context preview
- Task suggestions
- Copy-to-clipboard functionality
- Multiple export formats

### Python API

Use the prompt generator programmatically:

```python
# When running from project root
from src.generators.build_prompt import LovablePromptGenerator, TaskContext, ProjectInfo

# Initialize generator
generator = LovablePromptGenerator()

# Create context objects
task_context = TaskContext(
    task_type="build login page",
    project_name="Task Manager App",
    description="Create a secure login page with email/password authentication",
    technical_requirements=["NextAuth.js integration", "Form validation", "Error handling"],
    ui_requirements=["Clean design", "Mobile responsive", "Dark mode"],
    constraints=["Use Tailwind CSS", "Follow security best practices"]
)

project_info = ProjectInfo(
    name="Task Manager Pro",
    description="A modern task management application for teams",
    tech_stack=["Next.js", "React", "Tailwind CSS", "TypeScript"],
    target_audience="Professional teams",
    requirements=[]
)

# Generate prompt
prompt = generator.generate_prompt(task_context, project_info)
print(prompt)

# Validate prompt
validation = generator.validate_prompt(prompt)
print(f"Score: {validation['score']}/100")
```

## ⚙️ Configuration

### Tool Profile (lovable.yaml)

Customize the prompt generation behavior:

```yaml
tool_name: Lovable.dev
format: markdown
tone: official yet casual
preferred_use_cases:
  - project kickoff
  - UI scaffolding
  - responsiveness
  - API integrations
few_shot_examples:
  - input: "Start a task management app"
    output: |
      Build a Next.js + Tailwind app with task CRUD, due dates, and a dashboard.
```

### Template Customization

Modify `templates/lovable_task_template.md` to customize prompt structure:

```jinja2
# {{ task_context.task_type.title() }} - {{ project_info.name }}

You are a skilled AI development assistant on **{{ tool_profile.tool_name }}**.

## Project Overview
**Name:** {{ project_info.name }}
**Description:** {{ project_info.description }}
```

## 📁 Documentation Structure

```
data/lovable_docs/
├── prompting_guidelines.md      # Core prompting best practices
├── ui_design_patterns.md        # UI/UX design guidelines
├── api_integration.md           # API integration patterns
└── debugging_patterns.md        # Debugging and troubleshooting
```

Each documentation file is automatically categorized and tagged for optimal retrieval.

## 🎯 Examples

### Example 1: E-commerce Product Page

```bash
python generate_prompt.py \
  --task "create product page" \
  --project "Fashion Store" \
  --tech "Next.js,Tailwind,Stripe" \
  --requirements "Product gallery,Add to cart,Reviews,Stock management" \
  --ui-requirements "Image zoom,Mobile responsive,Loading states" \
  --constraints "SEO optimized,Performance under 3s"
```

### Example 2: Dashboard with Analytics

```bash
python generate_prompt.py \
  --task "analytics dashboard" \
  --project "SaaS Platform" \
  --tech "React,Chart.js,Tailwind" \
  --requirements "Real-time data,Export charts,Filters,Date ranges" \
  --ui-requirements "Dark mode,Responsive grid,Tooltips" \
  --constraints "TypeScript,Accessibility compliant"
```

### Example 3: Authentication System

```bash
python generate_prompt.py \
  --task "user authentication" \
  --project "Community Platform" \
  --tech "Next.js,NextAuth,Prisma" \
  --requirements "OAuth providers,Email verification,Password reset" \
  --ui-requirements "Clean forms,Error states,Success feedback" \
  --constraints "Security best practices,GDPR compliant"
```

## 🔧 Advanced Usage

### Custom Categories

Add new categories by modifying the metadata in `create_lovable_database.py`:

```python
# Add custom categorization logic
if 'your_custom_keyword' in source_file.lower():
    chunk.metadata['category'] = 'your_category'
    chunk.metadata['tags'] = ['tag1', 'tag2']
```

### Filtering by Context

Use category-specific retrieval:

```python
context_docs = generator.get_relevant_context(
    task_type="build dashboard",
    query="responsive design",
    category="ui_design"  # Filter by category
)
```

### Validation Customization

Modify validation criteria in the `validate_prompt` method:

```python
# Custom validation rules
def custom_validate(self, prompt):
    score = 0
    if 'accessibility' in prompt.lower():
        score += 10
    if 'responsive' in prompt.lower():
        score += 10
    return score
```

## 🛠️ Troubleshooting

### Common Issues

1. **Vector Database Not Found**
   ```
   Error: chroma_lovable directory not found
   ```
   **Solution**: Run `python create_lovable_database.py`

2. **OpenAI API Key Error**
   ```
   Error: OpenAI API key not found
   ```
   **Solution**: Check your `.env` file and ensure `OPENAI_API_KEY` is set

3. **Template Not Found**
   ```
   Error: Template 'lovable_task_template.md' not found
   ```
   **Solution**: Ensure the `templates/` directory exists with the template file

4. **Empty Context Retrieval**
   ```
   Warning: No relevant context found
   ```
   **Solution**: Check if your documentation files are properly loaded in the vector database

### Performance Tips

1. **Optimize Chunk Size**: Adjust `chunk_size` in the text splitter for better retrieval
2. **Use Category Filters**: Specify categories to reduce search space
3. **Cache Results**: Store frequently used prompts to avoid regeneration
4. **Batch Processing**: Process multiple prompts in sequence for efficiency

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run your prompt generation
generator = LovablePromptGenerator()
```

## 📊 Validation Scoring

The validation system scores prompts based on:

- **Completeness** (25 points): All required sections present
- **Specificity** (25 points): Avoids vague language
- **Structure** (25 points): Well-organized content
- **Best Practices** (25 points): Follows Lovable.dev guidelines

**Scoring Breakdown:**
- 90-100: Excellent
- 70-89: Good
- 50-69: Acceptable
- Below 50: Needs improvement

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new documentation files to `data/lovable_docs/`
4. Update the database: `python create_lovable_database.py`
5. Test your changes
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Lovable.dev for the amazing development platform
- LangChain for the RAG framework
- OpenAI for embeddings and language models
- Streamlit for the web interface

---

**Need help?** Check the troubleshooting section or open an issue on GitHub.
