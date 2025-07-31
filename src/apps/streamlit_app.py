"""
Streamlit Web Interface for Lovable.dev Prompt Generator
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import json
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.generators.build_prompt import LovablePromptGenerator, TaskContext, ProjectInfo

# Page configuration
st.set_page_config(
    page_title="Lovable.dev Prompt Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'generator' not in st.session_state:
    try:
        st.session_state.generator = LovablePromptGenerator()
        st.session_state.generator_ready = True
    except Exception as e:
        st.session_state.generator_ready = False
        st.session_state.generator_error = str(e)

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🚀 Lovable.dev Prompt Generator")
    st.markdown("Generate optimized prompts for Lovable.dev using RAG-powered context retrieval")
    
    # Check if generator is ready
    if not st.session_state.generator_ready:
        st.error(f"Failed to initialize generator: {st.session_state.generator_error}")
        st.stop()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Task suggestions
        st.subheader("💡 Task Suggestions")
        project_type = st.selectbox(
            "Project Type",
            options=["web_app", "mobile_app", "ecommerce", "blog"],
            help="Select project type to get relevant task suggestions"
        )
        
        if st.button("Get Suggestions"):
            suggestions = st.session_state.generator.get_task_suggestions(project_type)
            st.write("**Suggested tasks:**")
            for suggestion in suggestions:
                st.write(f"• {suggestion}")
        
        st.divider()
        
        # Advanced options
        st.subheader("🔧 Advanced Options")
        validate_prompt = st.checkbox("Validate generated prompt", value=True)
        show_context = st.checkbox("Show retrieved context", value=False)
        
        # Export options
        st.subheader("📤 Export")
        export_format = st.selectbox("Export Format", ["Markdown", "JSON", "Plain Text"])
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Project Information")
        
        # Project details
        project_name = st.text_input(
            "Project Name *",
            placeholder="e.g., Task Manager Pro",
            help="Name of your project"
        )
        
        project_description = st.text_area(
            "Project Description *",
            placeholder="A modern task management application for teams...",
            help="Brief description of your project"
        )
        
        tech_stack_input = st.text_input(
            "Technology Stack *",
            placeholder="React, Next.js, Tailwind CSS, TypeScript",
            help="Comma-separated list of technologies"
        )
        
        target_audience = st.text_input(
            "Target Audience",
            placeholder="Professional teams and project managers",
            value="General users"
        )
        
        st.header("🎯 Task Details")
        
        # Task information
        task_type = st.text_input(
            "Task Type *",
            placeholder="e.g., build login page, create dashboard",
            help="What type of task you want to accomplish"
        )
        
        task_description = st.text_area(
            "Task Description *",
            placeholder="Create a secure login page with email/password authentication...",
            help="Detailed description of the task"
        )
        
        # Requirements
        st.subheader("Technical Requirements")
        tech_requirements = st.text_area(
            "Technical Requirements",
            placeholder="NextAuth.js integration, Form validation, Error handling...",
            help="Comma-separated technical requirements"
        )
        
        st.subheader("UI/UX Requirements")
        ui_requirements = st.text_area(
            "UI/UX Requirements",
            placeholder="Clean modern design, Mobile responsive, Dark mode support...",
            help="Comma-separated UI/UX requirements"
        )
        
        st.subheader("Constraints")
        constraints = st.text_area(
            "Constraints",
            placeholder="Use Tailwind CSS, Follow security best practices...",
            help="Comma-separated constraints"
        )
    
    with col2:
        st.header("🎯 Generated Prompt")
        
        # Generate button
        if st.button("🚀 Generate Prompt", type="primary", use_container_width=True):
            # Validate required fields
            if not all([project_name, project_description, tech_stack_input, task_type, task_description]):
                st.error("Please fill in all required fields marked with *")
                st.stop()
            
            # Parse inputs
            tech_stack = [tech.strip() for tech in tech_stack_input.split(',') if tech.strip()]
            tech_reqs = [req.strip() for req in tech_requirements.split(',') if req.strip()]
            ui_reqs = [req.strip() for req in ui_requirements.split(',') if req.strip()]
            constraint_list = [c.strip() for c in constraints.split(',') if c.strip()]
            
            # Create context objects
            task_context = TaskContext(
                task_type=task_type,
                project_name=project_name,
                description=task_description,
                technical_requirements=tech_reqs,
                ui_requirements=ui_reqs,
                constraints=constraint_list
            )
            
            project_info = ProjectInfo(
                name=project_name,
                description=project_description,
                tech_stack=tech_stack,
                target_audience=target_audience,
                requirements=[]
            )
            
            # Generate prompt
            with st.spinner("Generating prompt..."):
                try:
                    prompt = st.session_state.generator.generate_prompt(task_context, project_info)
                    
                    # Store in session state
                    st.session_state.generated_prompt = prompt
                    st.session_state.task_context = task_context
                    st.session_state.project_info = project_info
                    
                    st.success("✅ Prompt generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Failed to generate prompt: {e}")
                    st.stop()
        
        # Display generated prompt
        if 'generated_prompt' in st.session_state:
            # Validation results
            if validate_prompt:
                with st.expander("🔍 Validation Results", expanded=False):
                    validation = st.session_state.generator.validate_prompt(st.session_state.generated_prompt)
                    
                    col1_val, col2_val = st.columns(2)
                    with col1_val:
                        st.metric("Validation Score", f"{validation['score']}/100")
                    with col2_val:
                        status = "✅ Valid" if validation['is_valid'] else "❌ Invalid"
                        st.metric("Status", status)
                    
                    if validation['issues']:
                        st.warning("**Issues found:**")
                        for issue in validation['issues']:
                            st.write(f"• {issue}")
                    
                    if validation['suggestions']:
                        st.info("**Suggestions:**")
                        for suggestion in validation['suggestions']:
                            st.write(f"• {suggestion}")
            
            # Show retrieved context
            if show_context:
                with st.expander("📚 Retrieved Context", expanded=False):
                    context_docs = st.session_state.generator.get_relevant_context(
                        st.session_state.task_context.task_type,
                        st.session_state.task_context.description
                    )
                    
                    if context_docs:
                        for i, doc in enumerate(context_docs[:3], 1):
                            st.write(f"**Context {i}:**")
                            st.text(doc.page_content[:300] + "...")
                            st.write(f"*Source: {doc.metadata.get('source', 'Unknown')}*")
                            st.write("---")
                    else:
                        st.write("No relevant context found.")
            
            # Display prompt
            st.subheader("Generated Prompt")
            prompt_container = st.container()
            
            with prompt_container:
                st.markdown(st.session_state.generated_prompt)
            
            # Copy to clipboard
            st.code(st.session_state.generated_prompt, language='markdown')
            
            # Export options
            st.subheader("📤 Export")
            
            col1_exp, col2_exp, col3_exp = st.columns(3)
            
            with col1_exp:
                if export_format == "Markdown":
                    st.download_button(
                        "💾 Download Markdown",
                        st.session_state.generated_prompt,
                        file_name=f"{project_name.lower().replace(' ', '_')}_prompt.md",
                        mime="text/markdown"
                    )
            
            with col2_exp:
                if export_format == "JSON":
                    export_data = {
                        "project_info": {
                            "name": st.session_state.project_info.name,
                            "description": st.session_state.project_info.description,
                            "tech_stack": st.session_state.project_info.tech_stack,
                            "target_audience": st.session_state.project_info.target_audience
                        },
                        "task_context": {
                            "task_type": st.session_state.task_context.task_type,
                            "description": st.session_state.task_context.description,
                            "technical_requirements": st.session_state.task_context.technical_requirements,
                            "ui_requirements": st.session_state.task_context.ui_requirements,
                            "constraints": st.session_state.task_context.constraints
                        },
                        "generated_prompt": st.session_state.generated_prompt
                    }
                    
                    st.download_button(
                        "💾 Download JSON",
                        json.dumps(export_data, indent=2),
                        file_name=f"{project_name.lower().replace(' ', '_')}_prompt.json",
                        mime="application/json"
                    )
            
            with col3_exp:
                if export_format == "Plain Text":
                    st.download_button(
                        "💾 Download Text",
                        st.session_state.generated_prompt,
                        file_name=f"{project_name.lower().replace(' ', '_')}_prompt.txt",
                        mime="text/plain"
                    )

# Footer
def footer():
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>🚀 Lovable.dev Prompt Generator | Built with Streamlit</p>
        <p>Powered by RAG (Retrieval-Augmented Generation)</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    footer()
