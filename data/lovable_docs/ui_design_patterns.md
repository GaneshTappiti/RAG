# Lovable.dev UI Design Best Practices

## Modern UI Patterns

### Component-Based Architecture

Use reusable components with consistent styling:

- Header/Navigation components
- Card layouts for content display
- Button variants (primary, secondary, outline)
- Form components with validation states
- Modal and dialog patterns

### Responsive Design Principles

#### Mobile-First Approach

Start with mobile layouts and enhance for larger screens:

```css
/* Mobile base styles */
.container {
  padding: 1rem;
  width: 100%;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

#### Tailwind CSS Breakpoints

- `sm:` - 640px and up (tablet portrait)
- `md:` - 768px and up (tablet landscape)
- `lg:` - 1024px and up (laptop)
- `xl:` - 1280px and up (desktop)
- `2xl:` - 1536px and up (large desktop)

### Layout Patterns

#### Dashboard Layout

```jsx
<div className="min-h-screen bg-gray-50">
  <nav className="bg-white shadow-sm border-b">
    {/* Navigation content */}
  </nav>
  
  <div className="flex">
    <aside className="w-64 bg-white shadow-sm hidden lg:block">
      {/* Sidebar content */}
    </aside>
    
    <main className="flex-1 p-6">
      {/* Main content */}
    </main>
  </div>
</div>
```

#### Card Grid Layout

```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map(item => (
    <div key={item.id} className="bg-white rounded-lg shadow-md p-6">
      {/* Card content */}
    </div>
  ))}
</div>
```

## Color and Typography

### Color Schemes

#### Primary Brand Colors

- Use a consistent primary color throughout the app
- Include hover and active states
- Ensure proper contrast ratios (4.5:1 minimum)

#### Semantic Colors

- Success: Green variations
- Warning: Yellow/Orange variations
- Error: Red variations
- Info: Blue variations

### Typography Scale

```css
/* Heading scale */
h1: text-4xl font-bold
h2: text-3xl font-semibold
h3: text-2xl font-semibold
h4: text-xl font-medium
h5: text-lg font-medium
h6: text-base font-medium

/* Body text */
body: text-base leading-relaxed
small: text-sm
caption: text-xs
```

## Interactive Elements

### Button States

```jsx
// Primary button with all states
<button className="
  px-4 py-2 bg-blue-600 text-white rounded-lg
  hover:bg-blue-700 active:bg-blue-800
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  disabled:bg-gray-300 disabled:cursor-not-allowed
  transition-colors duration-200
">
  Click me
</button>
```

### Form Elements

```jsx
// Input with validation states
<div className="space-y-2">
  <label className="block text-sm font-medium text-gray-700">
    Email Address
  </label>
  <input 
    type="email"
    className="
      w-full px-3 py-2 border rounded-lg
      focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
      invalid:border-red-500 invalid:ring-red-500
    "
  />
  <p className="text-sm text-red-600 hidden invalid:block">
    Please enter a valid email address
  </p>
</div>
```

## Loading and Error States

### Loading Spinners

```jsx
// Simple loading spinner
<div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>

// Loading skeleton
<div className="animate-pulse">
  <div className="h-4 bg-gray-300 rounded w-3/4 mb-2"></div>
  <div className="h-4 bg-gray-300 rounded w-1/2"></div>
</div>
```

### Error Boundaries

```jsx
// Error message component
<div className="bg-red-50 border border-red-200 rounded-lg p-4">
  <div className="flex">
    <div className="text-red-600">
      <ExclamationTriangleIcon className="h-5 w-5" />
    </div>
    <div className="ml-3">
      <h3 className="text-sm font-medium text-red-800">
        Something went wrong
      </h3>
      <p className="text-sm text-red-700 mt-1">
        {error.message}
      </p>
    </div>
  </div>
</div>
```

## Accessibility Guidelines

### Keyboard Navigation

- Ensure all interactive elements are keyboard accessible
- Provide clear focus indicators
- Support tab navigation in logical order
- Include skip links for main content

### Screen Reader Support

- Use semantic HTML elements
- Provide alt text for images
- Use proper heading hierarchy
- Include ARIA labels where needed

### Color Accessibility

- Don't rely solely on color to convey information
- Maintain proper contrast ratios
- Test with color blindness simulators
- Provide alternative indicators (icons, text)

## Performance Considerations

### Image Optimization

```jsx
// Next.js Image component with optimization
<Image
  src="/hero-image.jpg"
  alt="Hero section background"
  width={1200}
  height={600}
  priority
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

### Lazy Loading

- Use intersection observer for content below the fold
- Implement progressive loading for long lists
- Defer non-critical JavaScript
- Optimize bundle size with code splitting

### Animation Performance

```css
/* Prefer transform and opacity for animations */
.smooth-animation {
  transition: transform 0.3s ease, opacity 0.3s ease;
  will-change: transform, opacity;
}

/* Avoid animating layout properties */
.avoid {
  transition: width 0.3s ease; /* This causes layout thrashing */
}
```
