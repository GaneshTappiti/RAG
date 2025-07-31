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
UIUX_PROMPT_TEMPLATE = """You are a senior UI/UX designer and full-stack product strategist with 10+ years of experience designing high-quality, scalable applications. You are also an expert in Prompt Engineering v4, applying techniques such as role-based thinking, user intent decoding, progressive breakdowns, and outcome-focused structuring.

---

🎯 Objective:
I will provide you with:
- An app idea (concept, goal, or description)
- The target user or audience

Your job is to break the idea down in a **3-Phase Process**, from concept to UI wireframes:

---

📦 Phase 1: Idea Expansion & Product Skeleton

1. **Understand & Reframe the Idea**  
   - Summarize my app idea in clear product language  
   - Add **unique value propositions** (if any gaps or obvious additions are spotted)  
   - Suggest **adjacent features** that logically extend the idea  
   - List the **core use cases** and problems this app solves

2. **Build the App Skeleton**  
   - List all major **pages/screens** needed  
   - For each screen:  
     - Give a **brief description** of the purpose  
     - Explain its **role in the user journey**  
   - Visualize **high-level navigation flow** (e.g. home → dashboard → profile)

---

� Phase 2: UI System Design (Per Screen Breakdown)

For each screen from Phase 1, generate:

```markdown
🖼️ **Page Name: [e.g., Home / Login / Profile]**

🔍 **Purpose:**
- [What user need this screen addresses]

� **Layout & Structure:**
- [Header, content sections, navigation, FABs]

🔘 **Main UI Elements:**
- [Inputs, buttons, cards, lists, toggles, etc.]

🔗 **Connections & Logic:**
- [Navigation, where each action leads, modal triggers, etc.]

✅ **UX Notes:**
- [Visual hierarchy, feedback, accessibility, mobile vs desktop tweaks]
```

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
1. Phase 1: Complete idea expansion and app skeleton
2. Phase 2: Detailed UI system design for each screen
3. Phase 3: Ready-to-implement wireframe specifications
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
