# Lovable.dev Prompting Guidelines

## Overview
Lovable.dev is an AI-powered development platform that excels at creating modern web applications. To get the best results, your prompts should be clear, specific, and follow proven patterns.

## Core Prompting Principles

### 1. Be Specific and Actionable
Instead of: "Make a website"
Use: "Create a React e-commerce site with product catalog, shopping cart, and Stripe checkout"

### 2. Define the Technology Stack
Always specify:
- Frontend framework (React, Vue, Next.js)
- Styling approach (Tailwind, CSS modules, styled-components)
- Backend requirements (API routes, database)
- Third-party integrations

### 3. Include UI/UX Requirements
- Layout structure and navigation
- Color scheme and branding
- Responsive behavior
- Interactive elements

### 4. Specify Functionality Clearly
Break down features into specific requirements:
- User authentication flows
- Data management (CRUD operations)
- Real-time features
- Integration points

## Prompt Structure Template

```
Context: [Brief project description]

Requirements:
- Feature 1: [Specific functionality]
- Feature 2: [Specific functionality]
- Feature 3: [Specific functionality]

Technical Stack:
- Frontend: [Framework/library]
- Styling: [CSS approach]
- Backend: [If needed]
- Database: [If needed]

UI/UX:
- Layout: [Description]
- Styling: [Design requirements]
- Responsive: [Mobile considerations]

Success Criteria:
- [Measurable outcome 1]
- [Measurable outcome 2]
```

## Best Practices

### DO:
- Start with a clear project vision
- Break complex features into smaller components
- Specify error handling requirements
- Include accessibility considerations
- Mention performance requirements
- Define user interaction patterns

### DON'T:
- Use vague language like "nice" or "good"
- Forget mobile responsiveness
- Ignore error states
- Skip loading states
- Overcomplicate single requests
- Forget about data validation

## Example Prompts

### Project Kickoff
"Create a modern blog platform using Next.js 14 and Tailwind CSS. Include a clean homepage with featured posts, individual post pages with MDX support, and an admin dashboard for content management. Use a minimal, typography-focused design with dark mode support."

### UI Enhancement
"Improve the current dashboard layout to be fully responsive. The sidebar should collapse to a hamburger menu on mobile, cards should stack vertically on tablets, and the main content area should use a CSS Grid layout with proper gap spacing."

### API Integration
"Add Stripe payment integration to the checkout flow. Include payment form validation, error handling for failed payments, success confirmation page, and webhook handling for payment status updates. Ensure PCI compliance and proper error messaging."
