# Bolt.new Enhanced Prompting Guidelines

## Core Principles from Bolt.new Documentation

### Built-in Enhancement Feature

Bolt.new provides an automatic prompt enhancement feature:

1. Write your initial prompt in the chatbox
2. Click "Enhance prompt" ⭐ 
3. Bolt generates a detailed, optimized prompt
4. Edit the enhanced version as needed

### Progressive Development Approach

**Start with Architecture:**
Begin with the overall application structure, including your choice of tools, frameworks, and technology stack.

**Add Components Incrementally:**
Add individual components and features one by one, avoiding overwhelming the LLM with too many instructions at once.

**Detail with Specific Prompts:**
Add details to each component with small, specific prompts focused on particular aspects.

## Bolt.new Specific Optimization Strategies

### Explicit Change Control

Be very specific about what should and shouldn't change:

```markdown
✅ Good Practices:
"Change the header background color to blue, but do not modify the navigation links or logo"
"Add a new sidebar component without affecting the main content area layout"
"Update the login form validation while preserving all existing form fields"

❌ Avoid:
"Make the page look better"
"Fix the styling"
"Update the component"
```

### File and Directory Management

#### Target Specific Files
1. Right-click files you want to focus on in the Bolt Code editor
2. Select "Target file"

#### Exclude Files/Directories
1. Right-click files or directories you want to exclude
2. Select "Lock file" (single file) or "Lock all" (directory)

#### Focus on Code Sections
1. Switch to Code view
2. Highlight the specific code section
3. Click "Ask Bolt" button
4. Enter your request for that specific section

#### Focus on UI Elements
1. In Preview view, click Inspector 🔍
2. Click the UI element you want to modify
3. Bolt links the selection in the prompt box
4. Enter your modification request

### WebContainer Awareness

Bolt operates in a WebContainer environment with specific limitations:

```markdown
Environment Constraints:
- Browser-based Node.js runtime (not full Linux system)
- No native binary execution
- Limited to JavaScript, WebAssembly, and browser-compatible code
- Python standard library only (no pip support)
- Cannot install system-level packages

Optimization for WebContainer:
- Use web-based alternatives to native tools
- Leverage browser APIs when possible
- Focus on JavaScript/TypeScript solutions
- Avoid system-dependent operations
```

## Bolt.new Prompting Patterns

### Enhanced Base Patterns

Transform simple requests into detailed specifications:

```markdown
Basic Prompt:
"Create a todo app"

Enhanced for Bolt:
"Create a React todo application with TypeScript, featuring task creation, editing, deletion, and filtering. Include local storage persistence, responsive design with Tailwind CSS, and accessibility features. Implement proper state management and error handling."
```

### Troubleshooting Common Issues

#### When Bolt Doesn't Complete Everything
Break changes into smaller pieces:

```markdown
Instead of: "Add user authentication, dashboard, and notification system"

Do This:
1. "Add user authentication with login/logout functionality"
2. Check if authentication works properly
3. "Create a user dashboard with basic layout"
4. Verify dashboard displays correctly
5. "Add notification system to the dashboard"
```

#### When Bolt Forgets Context
The context window isn't infinite. Use summarization:

```markdown
Context Reset Pattern:
"Please summarize our conversation so far, including the key features we've implemented and the current state of the application. Then let's continue with [next task]."
```

### Project and System Prompts

#### Project Prompt Configuration
Access via: Settings > Knowledge > Project Prompt

Example optimized project prompt:
```markdown
For all designs I ask you to make, have them be beautiful, not cookie cutter. Make webpages that are fully featured and worthy for production.

By default, this template supports JSX syntax with Tailwind CSS classes, the shadcn/ui library, React hooks, and Lucide React for icons. Do not install other packages for UI themes, icons, etc unless absolutely necessary or I request them.

Use icons from lucide-react for logos.
Use stock photos from unsplash where appropriate.
Include instructions to Bolt to only change relevant code.
```

#### Global System Prompt
Apply consistent behavior across all projects:

```markdown
Always prioritize:
1. Clean, maintainable code
2. Responsive design principles
3. Accessibility compliance
4. Performance optimization
5. Security best practices

Default to TypeScript when possible.
Use semantic HTML structure.
Implement proper error boundaries.
Include loading states for async operations.
```

## Advanced Bolt.new Techniques

### Chain-of-Thought Prompting

Bolt benefits from understanding your implementation approach:

```markdown
Implementation Plan:
1. Set up the basic component structure
2. Add state management for todo items
3. Implement CRUD operations
4. Add filtering and sorting
5. Style with Tailwind CSS
6. Add local storage persistence

Now implement step 1: Create the basic todo component structure with TypeScript interfaces for todo items.
```

### Iterative Refinement

Use Bolt's conversational nature for improvements:

```markdown
First Implementation:
"Create a basic todo list component"

Refinement Cycle:
"The todo list looks good. Now add the ability to mark items as complete with a checkbox"
"Perfect! Now add a filter to show only incomplete items"
"Great! Add a delete button for each todo item"
"Excellent! Now style it with Tailwind to look modern and professional"
```

### Error-Driven Development

When errors occur, provide comprehensive context:

```markdown
Error Analysis Prompt:
"I'm seeing this error: [exact error message]

Current code context:
[relevant code snippet]

What I was trying to do:
[specific functionality being implemented]

Environment details:
[browser, any recent changes]

Please analyze the error and provide a fix that maintains all existing functionality."
```

## Bolt.new Best Practices Summary

### Pre-Development Setup
1. Configure project prompt with tech stack preferences
2. Set global system prompt for consistent behavior
3. Plan the development phases before starting

### During Development
1. Use the enhance prompt feature for complex requests
2. Target specific files to avoid unintended changes
3. Lock critical files that shouldn't be modified
4. Break complex features into incremental steps
5. Test functionality after each major change

### Code Quality Maintenance
1. Request TypeScript for better type safety
2. Ask for responsive design implementation
3. Include accessibility considerations
4. Implement proper error handling
5. Add loading states for better UX

### Debugging and Refinement
1. Provide complete error context
2. Use iterative refinement for improvements
3. Reset context when conversations get too long
4. Focus on specific UI elements using Inspector mode

## Example: Complete Bolt.new Development Session

```markdown
Session Start:
"I want to create a task management application. Let me enhance this prompt first."

Enhanced Prompt (after using ⭐):
"Create a comprehensive task management application using React with TypeScript, Tailwind CSS, and the shadcn/ui component library. The app should include:

Core Features:
- Task creation with title, description, due date, and priority levels
- Task editing and deletion functionality
- Task status management (todo, in-progress, completed)
- Task filtering by status and priority
- Task search functionality

UI/UX Requirements:
- Modern, clean interface using shadcn/ui components
- Fully responsive design for mobile and desktop
- Dark/light theme support
- Intuitive drag-and-drop for task reordering
- Loading states and error handling

Technical Specifications:
- TypeScript for type safety
- Local storage for data persistence
- Proper form validation
- Accessibility compliance (ARIA labels, keyboard navigation)
- Performance optimized with React best practices

Please start with the basic application structure and core task model."

Follow-up Prompts:
1. [After basic structure] "Great! Now implement the task creation form with validation"
2. [After form] "Perfect! Add the task list display with filtering options"
3. [After list] "Excellent! Now add drag-and-drop reordering functionality"
4. [After drag-drop] "Add the dark/light theme toggle and persist user preference"
```

This approach maximizes Bolt.new's capabilities while maintaining code quality and development efficiency.
