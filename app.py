"""
Web Application for AI Tool Prompt Generation
Description: Flask web app for generating UI/UX design prompts based on user inputs and tool selection
"""

import os
import sys
import json
from typing import Dict, List, Optional
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.core.types import SupportedTool, ProjectInfo, TaskContext, PromptStage
from src.generators.enhanced_generator import EnhancedMultiToolGenerator

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize the prompt generator
generator = EnhancedMultiToolGenerator()

# UI/UX Design Prompt Template
UIUX_PROMPT_TEMPLATE = """UI/UX Page-by-Page Design Plan for Cross-Device App

You are a senior UI/UX designer with 10+ years of experience designing responsive, production-ready interfaces for both mobile and desktop applications. — applying structured reasoning, role-based logic, and clean formatting to build scalable UI systems.

---

🎯 Objective:
Based on the app idea I give you, break down the entire user interface into individual pages. For each screen, provide a detailed UI layout description, component logic, user flow, and cross-device design adjustments.

Your job is to:
1. Break the app into all required screens (functional pages, onboarding, settings, etc.)
2. For each screen, describe:
   - Its **purpose**
   - **Layout and structure**
   - **Main UI components**
   - **Page connections and CTA flow**
   - Any **differences between desktop and mobile views**

---

🧠 Use this Format for Each Page:

🖼️ Page Name: [e.g., Dashboard]
🔍 Purpose:
[What user need this screen solves]
📐 Layout Structure:
Header: [Logo, nav links, user profile dropdown]
Main Content: [Card grid, lists, filters, inputs]
Sidebar (if desktop): [Nav links or quick actions]
Bottom Nav (if mobile): [Icon-based navigation]
📱 Mobile View Adjustments:
Stack content vertically
Replace sidebar with bottom nav or hamburger menu
Use modals for secondary actions (e.g., edit, filters)
💻 Desktop View Adjustments:
Use 2-3 column layout where possible
Persistent sidebar or floating panels
Table/grid views for dense data
🔘 Key UI Elements:
Buttons: ["Create Task", "Submit", etc.]
Cards/Lists: [What data they show, how they behave]
Inputs: [Search bars, dropdowns, form fields]
Feedback: [Toasts, alerts, success messages]
🔗 Page Connections:
[e.g., "Create Task" → goes to /create page]
["Edit" button opens modal → updates without navigation]
✅ UX Notes:
[Accessibility, mobile tap targets, font sizing]
[Visual hierarchy: Primary CTA, secondary actions]
[Consistency with color, typography, and spacing]

---

🏗️ Additional Instructions:
- Design every screen as mobile-first, then scale up to desktop
- Follow 4dp or 8dp spacing grid
- Stick to 1–2 primary CTAs per page
- Maintain consistent visual rhythm, alignment, and color palette

---

App Details:
- **App Name**: {app_name}
- **Platform**: {platform}
- **Design Style**: {design_style}
- **Style Description**: {style_description}
- **App Idea**: {app_idea}
- **Target Users**: {target_users}
- **Selected Tool**: {selected_tool}

Once I provide the app idea, return:
1. A list of all UI pages/screens
2. Each screen's layout + functionality using the format above
3. Logical UX flow from start to finish (from onboarding to dashboard to logout)
"""

@app.route('/')
def index():
    """Main page with tool selection and form"""
    # Get available tools
    tools = [
        {"value": tool.value, "name": tool.value.replace('_', ' ').title()} 
        for tool in SupportedTool
    ]
    return render_template('index.html', tools=tools)

@app.route('/generate', methods=['POST'])
def generate_prompt():
    """Generate UI/UX design prompt based on user input"""
    try:
        # Get form data
        app_name = request.form.get('app_name', '').strip()
        platform = request.form.get('platform', 'Web')
        design_style = request.form.get('design_style', 'Minimal')
        style_description = request.form.get('style_description', '').strip()
        app_idea = request.form.get('app_idea', '').strip()
        target_users = request.form.get('target_users', '').strip()
        selected_tool = request.form.get('selected_tool', 'lovable')
        
        # Validation
        if not app_name or not app_idea:
            return jsonify({
                'success': False,
                'error': 'App Name and App Idea are required fields.'
            })
        
        # Generate the UI/UX prompt
        generated_prompt = UIUX_PROMPT_TEMPLATE.format(
            app_name=app_name,
            platform=platform,
            design_style=design_style,
            style_description=style_description or "No additional style description provided",
            app_idea=app_idea,
            target_users=target_users or "General users",
            selected_tool=selected_tool.replace('_', ' ').title()
        )
        
        # Get tool-specific context from RAG system
        try:
            tool_enum = SupportedTool(selected_tool)
            
            # Create project info for RAG context
            project_info = ProjectInfo(
                name=app_name,
                description=app_idea,
                target_audience=target_users or "General users",
                industry=None,
                complexity_level="medium",
                tech_stack=[],
                requirements=[]
            )
            
            # Create task context for enhanced generator
            task_context = TaskContext(
                task_type="ui_design",
                project_name=app_name,
                description=app_idea,
                stage=PromptStage.PAGE_UI,
                technical_requirements=[],
                ui_requirements=[],
                constraints=[],
                target_tool=SupportedTool(selected_tool)
            )
            
            # Get enhanced prompt using the generator
            result = generator.generate_enhanced_prompt(task_context)
            
            # Combine the UI/UX prompt with enhanced context
            enhanced_prompt = f"""## Tool-Specific Context for {selected_tool.replace('_', ' ').title()}
{result.prompt}

---

{generated_prompt}

---

## Additional Guidance
Generated with confidence score: {result.confidence_score}
Applied strategy: {result.applied_strategy}
"""

        except Exception as e:
            print(f"Error getting tool context: {e}")
            enhanced_prompt = generated_prompt
        
        return jsonify({
            'success': True,
            'prompt': enhanced_prompt,
            'app_details': {
                'app_name': app_name,
                'platform': platform,
                'design_style': design_style,
                'style_description': style_description,
                'app_idea': app_idea,
                'target_users': target_users,
                'selected_tool': selected_tool
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

@app.route('/tools/<tool_name>')
def tool_info(tool_name):
    """Get information about a specific tool"""
    try:
        tool_enum = SupportedTool(tool_name)
        
        # Create a simple task context for tool info
        task_context = TaskContext(
            task_type="tool_info",
            project_name="Sample Project",
            description="Get tool information",
            stage=PromptStage.APP_SKELETON,
            technical_requirements=[],
            ui_requirements=[],
            constraints=[],
            target_tool=tool_enum
        )
        
        result = generator.generate_enhanced_prompt(task_context)
        
        return jsonify({
            'success': True,
            'tool_name': tool_name,
            'context': result.prompt,
            'confidence_score': result.confidence_score
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Tool not found: {str(e)}'
        })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(project_root, 'templates')
    static_dir = os.path.join(project_root, 'static')
    
    for directory in [templates_dir, static_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    print("🚀 Starting AI Tool Prompt Generator Web App...")
    print("📋 Available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
