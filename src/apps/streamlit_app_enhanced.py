"""
Enhanced Tool-Specific Streamlit Web Interface
Supports multiple no-code/low-code tools with stage-wise prompt generation
Run with: streamlit run streamlit_app_enhanced.py
"""

import streamlit as st
import json
import sys
import os
from typing import Dict, List, Optional

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.generators.tool_specific_generator import ToolSpecificPromptGenerator, TaskContext, ProjectInfo

# Page configuration
st.set_page_config(
    page_title="Multi-Tool Prompt Generator",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .tool-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
    .stage-badge {
        background: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.25rem;
        display: inline-block;
    }
    .stSelectbox > div > div {
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generator' not in st.session_state:
    try:
        st.session_state.generator = ToolSpecificPromptGenerator()
        st.session_state.generator_ready = True
        st.session_state.available_tools = st.session_state.generator.get_available_tools()
    except Exception as e:
        st.session_state.generator_ready = False
        st.session_state.generator_error = str(e)
        st.session_state.available_tools = []

def display_tool_info(tool: str):
    """Display information about the selected tool"""
    if not st.session_state.generator_ready:
        return
    
    tool_info = st.session_state.generator.get_tool_info(tool)
    if tool_info:
        with st.container():
            st.markdown(f"""
            <div class="tool-card">
                <h3>🛠️ {tool_info['name']}</h3>
                <p><strong>Framework:</strong> {tool_info['framework']}</p>
                <p><strong>Tone:</strong> {tool_info['tone']} | <strong>Format:</strong> {tool_info['format']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display stages
            if tool_info['stages']:
                st.write("**Available Stages:**")
                stages_html = "".join([
                    f'<span class="stage-badge">{stage}</span>' 
                    for stage in tool_info['stages']
                ])
                st.markdown(stages_html, unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🛠️ Multi-Tool Prompt Generator</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; color: #666; font-size: 1.1rem;">Generate tool-specific prompts with stage-wise development using RAG-powered documentation</p>',
        unsafe_allow_html=True
    )
    
    # Check if generator is ready
    if not st.session_state.generator_ready:
        st.error(f"❌ Failed to initialize generator: {st.session_state.generator_error}")
        st.info("💡 Make sure you have the required dependencies installed and the vector database is set up.")
        st.stop()
    
    # Sidebar for tool selection and configuration
    with st.sidebar:
        st.header("🎯 Tool Selection")
        
        # Tool selection
        selected_tool = st.selectbox(
            "Choose Development Tool",
            options=st.session_state.available_tools,
            index=0 if st.session_state.available_tools else 0,
            help="Select the no-code/low-code tool you want to generate prompts for"
        )
        
        # Display tool information
        if selected_tool:
            display_tool_info(selected_tool)
            
            # Get tool-specific stages
            available_stages = st.session_state.generator.get_tool_stages(selected_tool)
            available_components = st.session_state.generator.get_tool_components(selected_tool)
        else:
            available_stages = ['planning', 'implementation', 'testing']
            available_components = ['ui', 'logic', 'data']
        
        st.divider()
        
        # Stage selection
        st.subheader("📋 Development Stage")
        selected_stage = st.selectbox(
            "Current Stage",
            options=available_stages,
            help="Select the development stage you're currently working on"
        )
        
        # Component selection (optional)
        st.subheader("🧩 Component Focus")
        selected_component = st.selectbox(
            "Component Type (Optional)",
            options=["None"] + available_components,
            help="Optional: Focus on a specific component type"
        )
        
        st.divider()
        
        # Task suggestions
        st.subheader("💡 Task Suggestions")
        project_type = st.selectbox(
            "Project Type",
            options=["web_app", "mobile_app", "ecommerce", "blog", "dashboard", "landing_page"],
            help="Select project type to get relevant task suggestions"
        )
        
        if st.button("🔄 Get Tool-Specific Suggestions"):
            if selected_tool:
                suggestions = st.session_state.generator.get_tool_suggestions(selected_tool, project_type)
                st.write("**Suggested tasks:**")
                for suggestion in suggestions:
                    st.write(f"• {suggestion}")
        
        st.divider()
        
        # Advanced options
        st.subheader("⚙️ Advanced Options")
        validate_prompt = st.checkbox("Validate generated prompt", value=True)
        show_context = st.checkbox("Show retrieved context", value=False)
        show_metadata = st.checkbox("Show tool metadata", value=False)
        
        # Export options
        st.subheader("📤 Export Options")
        export_format = st.selectbox("Export Format", ["Markdown", "JSON", "Plain Text"])
        include_metadata = st.checkbox("Include metadata in export", value=True)
    
    # Main content area - split into two columns
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
            help="Brief description of your project",
            height=100
        )
        
        tech_stack_input = st.text_input(
            "Technology Stack *",
            placeholder="React, Next.js, Tailwind CSS, TypeScript",
            help="Comma-separated list of technologies (will be adapted for the selected tool)"
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
            placeholder=f"e.g., build login page, create dashboard (for {selected_tool})",
            help="What type of task you want to accomplish with the selected tool"
        )
        
        task_description = st.text_area(
            "Task Description *",
            placeholder=f"Create a secure login page using {selected_tool} with email/password authentication...",
            help="Detailed description of the task for the selected tool",
            height=120
        )
        
        # Requirements sections
        col1a, col1b = st.columns(2)
        
        with col1a:
            st.subheader("🔧 Technical Requirements")
            tech_requirements = st.text_area(
                "Technical Requirements",
                placeholder="Integration requirements, data handling, security...",
                help="Comma-separated technical requirements",
                height=80
            )
        
        with col1b:
            st.subheader("🎨 UI/UX Requirements")
            ui_requirements = st.text_area(
                "UI/UX Requirements",
                placeholder="Design system, responsiveness, accessibility...",
                help="Comma-separated UI/UX requirements",
                height=80
            )
        
        st.subheader("⚠️ Constraints & Limitations")
        constraints = st.text_area(
            "Constraints",
            placeholder=f"Tool-specific limitations, budget constraints, timeline...",
            help="Comma-separated constraints specific to the selected tool",
            height=60
        )
    
    with col2:
        st.header("🚀 Generated Stage-Specific Prompt")
        
        # Generate button
        generate_col1, generate_col2 = st.columns([3, 1])
        with generate_col1:
            generate_button = st.button(
                f"🚀 Generate {selected_stage.title()} Prompt for {selected_tool}",
                type="primary",
                use_container_width=True
            )
        
        with generate_col2:
            if st.button("🔄", help="Regenerate with same inputs"):
                generate_button = True
        
        if generate_button:
            # Validate required fields
            if not all([project_name, project_description, tech_stack_input, task_type, task_description, selected_tool]):
                st.error("❌ Please fill in all required fields marked with *")
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
                tool=selected_tool,
                stage=selected_stage,
                technical_requirements=tech_reqs,
                ui_requirements=ui_reqs,
                constraints=constraint_list,
                component_type=selected_component if selected_component != "None" else None
            )
            
            project_info = ProjectInfo(
                name=project_name,
                description=project_description,
                tech_stack=tech_stack,
                target_audience=target_audience,
                requirements=[],
                tool=selected_tool
            )
            
            # Generate prompt
            with st.spinner(f"🔄 Generating {selected_stage} prompt for {selected_tool}..."):
                try:
                    prompt = st.session_state.generator.generate_stage_prompt(task_context, project_info)
                    
                    # Store in session state
                    st.session_state.generated_prompt = prompt
                    st.session_state.task_context = task_context
                    st.session_state.project_info = project_info
                    
                    st.success(f"✅ {selected_stage.title()} prompt generated successfully for {selected_tool}!")
                    
                except Exception as e:
                    st.error(f"❌ Failed to generate prompt: {e}")
                    st.stop()
        
        # Display generated content
        if 'generated_prompt' in st.session_state:
            
            # Show tool metadata if requested
            if show_metadata:
                with st.expander("🛠️ Tool Metadata", expanded=False):
                    tool_info = st.session_state.generator.get_tool_info(selected_tool)
                    st.json(tool_info)
            
            # Validation results
            if validate_prompt:
                with st.expander("🔍 Validation Results", expanded=False):
                    validation = st.session_state.generator.validate_prompt(
                        st.session_state.generated_prompt, 
                        selected_tool
                    )
                    
                    col1_val, col2_val, col3_val = st.columns(3)
                    with col1_val:
                        st.metric("Validation Score", f"{validation['score']}/100")
                    with col2_val:
                        status = "✅ Valid" if validation['is_valid'] else "❌ Needs Improvement"
                        st.metric("Status", status)
                    with col3_val:
                        st.metric("Tool", selected_tool)
                    
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
                        tool=selected_tool,
                        task_type=st.session_state.task_context.task_type,
                        description=st.session_state.task_context.description,
                        stage=selected_stage
                    )
                    
                    if context_docs:
                        for i, doc in enumerate(context_docs[:3], 1):
                            st.write(f"**Context {i}:**")
                            st.write(f"*Source: {doc.metadata.get('source', 'Unknown')}*")
                            st.write(f"*Tool: {doc.metadata.get('tool', 'Unknown')}*")
                            st.text(doc.page_content[:300] + "...")
                            st.write("---")
                    else:
                        st.write("No relevant context found for this tool.")
            
            # Display prompt
            st.subheader(f"📝 Generated {selected_stage.title()} Prompt")
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📖 Formatted View", "📋 Raw Text"])
            
            with tab1:
                st.markdown(st.session_state.generated_prompt)
            
            with tab2:
                st.code(st.session_state.generated_prompt, language='markdown')
            
            # Export section
            st.subheader("📤 Export Options")
            
            col1_exp, col2_exp, col3_exp = st.columns(3)
            
            with col1_exp:
                if export_format == "Markdown":
                    export_content = st.session_state.generated_prompt
                    if include_metadata:
                        export_content = f"<!-- Tool: {selected_tool}, Stage: {selected_stage} -->\n\n{export_content}"
                    
                    st.download_button(
                        "💾 Download Markdown",
                        export_content,
                        file_name=f"{project_name.lower().replace(' ', '_')}_{selected_tool}_{selected_stage}_prompt.md",
                        mime="text/markdown"
                    )
            
            with col2_exp:
                if export_format == "JSON":
                    export_data = {
                        "tool": selected_tool,
                        "stage": selected_stage,
                        "project_info": {
                            "name": st.session_state.project_info.name,
                            "description": st.session_state.project_info.description,
                            "tech_stack": st.session_state.project_info.tech_stack,
                            "target_audience": st.session_state.project_info.target_audience,
                            "tool": st.session_state.project_info.tool
                        },
                        "task_context": {
                            "task_type": st.session_state.task_context.task_type,
                            "description": st.session_state.task_context.description,
                            "stage": st.session_state.task_context.stage,
                            "technical_requirements": st.session_state.task_context.technical_requirements,
                            "ui_requirements": st.session_state.task_context.ui_requirements,
                            "constraints": st.session_state.task_context.constraints,
                            "component_type": st.session_state.task_context.component_type
                        },
                        "generated_prompt": st.session_state.generated_prompt,
                        "timestamp": str(st.session_state.get('generation_time', 'Unknown'))
                    }
                    
                    st.download_button(
                        "💾 Download JSON",
                        json.dumps(export_data, indent=2),
                        file_name=f"{project_name.lower().replace(' ', '_')}_{selected_tool}_{selected_stage}_prompt.json",
                        mime="application/json"
                    )
            
            with col3_exp:
                if export_format == "Plain Text":
                    export_content = st.session_state.generated_prompt
                    if include_metadata:
                        export_content = f"Tool: {selected_tool}\nStage: {selected_stage}\n\n{export_content}"
                    
                    st.download_button(
                        "💾 Download Text",
                        export_content,
                        file_name=f"{project_name.lower().replace(' ', '_')}_{selected_tool}_{selected_stage}_prompt.txt",
                        mime="text/plain"
                    )

# Additional features section
def additional_features():
    """Display additional features and tools"""
    st.divider()
    
    st.header("🔧 Additional Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🔄 Batch Generation")
        if st.button("Generate All Stages"):
            st.info("Feature coming soon: Generate prompts for all stages at once")
    
    with col2:
        st.subheader("📊 Analytics")
        if st.button("View Tool Comparison"):
            st.info("Feature coming soon: Compare different tools for your project")
    
    with col3:
        st.subheader("💾 Save Templates")
        if st.button("Save as Template"):
            st.info("Feature coming soon: Save your configuration as a reusable template")

# Footer
def footer():
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <h4>🛠️ Multi-Tool Prompt Generator</h4>
        <p>Supports: Lovable.dev • Bolt.new • Bubble • FlutterFlow • Framer • Adalo • Uizard • and more!</p>
        <p>Built with Streamlit • Powered by RAG (Retrieval-Augmented Generation)</p>
        <p><em>Generate tool-specific prompts with stage-wise development precision</em></p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    additional_features()
    footer()
