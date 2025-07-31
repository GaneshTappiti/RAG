"""
Streamlit Web Interface for Lovable.dev Prompt Generator with Google Gemini
Description: Interactive web interface for generating optimized Lovable.dev prompts using Gemini RAG
"""

import streamlit as st
import os
import yaml
from shared_types import TaskContext, ProjectInfo
from typing import List, Dict, Any

# Configure the page
st.set_page_config(
    page_title="Lovable.dev Prompt Generator | Gemini",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f9fafb;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
    .success-message {
        padding: 1rem;
        background-color: #dcfce7;
        border-radius: 0.5rem;
        border-left: 4px solid #16a34a;
        color: #15803d;
    }
    .warning-message {
        padding: 1rem;
        background-color: #fef3c7;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
        color: #92400e;
    }
</style>
""", unsafe_allow_html=True)

def load_tool_profile(config_path: str = "lovable.yaml") -> Dict[str, Any]:
    """Load the Lovable.dev tool profile configuration"""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        st.warning(f"Configuration file {config_path} not found. Using default settings.")
        return {
            'tool_name': 'Lovable.dev',
            'format': 'markdown',
            'tone': 'official yet casual'
        }

def validate_prompt(prompt: str) -> Dict[str, Any]:
    """Validate the generated prompt for completeness"""
    validation_results = {
        'is_valid': True,
        'score': 0,
        'issues': [],
        'suggestions': []
    }
    
    # Check for key components
    required_sections = ['context', 'requirements', 'technical', 'ui']
    score = 0
    
    for section in required_sections:
        if section.lower() in prompt.lower():
            score += 25
        else:
            validation_results['issues'].append(f"Missing {section} section")
    
    # Check prompt length
    if len(prompt) < 200:
        validation_results['issues'].append("Prompt is too short")
        score -= 10
    elif len(prompt) > 2000:
        validation_results['issues'].append("Prompt might be too long")
        score -= 5
    
    # Check for specificity
    vague_words = ['nice', 'good', 'better', 'improve', 'enhance']
    vague_count = sum(1 for word in vague_words if word in prompt.lower())
    if vague_count > 3:
        validation_results['issues'].append("Prompt contains vague language")
        score -= 10
    
    validation_results['score'] = max(0, min(100, score))
    validation_results['is_valid'] = validation_results['score'] >= 60
    
    if not validation_results['is_valid']:
        validation_results['suggestions'] = [
            "Be more specific about requirements",
            "Include technical stack details",
            "Add UI/UX specifications",
            "Define success criteria"
        ]
    
    return validation_results

def generate_simple_prompt(task_context: TaskContext, project_info: ProjectInfo) -> str:
    """Generate a prompt using template-based approach for demo purposes"""
    
    tech_stack = ', '.join(project_info.tech_stack)
    tech_reqs = '\n'.join(f"- {req}" for req in task_context.technical_requirements)
    ui_reqs = '\n'.join(f"- {req}" for req in task_context.ui_requirements)
    constraints = '\n'.join(f"- {constraint}" for constraint in task_context.constraints)
    
    prompt = f"""# {task_context.task_type.title()} for {project_info.name}

## Project Overview
{project_info.description}

**Target Audience:** {project_info.target_audience}
**Technology Stack:** {tech_stack}

## Task Description
{task_context.description}

## Technical Requirements
{tech_reqs}

## UI/UX Requirements
{ui_reqs}

## Constraints & Guidelines
{constraints}

## Expected Deliverables
Create a modern, responsive web application that follows Lovable.dev best practices:

- Clean, maintainable code structure
- Mobile-first responsive design
- Accessible UI components (WCAG 2.1)
- Proper error handling and loading states
- Performance optimized (Core Web Vitals)
- Cross-browser compatibility
- SEO-friendly implementation

## Success Criteria
- Application loads in under 2 seconds
- Responsive across all device sizes
- Passes accessibility audits
- Clean code with proper documentation
- Working deployment with CI/CD pipeline

Please implement this step by step, ensuring each component is thoroughly tested before moving to the next."""

    return prompt

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🚀 Lovable.dev Prompt Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by Google Gemini RAG | Generate optimized development prompts</p>', unsafe_allow_html=True)
    
    # Load configuration
    tool_profile = load_tool_profile()
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Status Check
        gemini_api_key = os.getenv('GOOGLE_API_KEY', '')
        if gemini_api_key and gemini_api_key != 'your-google-api-key-here':
            st.success("✅ Google Gemini API configured")
            rag_enabled = st.checkbox("Use RAG retrieval", value=True, help="Enable semantic search for context")
        else:
            st.warning("⚠️ Google Gemini API not configured")
            st.info("Set GOOGLE_API_KEY in .env file for full RAG capabilities")
            rag_enabled = False
        
        # Vector Database Status
        chroma_path = "chroma_lovable_gemini"
        if os.path.exists(chroma_path):
            st.success("✅ Vector database ready")
        else:
            st.warning("📚 Vector database not found")
            if st.button("Create Vector Database"):
                with st.spinner("Creating vector database..."):
                    # This would run the database creation
                    st.info("Run: `python create_lovable_database_gemini.py`")
        
        st.divider()
        
        # Quick presets
        st.subheader("🎯 Quick Presets")
        preset = st.selectbox("Choose a preset:", [
            "Custom",
            "E-commerce Store",
            "SaaS Dashboard", 
            "Blog Platform",
            "Mobile App",
            "Portfolio Site"
        ])
        
        if preset != "Custom":
            st.info(f"Using {preset} preset template")

    # Main Content Area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Project Configuration")
        
        # Project Information
        with st.expander("🏢 Project Details", expanded=True):
            project_name = st.text_input("Project Name", value="MyApp")
            project_description = st.text_area(
                "Project Description",
                value="A modern web application",
                height=100
            )
            target_audience = st.text_input("Target Audience", value="General users")
            
            # Technology Stack
            tech_options = [
                "Next.js", "React", "Vue.js", "Angular", "Svelte",
                "TypeScript", "JavaScript", "Python", "Node.js",
                "Tailwind CSS", "Material-UI", "Chakra UI", "Ant Design",
                "Prisma", "Supabase", "Firebase", "MongoDB", "PostgreSQL"
            ]
            tech_stack = st.multiselect("Technology Stack", tech_options, default=["Next.js", "React", "Tailwind CSS"])
        
        # Task Configuration
        with st.expander("🎯 Task Configuration", expanded=True):
            task_type = st.selectbox("Task Type", [
                "build complete application",
                "create responsive dashboard", 
                "implement authentication",
                "add payment integration",
                "optimize performance",
                "enhance accessibility",
                "debug and refactor"
            ])
            
            task_description = st.text_area(
                "Task Description", 
                value="Create a modern, user-friendly application",
                height=100
            )
        
        # Requirements
        with st.expander("📋 Requirements", expanded=True):
            st.subheader("Technical Requirements")
            tech_req_input = st.text_area("Enter requirements (one per line)", height=100)
            tech_requirements = [req.strip() for req in tech_req_input.split('\n') if req.strip()]
            
            st.subheader("UI/UX Requirements")
            ui_req_input = st.text_area("Enter UI requirements (one per line)", height=100)
            ui_requirements = [req.strip() for req in ui_req_input.split('\n') if req.strip()]
            
            st.subheader("Constraints")
            constraints_input = st.text_area("Enter constraints (one per line)", height=100)
            constraints = [constraint.strip() for constraint in constraints_input.split('\n') if constraint.strip()]

    with col2:
        st.header("🚀 Generated Prompt")
        
        # Generate button
        if st.button("🎨 Generate Prompt", type="primary", use_container_width=True):
            
            # Create data structures
            task_context = TaskContext(
                task_type=task_type,
                project_name=project_name,
                description=task_description,
                technical_requirements=tech_requirements,
                ui_requirements=ui_requirements,
                constraints=constraints
            )
            
            project_info = ProjectInfo(
                name=project_name,
                description=project_description,
                tech_stack=tech_stack,
                target_audience=target_audience,
                requirements=[]
            )
            
            # Generate prompt
            with st.spinner("Generating optimized prompt..."):
                try:
                    if rag_enabled and os.path.exists(chroma_path):
                        # Try to use full RAG system
                        try:
                            from build_prompt_gemini import LovablePromptGeneratorGemini
                            generator = LovablePromptGeneratorGemini()
                            generated_prompt = generator.generate_prompt(task_context, project_info)
                        except Exception as e:
                            st.warning(f"RAG system unavailable: {e}")
                            generated_prompt = generate_simple_prompt(task_context, project_info)
                    else:
                        # Use simple template-based generation
                        generated_prompt = generate_simple_prompt(task_context, project_info)
                    
                    # Store in session state
                    st.session_state.generated_prompt = generated_prompt
                    st.success("✅ Prompt generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error generating prompt: {e}")
                    st.session_state.generated_prompt = None
        
        # Display generated prompt
        if hasattr(st.session_state, 'generated_prompt') and st.session_state.generated_prompt:
            
            # Validation
            validation = validate_prompt(st.session_state.generated_prompt)
            
            # Validation metrics
            col_score, col_status = st.columns(2)
            with col_score:
                st.metric("Quality Score", f"{validation['score']}/100")
            with col_status:
                status = "✅ Valid" if validation['is_valid'] else "⚠️ Needs Review"
                st.metric("Status", status)
            
            # Validation details
            if validation['issues']:
                with st.expander("⚠️ Validation Issues", expanded=True):
                    for issue in validation['issues']:
                        st.warning(f"• {issue}")
            
            if validation['suggestions']:
                with st.expander("💡 Suggestions"):
                    for suggestion in validation['suggestions']:
                        st.info(f"• {suggestion}")
            
            # Prompt display
            st.subheader("📄 Generated Prompt")
            st.text_area(
                "Copy this prompt to Lovable.dev:",
                value=st.session_state.generated_prompt,
                height=400,
                key="prompt_display"
            )
            
            # Export options
            col_copy, col_download = st.columns(2)
            with col_copy:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.info("Prompt copied! (Use Ctrl+C to copy from text area)")
            
            with col_download:
                st.download_button(
                    label="💾 Download as .md",
                    data=st.session_state.generated_prompt,
                    file_name=f"{project_name.lower().replace(' ', '_')}_prompt.md",
                    mime="text/markdown",
                    use_container_width=True
                )

    # Footer
    st.divider()
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.info("💡 **Tip:** Be specific about your requirements for better prompts")
    
    with col_info2:
        st.info("🔍 **RAG:** Enable semantic search for context-aware generation")
    
    with col_info3:
        st.info("⚡ **Fast:** Template-based generation works without API keys")

if __name__ == "__main__":
    main()
