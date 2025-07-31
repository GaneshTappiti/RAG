# Page UI Generator - {{ page_spec.page_name if page_spec else "Page Interface" }}

**Tool:** {{ tool_profile.tool_name }}
**Stage:** Detailed Page Interface Design
**Target:** Create polished, interactive page UI

## 🎯 Page Overview

{% if page_spec %}
**Page:** {{ page_spec.page_name }}
**Layout Type:** {{ page_spec.layout_type }}
{% else %}
**Page:** {{ task_context.description | default("Page Interface") }}
**Layout Type:** Responsive modern design
{% endif %}

**Project:** {{ project_info.name }}
**Tech Stack:** {{ project_info.tech_stack | join(', ') }}

## 📱 Layout Structure

{% if page_spec and page_spec.layout_type %}
### {{ page_spec.layout_type.title() }} Layout

{% if page_spec.layout_type == "dashboard" %}
Create a dashboard layout with:

- **Header**: Navigation bar with user profile and notifications
- **Sidebar**: Main navigation menu (collapsible on mobile)
- **Main Content**: Grid layout for widgets/cards
- **Footer**: Status information and quick actions

{% elif page_spec.layout_type == "form" %}
Create a form-focused layout with:

- **Form Container**: Centered with proper spacing
- **Field Groups**: Logical grouping of related inputs
- **Validation**: Real-time feedback and error states
- **Actions**: Clear primary and secondary buttons

{% elif page_spec.layout_type == "list" %}
Create a list/table layout with:

- **Header**: Search, filters, and bulk actions
- **List Items**: Cards or rows with key information
- **Pagination**: Navigation for large datasets
- **Empty States**: Meaningful placeholders

{% else %}
Create a flexible layout with:

- **Header Section**: Page title and primary actions
- **Content Area**: Main page functionality
- **Supporting Elements**: Secondary information and actions
{% endif %}

{% else %}
### Responsive Page Layout

Design a modern page interface with:

- **Header Section**: Clear page title and context
- **Main Content Area**: Primary functionality and information
- **Sidebar/Aside**: Supporting information (if needed)
- **Footer Section**: Secondary actions and information
{% endif %}

## 🧩 Component Requirements

{% if page_spec and page_spec.components %}
### Required Components

{% for component in page_spec.components %}
- **{{ component }}**: Interactive element with proper states
{% endfor %}
{% else %}
### Essential Components

{% for req in task_context.ui_requirements %}
- {{ req }}
{% endfor %}
{% endif %}

### Component States

For each interactive component, include:

- **Default State**: Normal appearance and behavior
- **Hover State**: Visual feedback on mouse over
- **Active State**: Response to user interaction
- **Loading State**: Progress indicators during operations
- **Error State**: Clear error messaging and recovery options
- **Disabled State**: Inactive appearance when not available

## ⚡ Interactions & Behavior

{% if page_spec and page_spec.interactions %}
### Page Interactions

{% for interaction in page_spec.interactions %}
- {{ interaction }}
{% endfor %}
{% else %}
### Core Interactions

- **Navigation**: Smooth transitions between sections
- **Form Handling**: Real-time validation and submission
- **Data Display**: Loading states and error handling
- **User Feedback**: Success messages and notifications
{% endif %}

### Micro-Interactions

- **Button Animations**: Subtle hover and click effects
- **Loading Spinners**: Smooth progress indicators
- **Toast Notifications**: Non-intrusive status updates
- **Form Validation**: Instant feedback on input changes

## 📊 Data Requirements

{% if page_spec and page_spec.data_requirements %}
### Data Integration

{% for data_req in page_spec.data_requirements %}
- {{ data_req }}
{% endfor %}
{% else %}
### Data Handling

- **API Integration**: Proper error handling and retries
- **State Management**: Consistent data flow
- **Caching Strategy**: Optimal performance
- **Real-time Updates**: Live data synchronization (if needed)
{% endif %}

## 📱 Responsive Design

### Breakpoint Specifications

- **Mobile (< 768px)**:
  - Single column layout
  - Touch-optimized buttons (min 44px)
  - Simplified navigation
  - Stacked form elements

- **Tablet (768px - 1024px)**:
  - Two-column layout where appropriate
  - Balanced content distribution
  - Hybrid navigation patterns

- **Desktop (> 1024px)**:
  - Full multi-column experience
  - Hover states and interactions
  - Dense information display

## 🎨 Visual Design

### Design System Application

- **Typography**: Clear hierarchy with {{ project_info.tech_stack[0] | default("modern") }} fonts
- **Color Scheme**: Consistent with brand identity
- **Spacing**: Proper margins and padding for readability
- **Shadows & Borders**: Subtle depth and separation

### Visual Hierarchy

1. **Primary Elements**: Most important actions and information
2. **Secondary Elements**: Supporting content and navigation
3. **Tertiary Elements**: Metadata and helper text

## ♿ Accessibility Features

- **Keyboard Navigation**: Full functionality without mouse
- **Screen Reader Support**: Proper ARIA labels and roles
- **Color Contrast**: WCAG AA compliance for all text
- **Focus Indicators**: Clear visual focus states
- **Alternative Text**: Descriptive alt text for images

## ⚙️ Technical Implementation

### Required Functionality

{% for req in task_context.technical_requirements %}
- {{ req }}
{% endfor %}

### Performance Requirements

- **Load Time**: Page ready in under 2 seconds
- **Interactive**: First meaningful interaction within 1 second
- **Smooth Animations**: 60fps for all transitions
- **Optimized Assets**: Compressed images and minified code

## ✅ Success Criteria

- [ ] Page loads quickly and smoothly
- [ ] All interactive elements work correctly
- [ ] Responsive design works across all devices
- [ ] Accessibility standards are met
- [ ] Visual design matches project requirements
- [ ] User flows are intuitive and efficient

## 🔄 Next Stage Options

After completing page UI:

1. **Flow Connections**: Link this page to others with navigation
2. **Feature Enhancement**: Add advanced functionality
3. **Performance Optimization**: Improve loading and interactions
4. **Additional Pages**: Create more interfaces using this as template

---

**Output Format:** Clean, implementable {{ tool_profile.format }} code with {{ tool_profile.tool_name }} best practices
**Focus:** User experience first - ensure intuitive, accessible, and performant interface
