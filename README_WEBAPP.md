# 🎨 AI Tool Prompt Generator

A Flask web application for generating UI/UX design prompts tailored for specific AI development tools using RAG (Retrieval-Augmented Generation) technology.

## 🌟 Features

- **Multi-Tool Support**: Generate prompts for 15+ AI development tools including:
  - Lovable.dev
  - Bolt.new
  - V0.dev
  - Cursor
  - Framer
  - Bubble
  - FlutterFlow
  - And many more!

- **Intelligent Prompt Generation**: Uses RAG system with tool-specific documentation
- **UI/UX Focus**: Specialized templates for page-by-page design planning
- **Cross-Device Design**: Mobile-first approach with desktop scaling
- **Modern Web Interface**: Beautiful, responsive interface with Tailwind CSS

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. **Clone or download the project**

   ```bash
   cd "c:\Users\2005g\Downloads\RAG"
   ```

2. **Install dependencies**

   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python app.py
   ```

4. **Open your browser**

   Navigate to: <http://localhost:5000>

## 📋 How to Use

1. **Select Your AI Tool**: Choose from 15+ supported development tools
2. **Fill Project Details**:
   - App Name (required)
   - Platform (Web/Mobile/Desktop)
   - Design Style (Minimal/Fun/Business)
   - Style Description (optional)
   - App Idea (required - be detailed!)
   - Target Users (optional)

3. **Generate Prompt**: Click "Generate UI/UX Prompt"
4. **Copy & Use**: Copy the generated prompt and paste it into your chosen AI tool

## 🎯 Generated Prompt Format

The application generates structured prompts that include:

- **Tool-specific context** from RAG system
- **Page-by-page breakdown** with detailed UI specifications
- **Cross-device considerations** (mobile + desktop)
- **UX flow mapping** from onboarding to completion
- **Component specifications** with modern design principles

## 📁 Project Structure

```text
RAG/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── src/
│   ├── core/
│   │   └── types.py      # Type definitions
│   └── generators/
│       └── enhanced_generator.py  # RAG prompt generator
├── data/                 # Tool documentation
├── config/               # Tool configurations
├── chroma_*/            # Vector databases
└── infra/               # Azure deployment files (for future)
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Tailwind), JavaScript
- **AI/ML**: LangChain, ChromaDB, Google Gemini
- **Deployment Ready**: Azure App Service configuration included

## 🌐 Supported Tools

- Lovable.dev - React development with Supabase
- Bolt.new - Full-stack web development
- V0.dev - Vercel's AI interface generator
- Cursor - AI-powered code editor
- Framer - Interactive design tool
- Bubble - No-code web app builder
- FlutterFlow - Visual Flutter development
- Uizard - AI design tool
- Adalo - Mobile app builder
- Cline - AI coding assistant
- Devin - AI software engineer
- Windsurf - AI development environment
- And more!

## 🔧 Customization

### Adding New Tools

1. Add tool configuration in `config/tools/`
2. Update `SupportedTool` enum in `src/core/types.py`
3. Add tool documentation in `data/` directory

### Modifying Prompt Templates

Edit the `UIUX_PROMPT_TEMPLATE` in `app.py` to customize the output format.

## 📊 RAG System

The application uses a sophisticated RAG system that:

- Indexes tool-specific documentation
- Provides context-aware prompt enhancement
- Calculates confidence scores for generated prompts
- Suggests improvements based on tool capabilities

## 🚀 Future Deployment (Azure)

The project includes infrastructure-as-code files for Azure deployment:

- `azure.yaml` - AZD configuration
- `infra/` - Bicep templates
- Ready for one-click deployment to Azure App Service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check that all dependencies are installed
2. Ensure Python 3.8+ is being used
3. Verify the Flask application starts without errors
4. Check the browser console for any JavaScript errors

---

Happy Prompting! 🎨✨
