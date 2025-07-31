# Flow Connections Generator - {{ project_info.name }}

**Tool:** {{ tool_profile.tool_name }}
**Stage:** Navigation & User Flow Mapping
**Target:** Connect pages with smooth, intuitive transitions

## 🎯 Flow Overview

**Project:** {{ project_info.name }}
**Focus:** Creating seamless user journeys between pages
**Tech Stack:** {{ project_info.tech_stack | join(', ') }}

## 🔗 Connection Mapping

{% if task_context.flow_connections %}
### Defined Flow Connections

{% for connection in task_context.flow_connections %}
**{{ connection.from_page }}** → **{{ connection.to_page }}**

- **Trigger:** {{ connection.trigger }}
{% if connection.animation %}
- **Animation:** {{ connection.animation }}
{% endif %}
{% if connection.conditions %}
- **Conditions:**
{% for condition in connection.conditions %}
  - {{ condition }}
{% endfor %}
{% endif %}

---
{% endfor %}
{% else %}
### Core Navigation Flows

Based on the app structure, implement these key connections:

**Landing Page** → **Dashboard**
- Trigger: "Get Started" button click
- Animation: Slide right transition
- Condition: User authentication check

**Dashboard** → **Feature Pages**
- Trigger: Navigation menu selection
- Animation: Fade in/out
- Condition: User permissions

**Any Page** → **Settings**
- Trigger: Settings icon click
- Animation: Modal overlay
- Condition: User logged in

**Forms** → **Confirmation**
- Trigger: Form submission success
- Animation: Success slide up
- Condition: Validation passed
{% endif %}

## 🎭 Transition Specifications

### Animation Guidelines

**Page Transitions:**
- **Duration:** 300-500ms for optimal UX
- **Easing:** cubic-bezier(0.4, 0.0, 0.2, 1) for natural feel
- **Direction:** Logical flow (left/right for navigation, up/down for modals)

**Component Transitions:**
- **Hover Effects:** 150ms for immediate feedback
- **Loading States:** Skeleton screens or spinners
- **Success/Error:** Gentle bounce or slide animations

### Responsive Transition Behavior

**Mobile Devices:**
- Simplified animations to preserve performance
- Touch-friendly swipe gestures
- Reduced motion for accessibility

**Desktop/Tablet:**
- Full animation suite
- Hover state transitions
- Smooth page transitions

## 🧭 Navigation Patterns

### Primary Navigation

```javascript
// Main navigation structure
const navigationFlow = {
  header: {
    logo: 'home',
    menu: ['dashboard', 'features', 'settings'],
    userProfile: 'profile-dropdown'
  },
  sidebar: {
    main: ['dashboard', 'projects', 'analytics'],
    secondary: ['settings', 'help', 'logout']
  }
}
```

### Secondary Navigation

**Breadcrumbs:**
- Show current page hierarchy
- Clickable parent levels
- Automatic generation from route structure

**In-Page Navigation:**
- Tab navigation for sections
- Anchor links for long content
- Previous/Next for sequential flows

## 🔄 User Journey Flows

### Authentication Flow

1. **Landing Page** → Login Modal
2. **Login Success** → Dashboard (with welcome animation)
3. **Login Failed** → Error state (shake animation)
4. **Signup Flow** → Email verification → Welcome sequence

### Feature Discovery Flow

1. **Dashboard** → Feature card click
2. **Feature Page** → Tutorial overlay (first time)
3. **Feature Usage** → Progress indicators
4. **Completion** → Success feedback → Next steps

### Error Recovery Flow

1. **Error Occurrence** → Error boundary catch
2. **Error Display** → Clear message with actions
3. **Recovery Action** → Retry or alternative path
4. **Success Recovery** → Return to intended flow

## 🎯 Interactive Elements

### Button Behaviors

**Primary Actions:**
- Clear visual hierarchy
- Loading states during operations
- Success/failure feedback
- Disabled states when appropriate

**Secondary Actions:**
- Subtle hover effects
- Clear labeling
- Consistent placement
- Accessible focus states

### Form Flow Connections

**Multi-Step Forms:**
- Progress indicators
- Save draft functionality
- Back/forward navigation
- Clear step transitions

**Form Validation:**
- Real-time field validation
- Summary error messages
- Focus management on errors
- Clear success confirmations

## 📱 Mobile Flow Considerations

### Touch Interactions

- **Swipe Gestures:** Back navigation, tab switching
- **Pull to Refresh:** Data reload in list views
- **Long Press:** Context menus and shortcuts
- **Pinch/Zoom:** Image and map interactions

### Mobile-Specific Transitions

- **Bottom Sheet:** Modal presentations
- **Tab Bar:** Quick navigation between main sections
- **Stack Navigation:** iOS-style page transitions
- **Drawer Navigation:** Side menu for secondary options

## ⚡ Performance Optimization

### Lazy Loading

```javascript
// Route-based code splitting
const LazyPage = lazy(() => import('./pages/FeaturePage'));

// Component-based lazy loading
const LazyModal = lazy(() => import('./components/Modal'));
```

### Preloading Strategies

- **Critical Path:** Load essential pages immediately
- **Predictive Loading:** Preload likely next pages
- **Intersection Observer:** Load content as user scrolls
- **Service Worker:** Cache frequently accessed routes

## 🔧 Implementation Guidelines

### Route Management

{% if 'Next.js' in project_info.tech_stack %}
**Next.js App Router:**
```javascript
// app/layout.js - Root layout with navigation
// app/page.js - Home page
// app/dashboard/page.js - Dashboard
// app/dashboard/[slug]/page.js - Dynamic routes
```
{% elif 'React' in project_info.tech_stack %}
**React Router:**
```javascript
// Route configuration with transitions
<Routes>
  <Route path="/" element={<Landing />} />
  <Route path="/dashboard" element={<Dashboard />} />
  <Route path="/feature/:id" element={<FeaturePage />} />
</Routes>
```
{% endif %}

### State Management

**Navigation State:**
- Current page tracking
- History management
- User flow analytics
- Breadcrumb generation

**Transition State:**
- Loading indicators
- Animation coordination
- Error boundary handling
- User preference storage

## ♿ Accessibility in Navigation

### Keyboard Navigation

- **Tab Order:** Logical flow through interactive elements
- **Skip Links:** Jump to main content
- **Focus Management:** Clear focus indicators
- **Escape Handling:** Exit modals and overlays

### Screen Reader Support

- **Aria Labels:** Clear navigation descriptions
- **Live Regions:** Announce page changes
- **Landmark Roles:** Structural navigation aids
- **Alternative Text:** Descriptive link text

## ✅ Success Criteria

- [ ] All pages connect logically and intuitively
- [ ] Transitions are smooth and performant
- [ ] Navigation is accessible via keyboard and screen readers
- [ ] Mobile flow patterns work seamlessly
- [ ] Error states provide clear recovery paths
- [ ] Performance remains optimal during transitions

## 🔄 Testing Checklist

**Manual Testing:**
- [ ] Navigate through all major user flows
- [ ] Test on various devices and screen sizes
- [ ] Verify accessibility with keyboard navigation
- [ ] Check animation performance

**Automated Testing:**
- [ ] Route transition tests
- [ ] Navigation component tests
- [ ] Flow integration tests
- [ ] Performance benchmarks

---

**Output Format:** Implementable {{ tool_profile.format }} with clear navigation logic
**Focus:** Seamless user experience with intuitive flow patterns and smooth transitions
