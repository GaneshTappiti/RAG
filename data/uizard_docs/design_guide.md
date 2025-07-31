# Uizard - Design and Wireframing Guide

## Tool Overview

Uizard is an AI-powered design tool that specializes in creating wireframes, mockups, and design systems quickly. It excels at translating ideas into visual designs and prototypes with minimal manual design work.

## Core Capabilities

### Design Creation
- **Wireframe Generation**: Low-fidelity layouts and structure
- **Mockup Creation**: High-fidelity visual designs
- **Design System**: Consistent components and styling
- **Prototype**: Interactive designs with clickable elements
- **Responsive Design**: Multi-device layout adaptation

### AI-Powered Features
- **Text-to-Design**: Generate designs from text descriptions
- **Screenshot-to-Design**: Convert existing apps/websites to designs
- **Hand-drawn Sketch**: Transform sketches into digital designs
- **Auto-layout**: Intelligent component arrangement
- **Theme Generation**: Consistent color and typography systems

### Design Elements
- **UI Components**: Buttons, forms, cards, navigation
- **Layout Systems**: Grids, flexbox, responsive containers
- **Typography**: Font pairing and hierarchy
- **Color Palettes**: Brand-consistent color schemes
- **Icons and Images**: Design assets and placeholders

## Prompting Best Practices

### Structure Your Design Requests

1. **Platform First**: Specify mobile, tablet, or desktop
2. **Layout Type**: Define the overall structure (dashboard, landing, form)
3. **Content Requirements**: List sections and information hierarchy
4. **Style Preferences**: Mention design aesthetic and brand guidelines
5. **User Flow**: Describe navigation and interactions

### Effective Prompt Patterns

#### Wireframe Creation
```
Create a wireframe for a [platform] [app type] with:

Layout structure:
- [Header/navigation elements]
- [Main content areas]
- [Sidebar/secondary content]
- [Footer elements]

Key sections:
- [Section 1]: [Purpose and content]
- [Section 2]: [Purpose and content]
- [Section 3]: [Purpose and content]

Design style:
- [Modern/minimal/corporate/playful]
- [Color preferences if any]
- [Typography approach]

Target users: [User demographic and use case]
```

#### Mobile App Design
```
Design a mobile app interface for [app purpose]:

Screen requirements:
- [Screen 1]: [Layout and components]
- [Screen 2]: [Layout and components]
- [Screen 3]: [Layout and components]

UI components needed:
- Navigation: [Tab bar/drawer/stack]
- Forms: [Input types and validation]
- Lists: [Card layouts and data display]
- Actions: [Button styles and CTAs]

Design guidelines:
- Platform: [iOS/Android/Cross-platform]
- Style: [Material Design/iOS HIG/Custom]
- Accessibility: [Requirements and considerations]
```

### Design System Creation

#### Component Library
```
Create a design system for [project type] including:

Core components:
- Buttons: [Primary, secondary, ghost, icon variants]
- Forms: [Input fields, dropdowns, checkboxes, radio buttons]
- Cards: [Content cards, product cards, info cards]
- Navigation: [Header, sidebar, breadcrumbs, pagination]

Visual elements:
- Color palette: [Primary, secondary, accent, neutral colors]
- Typography: [Heading hierarchy, body text, captions]
- Spacing: [Margin and padding system]
- Borders: [Radius, shadows, dividers]

Brand requirements:
- Logo placement and sizing
- Brand colors and usage
- Photography style
- Icon style and weight
```

## Platform-Specific Guidelines

### Mobile Design Principles

#### iOS Design Guidelines
- Follow Apple's Human Interface Guidelines
- Use system fonts (SF Pro) and native components
- Implement proper touch targets (44pt minimum)
- Consider safe areas and device-specific layouts
- Use appropriate navigation patterns (tab bar, navigation stack)

#### Android Design Guidelines
- Follow Material Design principles
- Use Roboto font family and material components
- Implement proper elevation and shadows
- Consider Android-specific navigation (bottom navigation, FAB)
- Use appropriate color theming and dark mode support

#### Cross-Platform Considerations
- Maintain platform consistency while keeping brand identity
- Use appropriate navigation patterns for each platform
- Consider different screen sizes and orientations
- Test designs on various device types and resolutions

### Web Design Principles

#### Responsive Design
- Mobile-first approach with progressive enhancement
- Flexible grid systems and breakpoints
- Scalable typography and spacing
- Optimized images and media queries
- Touch-friendly interfaces for mobile devices

#### Desktop Interface Design
- Efficient use of screen real estate
- Hover states and cursor interactions
- Keyboard navigation support
- Multi-column layouts and sidebars
- Dense information presentation when appropriate

## Common Design Patterns

### Landing Page Design
```
Create a landing page design with:

Hero section:
- Compelling headline and subheading
- Primary call-to-action button
- Hero image or video background
- Trust indicators (logos, testimonials)

Content sections:
- Features/benefits with icons
- Social proof (testimonials, reviews)
- Pricing or product information
- FAQ or additional details

Footer:
- Navigation links
- Contact information
- Social media links
- Legal pages and policies

Design approach:
- Clear visual hierarchy
- Scannable content layout
- Strong contrast and readability
- Mobile-responsive design
```

### Dashboard Interface
```
Design a dashboard interface featuring:

Top navigation:
- Logo/brand identifier
- Main navigation menu
- User profile and settings
- Search functionality
- Notifications

Main content area:
- Key metrics and KPIs in card format
- Data visualization (charts, graphs)
- Recent activity or updates
- Quick action buttons
- Filtering and sorting options

Sidebar (optional):
- Secondary navigation
- Contextual information
- Recently accessed items
- Quick links or shortcuts

Layout considerations:
- Grid-based component arrangement
- Consistent spacing and alignment
- Loading states for data
- Empty states for no data
- Responsive behavior for smaller screens
```

### E-commerce Design
```
Design an e-commerce interface with:

Product catalog:
- Grid/list view toggle
- Product cards with images and key info
- Filtering and sorting options
- Search with autocomplete
- Category navigation

Product detail:
- High-quality product images with zoom
- Product information and specifications
- Pricing and availability
- Add to cart and wishlist buttons
- Reviews and ratings
- Related/recommended products

Shopping cart:
- Item list with images and details
- Quantity adjustment controls
- Price calculations and totals
- Promotional code input
- Proceed to checkout button

Checkout process:
- Multi-step or single-page checkout
- Guest and account options
- Payment method selection
- Shipping information forms
- Order summary and confirmation
```

## Color and Typography Guidelines

### Color Psychology in Design
- **Blue**: Trust, professionalism, technology
- **Green**: Growth, health, money, environment
- **Red**: Urgency, passion, energy, danger
- **Orange**: Enthusiasm, creativity, warmth
- **Purple**: Luxury, creativity, mystery
- **Black**: Sophistication, elegance, power
- **White**: Cleanliness, simplicity, peace

### Typography Hierarchy
```
Heading 1 (H1): 32-48px - Page titles, main headings
Heading 2 (H2): 24-32px - Section headings
Heading 3 (H3): 20-24px - Subsection headings
Heading 4 (H4): 18-20px - Component headings
Body Large: 16-18px - Important body text
Body Regular: 14-16px - Standard body text
Caption: 12-14px - Secondary information
Small: 10-12px - Fine print, metadata
```

### Font Pairing Guidelines
- **Sans-serif combinations**: Modern, clean, tech-focused
- **Serif combinations**: Traditional, elegant, trustworthy
- **Mixed pairing**: Sans-serif headings with serif body (or vice versa)
- **Monospace accents**: Code, data, technical content

## Layout and Spacing

### Grid Systems
- **12-column grid**: Standard web layout system
- **8-point grid**: Consistent spacing and sizing
- **4-column mobile**: Simplified mobile layouts
- **Flexible grids**: Responsive design adaptation

### Spacing Principles
```
Base unit: 8px (or 4px for fine adjustments)

Spacing scale:
- 4px: Tight spacing within components
- 8px: Standard component spacing
- 16px: Section spacing within cards
- 24px: Small gaps between sections
- 32px: Medium gaps between sections
- 48px: Large gaps between major sections
- 64px+: Extra large gaps for visual separation
```

### Visual Hierarchy
1. **Size**: Larger elements draw attention first
2. **Color**: High contrast and bright colors stand out
3. **Position**: Top-left gets attention in western layouts
4. **Spacing**: White space creates emphasis
5. **Typography**: Weight and style indicate importance
6. **Imagery**: Photos and illustrations attract attention

## Accessibility in Design

### Color Accessibility
- Maintain 4.5:1 contrast ratio for normal text
- Use 3:1 contrast ratio for large text (18px+ or 14px+ bold)
- Don't rely on color alone to convey information
- Provide alternative indicators (icons, patterns, text)

### Layout Accessibility
- Logical reading order and tab sequence
- Clear focus indicators for interactive elements
- Sufficient touch target sizes (44px minimum on mobile)
- Consistent navigation and layout patterns

### Content Accessibility
- Descriptive alt text for images
- Clear and concise copy
- Proper heading hierarchy
- Meaningful link text
- Error messages and form validation

## Prototyping and Interaction

### Interactive Elements
- **Hover states**: Visual feedback for desktop interactions
- **Active states**: Immediate response to user actions
- **Loading states**: Progress indicators during waits
- **Error states**: Clear communication of problems
- **Empty states**: Guidance when no content exists

### Micro-interactions
- **Button animations**: Subtle feedback on clicks
- **Form interactions**: Real-time validation and help
- **Navigation transitions**: Smooth page/section changes
- **Data loading**: Skeleton screens and progress bars
- **Success feedback**: Confirmations and celebrations

### User Flow Design
1. **Entry point**: How users arrive at the interface
2. **Primary path**: Main task completion flow
3. **Alternative paths**: Secondary actions and edge cases
4. **Exit points**: Task completion and next steps
5. **Error recovery**: Handling mistakes and problems
