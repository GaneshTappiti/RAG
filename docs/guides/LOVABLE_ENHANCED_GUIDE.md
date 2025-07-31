# Lovable.dev Enhanced Prompting Guidelines

## Core Principles from Lovable Documentation

### The C.L.E.A.R. Framework for Lovable

**Concise**: Direct, focused instructions without unnecessary fluff
- ❌ "Could you maybe write something about a task management feature?"
- ✅ "Create a task management component with CRUD operations, due dates, and status filtering."

**Logical**: Step-by-step, well-structured approach
- Break complex requests into ordered steps
- ❌ "Build me a user signup feature and also show some stats on usage."
- ✅ "First, implement a user sign-up form with email and password using Supabase. Then, after successful signup, display a dashboard showing user count statistics."

**Explicit**: State exactly what you want and don't want
- Provide examples of format or content
- ❌ "Tell me about user authentication."
- ✅ "Implement secure user authentication using Supabase Auth with email/password, including signup, login, logout, and protected routes. Use TypeScript for type safety."

**Adaptive**: Refine prompts based on results
- Engage in dialogue to improve outcomes
- "The solution you gave is missing the authentication step. Please include user auth in the code."

**Reflective**: Learn from each interaction
- Review what worked and what didn't
- Ask AI to summarize solutions for future reference

## Four Levels of Lovable Prompting

### 1. Structured "Training Wheels" Prompting

Use labeled sections for complex tasks:

```
Context: You are an expert full-stack developer using Lovable.
Task: Create a secure login page in React using Supabase (email/password auth).
Guidelines: The UI should be minimalistic, and follow Tailwind CSS conventions. Provide clear code comments for each step.
Constraints: Only modify the LoginPage component; do not change other pages. Ensure the final output is a working page in the Lovable editor.
```

### 2. Conversational Prompting

More natural communication while maintaining clarity:

```
Let's build a feature to upload a profile picture. It should include a form with an image file input and a submit button. When submitted, it should store the image in Supabase storage and update the user profile. Please write the necessary React component and any backend function needed for this, and ensure to handle errors (like file too large) gracefully.
```

### 3. Meta Prompting

Ask AI to improve your prompts:

```
Review my last prompt and identify any ambiguity or missing info. How can I rewrite it to be more concise and precise?
```

### 4. Reverse Meta Prompting

Use AI for documentation and learning:

```
Summarize the errors we encountered setting up JWT authentication and explain how we resolved them. Then, draft a prompt I could use in the future to avoid those mistakes when setting up auth.
```

## Lovable-Specific Best Practices

### Knowledge Base Optimization

Before any coding:

```markdown
Before writing any code, read the project Knowledge Base and confirm you understand the app's purpose and constraints.
```

Set up your Knowledge Base with:
- Project Requirements Document (PRD)
- User flows and tech stack details
- UI design guidelines
- Backend specifications
- Explicitly out-of-scope features

### Incremental Development

Break development into logical steps:

```markdown
❌ DON'T: "Build a CRM app with Supabase, auth, Google Sheets export, and data enrichment."

✅ DO:
1. "Set up a Supabase-connected CRM backend."
2. "Great! Could you please add a secure authentication flow with user roles?"
3. "Thank you! The next step is to integrate Google Sheets to export records."
```

### Specific and Constraint-Driven

Include clear constraints and requirements:

```markdown
Create a simple to-do app with a maximum of 3 tasks visible at a time.
Include the ability to add, edit, and delete tasks.
Use at most 3 API calls for this, and ensure no external library is required.
```

### Avoid Ambiguity

Be explicit about scope and expectations:

```markdown
❌ "Add a profile feature"
✅ "Add a user profile page with fields for name, email, bio, and profile picture upload."

❌ "Support notifications"
✅ "Send an email notification when a new task is assigned to a user."
```

## Advanced Lovable Techniques

### Image-Based Prompting

Lovable supports image uploads for design matching:

```markdown
Simple approach:
"Create and implement a UI that looks as similar as possible to the image attached."

Detailed approach:
"I want you to create the app as similar as possible to the one shown in this screenshot. It's essentially a kanban clone. It should have the ability to add new cards (tickets) in each column, have the ability to change the order of those tickets within a single column, and even move those cards between columns. Feel free to use the @dnd-kit/core npm package for drag-and-drop functionality."
```

### Precise Edit Instructions

Focus the AI on specific changes:

```markdown
In the Header component, change the signup button's text to 'Get Started' and move it to the left side of the nav bar. Do not modify any other components or logic unrelated to the header.
```

### Design and UI Tweaks

Be clear about visual vs. functional changes:

```markdown
Make the login button blue and 20% larger, but do not alter any of its functionality or onClick logic.

Optimize the landing page for mobile: use a mobile-first approach. Start by outlining how each section should rearrange on smaller screens, then implement those CSS changes. Use standard Tailwind breakpoints (sm, md, lg) and avoid custom breakpoints. Ensure nothing in functionality changes, just layout.
```

### Debugging with Lovable

Leverage Lovable's "Try to Fix" feature and AI assistance:

```markdown
Here's the error and relevant code snippet – what is causing this and how can we fix it?
[Include error logs and context]

The fix didn't work. The state is still undefined at runtime. What else could be wrong? Let's think through possible causes.
```

### Component Library Integration

Specify preferred libraries and patterns:

```markdown
Create a responsive navigation bar using the shadcn/ui library with Tailwind CSS for styling.

Generate a React component for a login form that follows accessibility best practices, including appropriate ARIA labels and keyboard navigation support.
```

## Zero-Shot vs. Few-Shot in Lovable

### Zero-Shot (No Examples)
Good for common patterns Lovable already knows:

```markdown
Create a user authentication system with email/password login using Supabase Auth.
```

### Few-Shot (With Examples)
Better for specific formats or styles:

```markdown
Correct the grammar in these sentences:
Input: "the code not working good" → Output: "The code is not working well."
Input: "API give error in login" → Output: "The API gives an error during login."
Now Input: "user not found in database" → Output:
```

## Managing Hallucinations in Lovable

### Provide Grounding Data
- Use the Knowledge Base extensively
- Include documentation snippets in prompts
- Reference specific APIs or data models

### Ask for Step-by-Step Reasoning
```markdown
Explain your solution approach before giving the final code. If there are any uncertainties, state them.
```

### Instruct Honesty
```markdown
If you are not sure of a fact or the correct code, do not fabricate it – instead, explain what would be needed or ask for clarification.
```

### Iterative Verification
```markdown
Confirm that the above code follows the requirements and explain any part that might not meet the spec.
```

## Lovable Mode Utilization

### Chat Mode
Use for:
- Brainstorming and planning
- Discussing design decisions
- Debugging without code changes
- Architecture discussions

```markdown
I want to add a blog section to my app. Let's discuss how to structure the data and pages.
```

### Default Mode
Use for:
- Implementing planned features
- Making direct code changes
- Creating components

```markdown
Create a BlogPost page and a Supabase table schema for blog posts based on the above plan.
```

## Common Lovable Patterns

### Project Structure Clarity
```markdown
Create a new React component named 'UserProfile' and save it as 'components/user-profile.tsx'. Ensure it includes a profile picture, username, and bio section.
```

### Accessibility Integration
```markdown
Generate a React component that follows accessibility best practices, including appropriate ARIA labels, keyboard navigation support, and semantic HTML structure.
```

### Multilingual Support
```markdown
Generate a Python script that calculates the Fibonacci sequence. Provide comments and documentation in French.
```

### Feedback Integration
```markdown
The login form looks good, but please add validation for the email field to ensure it contains a valid email address and show appropriate error messages.
```

## Example: Complete Lovable Project Prompt

```markdown
Context: You are building a task management SaaS application for small teams using Lovable.

Initial Setup Request:
Review the Knowledge Base which contains our PRD specifying a React + TypeScript + Tailwind + Supabase stack for a team productivity tool targeting 5-50 person teams.

Task: Create the foundational application structure starting with user authentication.

Requirements:
1. Implement Supabase Auth with email/password
2. Create protected routes using middleware
3. Design a clean, minimal login/signup interface using shadcn/ui
4. Include proper error handling and loading states
5. Ensure mobile-responsive design from the start

Constraints:
- Use TypeScript for all components
- Follow established Tailwind + shadcn/ui patterns
- Do not implement social login (explicitly out of scope)
- Maintain accessibility standards (ARIA labels, keyboard navigation)

Success Criteria:
- Users can sign up and log in successfully
- Protected routes redirect unauthenticated users
- Clean, professional UI that works on mobile and desktop
- Proper error messages for invalid credentials
- Loading states during authentication process

Next Steps Preview:
After authentication is working, we'll add the main dashboard and task management features incrementally.
```

This approach embodies all the Lovable best practices: structured context, clear constraints, specific technical requirements, and a logical progression toward the larger goal.
