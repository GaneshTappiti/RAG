"""
AI Tool Prompt Generator - Command Line Interface
Description: Generate UI/UX design prompts based on user inputs and tool selection
"""

import os
import sys
import json
from typing import Dict, List, Optional

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.core.types import SupportedTool

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

Based on this app idea, return:
1. A list of all UI pages/screens
2. Each screen's layout + functionality using the format above
3. Logical UX flow from start to finish (from onboarding to dashboard to logout)
"""

def collect_user_input():
    """Collect user inputs for UI/UX prompt generation"""
    print("🚀 AI Tool UI/UX Prompt Generator")
    print("=" * 60)
    
    # Tool Selection
    print("\n🛠️ AI Development Tool Selection")
    print("Available tools:")
    tools = list(SupportedTool)
    for i, tool in enumerate(tools, 1):
        print(f"{i:2d}. {tool.value.replace('_', ' ').title()}")
    
    while True:
        try:
            tool_choice = int(input(f"\nSelect development tool (1-{len(tools)}): ").strip())
            if 1 <= tool_choice <= len(tools):
                selected_tool = tools[tool_choice - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(tools)}")
        except ValueError:
            print("Please enter a valid number")
    
    print(f"Selected: {selected_tool.value.replace('_', ' ').title()}")
    
    # Frontend Input Collection
    print("\n📋 Frontend Input Collection")
    app_name = input("App Name: ").strip()
    if not app_name:
        print("❌ App Name is required!")
        return None
    
    print("\nPlatform:")
    print("1. Web")
    print("2. Mobile")
    print("3. Both (Cross-platform)")
    platform_choice = input("Select platform (1-3): ").strip()
    platform_map = {"1": "Web", "2": "Mobile", "3": "Both (Cross-platform)"}
    platform = platform_map.get(platform_choice, "Web")
    
    print("\nDesign Style:")
    print("1. Minimal")
    print("2. Fun")
    print("3. Business")
    print("4. Modern")
    print("5. Classic")
    style_choice = input("Select design style (1-5): ").strip()
    style_map = {"1": "Minimal", "2": "Fun", "3": "Business", "4": "Modern", "5": "Classic"}
    design_style = style_map.get(style_choice, "Minimal")
    
    style_description = input("Style Description (Optional): ").strip()
    
    app_idea = input("App Idea in Detail: ").strip()
    if not app_idea:
        print("❌ App Idea is required!")
        return None
    
    target_users = input("Target Users (Optional): ").strip()
    
    return {
        'app_name': app_name,
        'platform': platform,
        'design_style': design_style,
        'style_description': style_description,
        'app_idea': app_idea,
        'target_users': target_users,
        'selected_tool': selected_tool.value
    }

def generate_uiux_prompt(user_input):
    """Generate UI/UX design prompt based on user input"""
    try:
        # Generate the UI/UX prompt
        generated_prompt = UIUX_PROMPT_TEMPLATE.format(
            app_name=user_input['app_name'],
            platform=user_input['platform'],
            design_style=user_input['design_style'],
            style_description=user_input['style_description'] or "No additional style description provided",
            app_idea=user_input['app_idea'],
            target_users=user_input['target_users'] or "General users",
            selected_tool=user_input['selected_tool'].replace('_', ' ').title()
        )
        
        # Get tool-specific context from document files
        try:
            tool_context = get_tool_documentation_context(user_input['selected_tool'])
            
            # Combine the UI/UX prompt with tool-specific guidance
            enhanced_prompt = f"""## Tool-Specific Context for {user_input['selected_tool'].replace('_', ' ').title()}
{tool_context}

---

{generated_prompt}

---

## Additional Guidance
Please ensure the UI/UX design follows the best practices and capabilities of {user_input['selected_tool'].replace('_', ' ').title()} as outlined in the tool context above."""

        except Exception as e:
            print(f"⚠️ Warning: Could not get tool context: {e}")
            enhanced_prompt = generated_prompt
        
        return enhanced_prompt
        
    except Exception as e:
        print(f"❌ Error generating prompt: {e}")
        return None

def get_tool_documentation_context(tool_name):
    """Get documentation context for a specific tool"""
    tool_docs_map = {
        'lovable': 'data/lovable_docs',
        'bolt': 'data/bolt_docs', 
        'bubble': 'data/bubble_docs',
        'cline': 'data/cline_docs',
        'cursor': 'data/cursor_docs',
        'adalo': 'data/adalo_docs',
        'flutterflow': 'data/flutterflow_docs',
        'framer': 'data/framer_docs',
        'uizard': 'data/uizard_docs',
        'v0': 'data/v0_docs',
        'devin': 'data/devin_docs',
        'windsurf': 'data/windsurf_docs',
        'roocode': 'data/roocode_docs',
        'manus': 'data/manus_docs',
        'same_dev': 'data/same_docs'
    }
    
    docs_dir = tool_docs_map.get(tool_name)
    if not docs_dir or not os.path.exists(docs_dir):
        return f"Documentation for {tool_name.replace('_', ' ').title()} is not available. Please refer to the official documentation."
    
    # Try to read a few key documentation files
    context_parts = []
    
    # Common documentation filenames to look for
    doc_files = ['README.md', 'overview.md', 'getting-started.md', 'features.md', 'capabilities.md']
    
    for doc_file in doc_files:
        doc_path = os.path.join(docs_dir, doc_file)
        if os.path.exists(doc_path):
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()[:1000]  # Limit to first 1000 chars
                    context_parts.append(f"### {doc_file}\n{content}")
                break  # Just get the first available file
            except Exception as e:
                continue
    
    if context_parts:
        return "\n\n".join(context_parts)
    else:
        return f"Documentation for {tool_name.replace('_', ' ').title()} is available but could not be read. Please ensure proper file permissions."

def save_prompt_to_file(prompt, filename=None):
    """Save generated prompt to a file"""
    if not filename:
        filename = "generated_uiux_prompt.md"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"✅ Prompt saved to: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

def main():
    """Main application function"""
    try:
        # Collect user input
        user_input = collect_user_input()
        if not user_input:
            print("❌ Failed to collect required inputs. Exiting.")
            return
        
        print("\n" + "="*60)
        print("🎨 Generating UI/UX Design Prompt...")
        print("="*60)
        
        # Generate prompt
        prompt = generate_uiux_prompt(user_input)
        if not prompt:
            print("❌ Failed to generate prompt. Exiting.")
            return
        
        # Display prompt
        print("\n" + "📝 Generated UI/UX Design Prompt:")
        print("-" * 60)
        print(prompt)
        
        # Ask if user wants to save
        save_choice = input("\n💾 Save prompt to file? (y/n): ").strip().lower()
        if save_choice in ['y', 'yes']:
            filename = input("Enter filename (or press Enter for default): ").strip()
            if not filename:
                filename = f"uiux_prompt_{user_input['app_name'].replace(' ', '_').lower()}.md"
            save_prompt_to_file(prompt, filename)
        
        print("\n✅ Done! You can now use this prompt with your selected AI tool.")
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == '__main__':
    main()
