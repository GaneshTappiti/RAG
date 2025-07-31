# Lovable.dev RAG System Setup Guide - Google Gemini Edition

## 🚀 Quick Start with Google Gemini

Since you're using Google Gemini API, this guide will help you set up the complete RAG system with your existing Gemini configuration.

## 📋 Prerequisites

1. **Google AI Studio API Key**: You already have this set up
2. **Python 3.8+**: Required for all dependencies
3. **VS Code**: Recommended for development

## ⚙️ Setup Steps

### 1. Environment Configuration

Your `.env` file should contain:

```bash
GOOGLE_API_KEY=your-google-api-key-here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The requirements.txt already includes all Gemini-specific packages:

- `langchain-google-genai` - Google Gemini integration
- `google-generativeai` - Google AI SDK
- `chromadb` - Vector database
- `streamlit` - Web interface

### 3. Create Vector Database (Optional)

If you want full RAG capabilities with semantic search:

```bash
python create_lovable_database_gemini.py
```

This creates a `chroma_lovable_gemini` directory with your vector database.

## 🎯 Usage Options

### Option 1: Demo Mode (Works Immediately)

```bash
python demo_prompt_generator_gemini.py
```

- No API key required
- Uses built-in examples
- Perfect for testing

### Option 2: CLI Interface

```bash
# Interactive mode
python generate_prompt_gemini.py

# Batch mode with config file
python generate_prompt_gemini.py -c config.json

# Save example configuration
python generate_prompt_gemini.py --example
```

### Option 3: Web Interface

```bash
streamlit run streamlit_app_gemini.py
```

- Interactive web UI
- Real-time validation
- Export capabilities

### Option 4: Full RAG System

```bash
python build_prompt_gemini.py
```

- Requires vector database
- Uses semantic search
- Context-aware generation

## 🔧 Configuration Files

### lovable.yaml

Your tool profile configuration (already created):

- Defines tone and style
- Contains few-shot examples
- Sets prompting guidelines

### Vector Database

Located in `chroma_gemini/` directory from your existing setup, or create new one with:

- `chroma_lovable_gemini/` for this system

## 📁 File Structure

```text
RAG/
├── lovable.yaml                        # Tool configuration
├── build_prompt_gemini.py             # Main RAG system (Gemini)
├── create_lovable_database_gemini.py  # Vector DB creation (Gemini)
├── demo_prompt_generator_gemini.py    # Working demo (Gemini)
├── generate_prompt_gemini.py          # CLI interface (Gemini)
├── streamlit_app_gemini.py           # Web interface (Gemini)
├── requirements.txt                    # Dependencies
├── .env                               # Environment variables
└── data/
    └── lovable_docs/                  # Documentation for RAG
        ├── lovable_prompting_guide.md
        ├── lovable_ui_design_guide.md
        ├── lovable_api_integration_guide.md
        └── lovable_debugging_guide.md
```

## 🚨 Troubleshooting

### 1. Import Errors

If you see import errors for `jinja2` or other packages:

```bash
pip install jinja2 pyyaml streamlit
```

### 2. Gemini API Issues

- Verify your `GOOGLE_API_KEY` in `.env` file
- Check API quota limits in Google AI Studio
- Ensure your API key has the correct permissions

### 3. Vector Database Issues

- If vector database creation fails, use demo mode
- Check that documentation files exist in `data/lovable_docs/`
- Ensure sufficient disk space for ChromaDB

### 4. Missing Dependencies

```bash
pip install --upgrade -r requirements.txt
```

## 🎯 Validation Scores

The system validates generated prompts with scores:

- **90-100**: Excellent prompt quality
- **80-89**: Good prompt quality  
- **70-79**: Acceptable with minor issues
- **Below 70**: Needs improvement

## 💡 Tips for Best Results

1. **Be Specific**: Include detailed technical requirements
2. **Define Tech Stack**: Specify exact versions when possible
3. **Include Constraints**: Performance, accessibility, security
4. **Set Success Criteria**: Clear, measurable outcomes
5. **Use Examples**: Reference similar projects or features

## 🔄 Upgrade Path

1. **Current**: Demo mode with template-based generation
2. **Next**: Create vector database for semantic search
3. **Advanced**: Custom documentation and domain-specific knowledge

## 📞 Quick Commands Reference

```bash
# Demo (works immediately)
python demo_prompt_generator_gemini.py

# Web interface
streamlit run streamlit_app_gemini.py

# CLI interactive
python generate_prompt_gemini.py

# Create vector database
python create_lovable_database_gemini.py

# Full RAG system
python build_prompt_gemini.py
```

## 🎉 You're Ready

Your Gemini-powered RAG system is ready to use. Start with the demo to see it in action, then move to the web interface or CLI based on your preference.

The system will generate optimized Lovable.dev prompts with:

- ✅ Proper structure and formatting
- ✅ Technical specifications
- ✅ UI/UX requirements  
- ✅ Implementation guidelines
- ✅ Success criteria
- ✅ Validation scoring
