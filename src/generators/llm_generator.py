"""
LLM Response Generator for UI/UX Design Prompts
Integrates with your existing RAG system to generate actual responses
"""

import os
from typing import Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMUIGenerator:
    """Generate actual UI/UX responses using LLM"""
    
    def __init__(self):
        # Set up Gemini model
        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=os.environ.get('GOOGLE_API_KEY', '')
        )
        
        # System message for UI/UX generation
        self.system_prompt = """You are a top-tier senior UI/UX designer working at Lovable.dev with 10+ years of experience designing responsive, production-ready interfaces for both mobile and desktop applications.

Your job is to convert app ideas into detailed screen-by-screen UI design plans for cross-platform apps.

CRITICAL FORMATTING REQUIREMENTS:
- Use EXACTLY the emoji format provided in the example
- Include ALL required sections for each page
- Be exhaustive and precise
- Respond ONLY with structured design output
- Follow the exact markdown format and emoji patterns

Your expertise includes:
- Modern design systems and patterns  
- Cross-platform responsive design
- User experience optimization
- Accessibility best practices
- Component-based architecture

When given an app idea, you MUST respond with a comprehensive UI/UX design plan that follows the EXACT format shown in the example. Do not deviate from the emoji structure."""

    def generate_ui_response(self, prompt: str, app_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate actual UI/UX design response using LLM
        
        Args:
            prompt: The formatted prompt template
            app_details: Application details for context
            
        Returns:
            Dict with generated response and metadata
        """
        try:
            # Create few-shot example for better results
            few_shot_example = self._get_few_shot_example()
            
            # Combine system message, few-shot example, and user prompt
            full_prompt = f"""{self.system_prompt}

## REQUIRED OUTPUT FORMAT EXAMPLE:

{few_shot_example}

## IMPORTANT INSTRUCTIONS:
1. Use the EXACT emoji format shown above (🖼️, 🔍, 📐, 📱, 💻, 🔘, 🔗, ✅)
2. Include ALL sections for each page: Purpose, Layout Structure, Mobile/Desktop adjustments, UI Elements, Page Connections, UX Notes
3. Design AT LEAST 3-5 pages for a complete app
4. Be specific and actionable in every section
5. Follow the exact formatting structure

## NOW GENERATE THE SAME DETAILED BREAKDOWN FOR THE FOLLOWING APP:

{prompt}

Remember: Use the EXACT emoji format and include all required sections!"""

            # Generate response using Gemini
            messages = [HumanMessage(content=full_prompt)]
            response = self.model.invoke(messages)
            
            # Extract and format response
            generated_content = response.content
            
            return {
                'success': True,
                'generated_ui_design': generated_content,
                'app_details': app_details,
                'model_used': 'gemini-1.5-flash',
                'prompt_length': len(prompt),
                'response_length': len(generated_content)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"LLM Generation Error: {str(e)}",
                'app_details': app_details
            }
    
    def _get_few_shot_example(self) -> str:
        """Provide a few-shot example for better LLM responses"""
        return """📱 **Task Manager App Example**

## 📋 All Required Screens:
1. **Login/Signup** - User authentication
2. **Dashboard** - Main task overview  
3. **Create Task** - New task form
4. **Task Details** - Individual task view
5. **Settings** - User preferences

---

🖼️ **Page Name**: Dashboard
🔍 **Purpose**: 
Main hub where users view, manage, and track their tasks with quick actions and status overview

📐 **Layout Structure**:
Header: Logo, search bar, user profile dropdown, notification bell
Main Content: Task grid/list with filters (All, Today, Upcoming, Completed)
Sidebar (desktop): Quick actions (New Task, Categories, Calendar view)
Bottom Nav (mobile): Dashboard, Create, Calendar, Profile

📱 **Mobile View Adjustments**:
- Stack task cards vertically in single column
- Replace sidebar with bottom navigation
- Search becomes expandable from header icon
- Filters accessible via horizontal scroll tabs

💻 **Desktop View Adjustments**:
- 3-column layout: sidebar, main content, task details panel
- Table view option for dense task data
- Drag-and-drop task reordering
- Persistent quick action panel

🔘 **Key UI Elements**:
Buttons: ["+ New Task", "Filter", "Sort", "View Toggle"]
Cards: Task cards showing title, due date, priority, progress bar
Inputs: Search bar with autocomplete, filter dropdowns
Feedback: Toast notifications for task updates, progress indicators

🔗 **Page Connections**:
"+ New Task" → navigates to /create-task
Task card click → opens /task/:id detail view
Filter selection → updates current view with filtered results
Profile dropdown → Settings page or logout

✅ **UX Notes**:
- Use color coding for priority levels (Red: High, Yellow: Medium, Green: Low)
- Implement infinite scroll for large task lists
- Add keyboard shortcuts for power users (Ctrl+N for new task)
- Ensure 44px minimum touch targets on mobile
- Use consistent 8px spacing grid throughout

---

🖼️ **Page Name**: Create Task
🔍 **Purpose**: 
Allow users to quickly add new tasks with proper categorization and priority settings

📐 **Layout Structure**:
Header: Back button, "Create Task" title, Save button
Main Content: Form with task title, description, due date, priority, category
Footer: Cancel and Create buttons

📱 **Mobile View Adjustments**:
- Full-screen modal overlay
- Large touch-friendly form inputs
- Date picker optimized for mobile
- Sticky header with save/cancel actions

💻 **Desktop View Adjustments**:
- Centered modal dialog (600px width)
- Keyboard shortcuts (Enter to save, Esc to cancel)
- Auto-focus on task title field
- Inline validation messages

🔘 **Key UI Elements**:
Buttons: ["Cancel", "Create Task", "Save Draft"]
Inputs: Text field (title), textarea (description), date picker, priority dropdown, category selector
Forms: Validation states, required field indicators

🔗 **Page Connections**:
"Cancel" → returns to Dashboard
"Create Task" → saves and returns to Dashboard with success message
"Save Draft" → saves incomplete task and returns to Dashboard

✅ **UX Notes**:
- Auto-save draft every 30 seconds
- Clear validation feedback for required fields
- Quick category creation from this form
- Default due date to today + 1 day"""

    def validate_response_quality(self, response: str) -> Dict[str, Any]:
        """
        Validate the quality of the generated response
        
        Args:
            response: Generated UI/UX response
            
        Returns:
            Quality metrics and validation results
        """
        metrics = {
            'has_page_sections': '🖼️ Page Name:' in response,
            'has_layout_structure': '📐 Layout Structure:' in response,
            'has_mobile_adjustments': '📱 Mobile View' in response,
            'has_desktop_adjustments': '💻 Desktop View' in response,
            'has_ui_elements': '🔘 Key UI Elements:' in response,
            'has_page_connections': '🔗 Page Connections:' in response,
            'has_ux_notes': '✅ UX Notes:' in response,
            'response_length': len(response),
            'estimated_pages': response.count('🖼️ Page Name:')
        }
        
        # Calculate quality score
        structure_score = sum([
            metrics['has_page_sections'],
            metrics['has_layout_structure'], 
            metrics['has_mobile_adjustments'],
            metrics['has_desktop_adjustments'],
            metrics['has_ui_elements'],
            metrics['has_page_connections'],
            metrics['has_ux_notes']
        ]) / 7
        
        length_score = min(metrics['response_length'] / 2000, 1.0)  # Target ~2000+ chars
        page_score = min(metrics['estimated_pages'] / 3, 1.0)  # Target 3+ pages
        
        overall_quality = (structure_score * 0.6 + length_score * 0.2 + page_score * 0.2)
        
        return {
            **metrics,
            'structure_score': structure_score,
            'length_score': length_score,
            'page_score': page_score,
            'overall_quality_score': overall_quality,
            'quality_rating': self._get_quality_rating(overall_quality)
        }
    
    def _get_quality_rating(self, score: float) -> str:
        """Convert quality score to rating"""
        if score >= 0.9:
            return "Excellent"
        elif score >= 0.7:
            return "Good"
        elif score >= 0.5:
            return "Fair"
        else:
            return "Needs Improvement"
