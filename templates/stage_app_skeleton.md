# Multi-Stage App Skeleton Generator - {{ project_info.name }}

**Tool:** {{ tool_profile.tool_name }}
**Stage:** Application Structure & Foundation
**Target:** Build complete app architecture

## 🎯 Project Overview
**Name:** {{ project_info.name }}
**Description:** {{ project_info.description }}
**Industry:** {{ project_info.industry | default("General") }}
**Complexity:** {{ project_info.complexity_level.title() }}
**Tech Stack:** {{ project_info.tech_stack | join(', ') }}
**Target Audience:** {{ project_info.target_audience }}

## 📋 App Structure Requirements

### Core Pages
{% if task_context.app_structure and task_context.app_structure.pages %}
{% for page in task_context.app_structure.pages %}
- **{{ page }}**: {{ loop.index }}. Primary user interface
{% endfor %}
{% else %}
Based on the project description, create these essential pages:
- Landing/Home page with hero section
- Main dashboard/workspace
- User authentication (login/signup)
- Settings/profile management
{% endif %}

### Key Features
{% if task_context.app_structure and task_context.app_structure.features %}
{% for feature in task_context.app_structure.features %}
- {{ feature }}
{% endfor %}
{% else %}
{% for req in task_context.technical_requirements %}
- {{ req }}
{% endfor %}
{% endif %}

### Navigation Structure
{% if task_context.app_structure and task_context.app_structure.navigation_flow %}
{% for page, connections in task_context.app_structure.navigation_flow.items() %}
**{{ page }}** connects to:
{% for connection in connections %}
  - {{ connection }}
{% endfor %}
{% endfor %}
{% else %}
Create logical navigation flow:
- Header navigation for main sections
- Footer with secondary links
- Breadcrumb navigation for deep pages
- Mobile-friendly hamburger menu
{% endif %}

## ⚙️ Technical Foundation

### Architecture Requirements
{% for req in task_context.technical_requirements %}
- {{ req }}
{% endfor %}

### UI/UX Foundations
{% for req in task_context.ui_requirements %}
- {{ req }}
{% endfor %}

### Development Constraints
{% for constraint in task_context.constraints %}
- {{ constraint }}
{% endfor %}

## 🚀 Implementation Instructions

### Step 1: Project Setup
```
Initialize {{ project_info.tech_stack[0] | default("Next.js") }} project with:
- Proper folder structure (/components, /pages, /utils, /styles)
- Essential dependencies and configurations
- Environment setup for development
```

### Step 2: Core Layout System
```
Create main layout components:
- Header with navigation and branding
- Footer with links and contact info
- Sidebar (if applicable)
- Main content wrapper with proper responsive grid
```

### Step 3: Page Structure
```
Build page scaffolding for each core page:
- Route structure and navigation
- Basic layouts without detailed components
- Placeholder content and spacing
- Responsive breakpoints
```

### Step 4: Global Styling
```
Establish design system:
- Color palette and typography
- Component spacing and sizing standards
- Animation and transition patterns
- Mobile-first responsive approach
```

## 📱 Responsive Design Requirements

- **Mobile (320px-768px)**: Single column, touch-optimized
- **Tablet (768px-1024px)**: Two-column layout where appropriate
- **Desktop (1024px+)**: Full multi-column experience

## ♿ Accessibility Standards

- WCAG 2.1 AA compliance
- Proper heading hierarchy (h1-h6)
- Alt text for all images
- Keyboard navigation support
- Screen reader compatibility

## 🎨 Design Guidelines

Follow {{ tool_profile.tool_name }} best practices:
- {{ tool_profile.tone }} design approach
- Clean, modern interface patterns
- Consistent spacing and typography
- Intuitive user interactions

## ✅ Success Criteria

- [ ] All core pages load successfully
- [ ] Navigation works across all breakpoints
- [ ] Design system is consistently applied
- [ ] App structure supports planned features
- [ ] Performance metrics meet standards (< 2s load time)

## 🔄 Next Stage Preparation

After completing the app skeleton:
1. **Page UI Stage**: Design detailed page interfaces
2. **Feature Implementation**: Add specific functionality
3. **Flow Connections**: Link pages with smooth transitions

---

**Output Format:** Clean, implementable {{ tool_profile.format }} following {{ tool_profile.tool_name }} conventions
**Implementation Focus:** Structure first, polish later - ensure solid foundation for iterative development
