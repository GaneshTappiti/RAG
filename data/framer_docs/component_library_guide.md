# Framer - Component Library and Code Integration Guide

## Advanced Component Development

### Code Components in Framer

Framer allows integration of real React components, bridging design and development seamlessly.

#### Custom React Components

```typescript
// Example: Custom Button Component
import { ComponentProps } from "framer"

interface ButtonProps extends ComponentProps {
  variant: "primary" | "secondary" | "ghost"
  size: "small" | "medium" | "large"
  icon?: string
  loading?: boolean
  disabled?: boolean
  onClick?: () => void
}

export function CustomButton({
  variant = "primary",
  size = "medium",
  icon,
  loading = false,
  disabled = false,
  onClick,
  children,
  ...props
}: ButtonProps) {
  const baseStyles = {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    border: "none",
    borderRadius: "8px",
    fontWeight: "600",
    cursor: disabled ? "not-allowed" : "pointer",
    transition: "all 0.2s ease",
  }

  const variantStyles = {
    primary: { backgroundColor: "#007AFF", color: "white" },
    secondary: { backgroundColor: "#F2F2F7", color: "#000" },
    ghost: { backgroundColor: "transparent", color: "#007AFF" },
  }

  const sizeStyles = {
    small: { padding: "8px 16px", fontSize: "14px" },
    medium: { padding: "12px 24px", fontSize: "16px" },
    large: { padding: "16px 32px", fontSize: "18px" },
  }

  return (
    <button
      style={{
        ...baseStyles,
        ...variantStyles[variant],
        ...sizeStyles[size],
        opacity: disabled ? 0.5 : 1,
      }}
      onClick={onClick}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <span>Loading...</span>}
      {icon && !loading && <span style={{ marginRight: "8px" }}>{icon}</span>}
      {children}
    </button>
  )
}

// Property Controls for Framer
CustomButton.defaultProps = {
  variant: "primary",
  size: "medium",
  children: "Button",
}

CustomButton.propertyControls = {
  variant: {
    type: "enum",
    options: ["primary", "secondary", "ghost"],
    defaultValue: "primary",
  },
  size: {
    type: "enum",
    options: ["small", "medium", "large"],
    defaultValue: "medium",
  },
  icon: {
    type: "string",
    defaultValue: "",
  },
  loading: {
    type: "boolean",
    defaultValue: false,
  },
  disabled: {
    type: "boolean",
    defaultValue: false,
  },
}
```

#### Data-Connected Components

```typescript
// Example: Dynamic Card Component with API Data
import { useEffect, useState } from "react"
import { ComponentProps } from "framer"

interface ApiCardProps extends ComponentProps {
  apiEndpoint: string
  cardId: string
  showImage: boolean
  imageAspectRatio: number
}

export function ApiCard({
  apiEndpoint,
  cardId,
  showImage = true,
  imageAspectRatio = 1.5,
  ...props
}: ApiCardProps) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (apiEndpoint && cardId) {
      fetchData()
    }
  }, [apiEndpoint, cardId])

  const fetchData = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${apiEndpoint}/${cardId}`)
      const result = await response.json()
      setData(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div style={{ padding: "20px", background: "#f5f5f5", borderRadius: "12px" }}>
        <div style={{ height: "20px", background: "#ddd", borderRadius: "4px", marginBottom: "10px" }} />
        <div style={{ height: "60px", background: "#ddd", borderRadius: "4px" }} />
      </div>
    )
  }

  if (error) {
    return (
      <div style={{ padding: "20px", background: "#fee", borderRadius: "12px", color: "#c00" }}>
        Error loading data: {error}
      </div>
    )
  }

  return (
    <div style={{ background: "white", borderRadius: "12px", overflow: "hidden", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }} {...props}>
      {showImage && data?.image && (
        <img
          src={data.image}
          alt={data.title}
          style={{
            width: "100%",
            height: `${300 / imageAspectRatio}px`,
            objectFit: "cover",
          }}
        />
      )}
      <div style={{ padding: "20px" }}>
        <h3 style={{ margin: "0 0 10px", fontSize: "18px", fontWeight: "600" }}>
          {data?.title || "No Title"}
        </h3>
        <p style={{ margin: "0", color: "#666", lineHeight: "1.5" }}>
          {data?.description || "No description available"}
        </p>
        {data?.tags && (
          <div style={{ marginTop: "15px", display: "flex", gap: "8px", flexWrap: "wrap" }}>
            {data.tags.map((tag, index) => (
              <span
                key={index}
                style={{
                  background: "#e3f2fd",
                  color: "#1976d2",
                  padding: "4px 8px",
                  borderRadius: "4px",
                  fontSize: "12px",
                }}
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

ApiCard.propertyControls = {
  apiEndpoint: {
    type: "string",
    defaultValue: "https://api.example.com/items",
  },
  cardId: {
    type: "string",
    defaultValue: "1",
  },
  showImage: {
    type: "boolean",
    defaultValue: true,
  },
  imageAspectRatio: {
    type: "number",
    min: 0.5,
    max: 3,
    step: 0.1,
    defaultValue: 1.5,
  },
}
```

### Design System Implementation

#### Token-Based Design System

```typescript
// Design Tokens
export const designTokens = {
  colors: {
    primary: {
      50: "#e3f2fd",
      100: "#bbdefb",
      500: "#2196f3",
      900: "#0d47a1",
    },
    neutral: {
      50: "#fafafa",
      100: "#f5f5f5",
      500: "#9e9e9e",
      900: "#212121",
    },
    semantic: {
      success: "#4caf50",
      warning: "#ff9800",
      error: "#f44336",
      info: "#2196f3",
    },
  },
  typography: {
    fontFamily: {
      sans: ["Inter", "system-ui", "sans-serif"],
      mono: ["Fira Code", "monospace"],
    },
    fontSize: {
      xs: "12px",
      sm: "14px",
      base: "16px",
      lg: "18px",
      xl: "20px",
      "2xl": "24px",
      "3xl": "30px",
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
    },
  },
  spacing: {
    0: "0px",
    1: "4px",
    2: "8px",
    3: "12px",
    4: "16px",
    5: "20px",
    6: "24px",
    8: "32px",
    10: "40px",
    12: "48px",
    16: "64px",
    20: "80px",
    24: "96px",
  },
  borderRadius: {
    none: "0px",
    sm: "4px",
    base: "8px",
    lg: "12px",
    xl: "16px",
    full: "9999px",
  },
  boxShadow: {
    sm: "0 1px 2px rgba(0, 0, 0, 0.05)",
    base: "0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)",
    lg: "0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05)",
    xl: "0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04)",
  },
}

// Component Factory
export function createComponent(name: string, baseStyles: any, variants: any = {}) {
  const Component = ({ variant = "default", children, style = {}, ...props }) => {
    const appliedStyles = {
      ...baseStyles,
      ...(variants[variant] || {}),
      ...style,
    }

    return (
      <div style={appliedStyles} {...props}>
        {children}
      </div>
    )
  }

  Component.displayName = name
  return Component
}

// Usage Example: Card Component
export const Card = createComponent(
  "Card",
  {
    background: designTokens.colors.neutral[50],
    borderRadius: designTokens.borderRadius.lg,
    boxShadow: designTokens.boxShadow.base,
    padding: designTokens.spacing[6],
  },
  {
    elevated: {
      boxShadow: designTokens.boxShadow.xl,
    },
    outlined: {
      border: `1px solid ${designTokens.colors.neutral[100]}`,
      boxShadow: "none",
    },
  }
)
```

## Animation and Motion Design

### Advanced Animation Patterns

#### Custom Animation Hooks

```typescript
// Custom Animation Hook for Framer
import { useAnimation, useMotionValue, useTransform } from "framer-motion"
import { useEffect } from "react"

export function useSequentialAnimation(items: any[], delay: number = 0.1) {
  const controls = useAnimation()

  const animateIn = async () => {
    await controls.start((i) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: i * delay,
        duration: 0.5,
        ease: "easeOut",
      },
    }))
  }

  const animateOut = async () => {
    await controls.start({
      opacity: 0,
      y: 20,
      transition: { duration: 0.3 },
    })
  }

  return { controls, animateIn, animateOut }
}

// Scroll-based Animation Hook
export function useScrollAnimation(threshold: number = 0.1) {
  const scrollY = useMotionValue(0)
  const opacity = useTransform(scrollY, [0, 300], [1, 0])
  const scale = useTransform(scrollY, [0, 300], [1, 0.8])

  useEffect(() => {
    const updateScrollY = () => scrollY.set(window.scrollY)
    window.addEventListener("scroll", updateScrollY)
    return () => window.removeEventListener("scroll", updateScrollY)
  }, [scrollY])

  return { opacity, scale, scrollY }
}

// Interactive Animation Component
export function AnimatedCard({ children, ...props }) {
  const { controls, animateIn, animateOut } = useSequentialAnimation([])
  const [isHovered, setIsHovered] = useState(false)

  return (
    <motion.div
      animate={controls}
      initial={{ opacity: 0, y: 20 }}
      whileHover={{ scale: 1.05, rotate: 1 }}
      whileTap={{ scale: 0.95 }}
      onHoverStart={() => {
        setIsHovered(true)
        animateIn()
      }}
      onHoverEnd={() => {
        setIsHovered(false)
        animateOut()
      }}
      style={{
        background: "white",
        borderRadius: "12px",
        padding: "20px",
        cursor: "pointer",
      }}
      {...props}
    >
      {children}
    </motion.div>
  )
}
```

#### Complex Animation Sequences

```typescript
// Multi-step Onboarding Animation
export function OnboardingFlow({ steps, currentStep, onNext, onPrev }) {
  const [scope, animate] = useAnimate()

  const animateStep = async (direction: "next" | "prev") => {
    const exitX = direction === "next" ? -300 : 300
    const enterX = direction === "next" ? 300 : -300

    // Animate current step out
    await animate(
      ".current-step",
      { opacity: 0, x: exitX },
      { duration: 0.3, ease: "easeInOut" }
    )

    // Update step content (handled by parent)
    direction === "next" ? onNext() : onPrev()

    // Animate new step in
    await animate(
      ".current-step",
      { opacity: 1, x: 0 },
      { duration: 0.3, ease: "easeInOut" }
    )
  }

  return (
    <div ref={scope} style={{ position: "relative", overflow: "hidden" }}>
      <motion.div
        className="current-step"
        initial={{ opacity: 0, x: 300 }}
        animate={{ opacity: 1, x: 0 }}
        style={{ padding: "40px" }}
      >
        {steps[currentStep]}
      </motion.div>

      <div style={{ display: "flex", justifyContent: "space-between", padding: "20px" }}>
        <button
          onClick={() => animateStep("prev")}
          disabled={currentStep === 0}
          style={{ opacity: currentStep === 0 ? 0.5 : 1 }}
        >
          Previous
        </button>
        <div style={{ display: "flex", gap: "8px" }}>
          {steps.map((_, index) => (
            <div
              key={index}
              style={{
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                background: index === currentStep ? "#007AFF" : "#ddd",
                transition: "background 0.3s ease",
              }}
            />
          ))}
        </div>
        <button
          onClick={() => animateStep("next")}
          disabled={currentStep === steps.length - 1}
          style={{ opacity: currentStep === steps.length - 1 ? 0.5 : 1 }}
        >
          Next
        </button>
      </div>
    </div>
  )
}

// Gesture-based Card Stack
export function CardStack({ cards }) {
  const [currentIndex, setCurrentIndex] = useState(0)

  return (
    <div style={{ position: "relative", height: "400px", width: "300px" }}>
      {cards.map((card, index) => (
        <motion.div
          key={index}
          drag="x"
          dragConstraints={{ left: -200, right: 200 }}
          onDragEnd={(event, info) => {
            if (info.offset.x > 100) {
              // Swiped right
              setCurrentIndex((prev) => Math.min(prev + 1, cards.length - 1))
            } else if (info.offset.x < -100) {
              // Swiped left
              setCurrentIndex((prev) => Math.max(prev - 1, 0))
            }
          }}
          animate={{
            x: 0,
            scale: index === currentIndex ? 1 : 0.9,
            zIndex: cards.length - Math.abs(index - currentIndex),
            opacity: Math.abs(index - currentIndex) > 2 ? 0 : 1,
          }}
          style={{
            position: "absolute",
            background: "white",
            borderRadius: "16px",
            padding: "20px",
            boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
            cursor: "grab",
          }}
          whileDrag={{ cursor: "grabbing", rotate: 5 }}
        >
          {card}
        </motion.div>
      ))}
    </div>
  )
}
```

## Data Integration and State Management

### Real-time Data Components

#### WebSocket Integration

```typescript
// Real-time Data Hook
export function useWebSocket(url: string) {
  const [socket, setSocket] = useState<WebSocket | null>(null)
  const [data, setData] = useState(null)
  const [connectionStatus, setConnectionStatus] = useState("Disconnected")

  useEffect(() => {
    const ws = new WebSocket(url)
    setSocket(ws)

    ws.onopen = () => {
      setConnectionStatus("Connected")
    }

    ws.onmessage = (event) => {
      const newData = JSON.parse(event.data)
      setData(newData)
    }

    ws.onerror = () => {
      setConnectionStatus("Error")
    }

    ws.onclose = () => {
      setConnectionStatus("Disconnected")
    }

    return () => {
      ws.close()
    }
  }, [url])

  const sendMessage = (message: any) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message))
    }
  }

  return { data, connectionStatus, sendMessage }
}

// Real-time Dashboard Component
export function LiveDashboard({ websocketUrl }) {
  const { data, connectionStatus, sendMessage } = useWebSocket(websocketUrl)
  const [metrics, setMetrics] = useState([])

  useEffect(() => {
    if (data && data.type === "metrics") {
      setMetrics((prev) => [...prev.slice(-20), data.payload])
    }
  }, [data])

  return (
    <div style={{ padding: "20px" }}>
      <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "20px" }}>
        <div
          style={{
            width: "10px",
            height: "10px",
            borderRadius: "50%",
            background: connectionStatus === "Connected" ? "#4caf50" : "#f44336",
          }}
        />
        <span>Status: {connectionStatus}</span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "20px" }}>
        {metrics.map((metric, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            style={{
              background: "white",
              padding: "20px",
              borderRadius: "12px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            }}
          >
            <h3 style={{ margin: "0 0 10px", fontSize: "14px", color: "#666" }}>
              {metric.label}
            </h3>
            <div style={{ fontSize: "24px", fontWeight: "bold", color: "#333" }}>
              {metric.value}
            </div>
            <div style={{ fontSize: "12px", color: metric.change > 0 ? "#4caf50" : "#f44336" }}>
              {metric.change > 0 ? "↑" : "↓"} {Math.abs(metric.change)}%
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
```

### Form Handling and Validation

#### Advanced Form Components

```typescript
// Form Context and Validation
export const FormContext = createContext()

export function useForm(initialValues: any, validationSchema: any) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  const [touched, setTouched] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const validateField = (name: string, value: any) => {
    const fieldSchema = validationSchema[name]
    if (!fieldSchema) return null

    for (const rule of fieldSchema) {
      if (rule.required && (!value || value.trim() === "")) {
        return rule.message || `${name} is required`
      }
      if (rule.minLength && value.length < rule.minLength) {
        return rule.message || `${name} must be at least ${rule.minLength} characters`
      }
      if (rule.pattern && !rule.pattern.test(value)) {
        return rule.message || `${name} format is invalid`
      }
    }
    return null
  }

  const setValue = (name: string, value: any) => {
    setValues((prev) => ({ ...prev, [name]: value }))
    const error = validateField(name, value)
    setErrors((prev) => ({ ...prev, [name]: error }))
  }

  const setTouched = (name: string) => {
    setTouched((prev) => ({ ...prev, [name]: true }))
  }

  const handleSubmit = async (onSubmit: (values: any) => Promise<void>) => {
    setIsSubmitting(true)
    try {
      // Validate all fields
      const newErrors = {}
      Object.keys(values).forEach((key) => {
        const error = validateField(key, values[key])
        if (error) newErrors[key] = error
      })

      if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors)
        return
      }

      await onSubmit(values)
    } catch (error) {
      console.error("Form submission error:", error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return {
    values,
    errors,
    touched,
    isSubmitting,
    setValue,
    setTouched,
    handleSubmit,
  }
}

// Smart Input Component
export function SmartInput({
  name,
  type = "text",
  placeholder,
  icon,
  ...props
}) {
  const { values, errors, touched, setValue, setTouched } = useContext(FormContext)
  const [isFocused, setIsFocused] = useState(false)

  const hasError = touched[name] && errors[name]
  const value = values[name] || ""

  return (
    <div style={{ marginBottom: "20px" }}>
      <div
        style={{
          position: "relative",
          border: `2px solid ${hasError ? "#f44336" : isFocused ? "#2196f3" : "#e0e0e0"}`,
          borderRadius: "8px",
          transition: "all 0.2s ease",
        }}
      >
        {icon && (
          <div
            style={{
              position: "absolute",
              left: "12px",
              top: "50%",
              transform: "translateY(-50%)",
              color: hasError ? "#f44336" : isFocused ? "#2196f3" : "#666",
            }}
          >
            {icon}
          </div>
        )}
        <input
          type={type}
          value={value}
          onChange={(e) => setValue(name, e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => {
            setIsFocused(false)
            setTouched(name)
          }}
          placeholder={placeholder}
          style={{
            width: "100%",
            padding: icon ? "12px 12px 12px 40px" : "12px",
            border: "none",
            outline: "none",
            fontSize: "16px",
            background: "transparent",
          }}
          {...props}
        />
      </div>
      {hasError && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          style={{
            color: "#f44336",
            fontSize: "14px",
            marginTop: "4px",
          }}
        >
          {errors[name]}
        </motion.div>
      )}
    </div>
  )
}
```

## Performance Optimization

### Code Optimization Strategies

#### Component Performance

```typescript
// Memoization and Performance Optimization
import { memo, useMemo, useCallback } from "react"

// Optimized List Component
export const OptimizedList = memo(({ items, onItemClick }) => {
  const memoizedItems = useMemo(() => {
    return items.map((item) => ({
      ...item,
      id: item.id,
    }))
  }, [items])

  const handleItemClick = useCallback(
    (itemId) => {
      onItemClick(itemId)
    },
    [onItemClick]
  )

  return (
    <div>
      {memoizedItems.map((item) => (
        <ListItem
          key={item.id}
          item={item}
          onClick={() => handleItemClick(item.id)}
        />
      ))}
    </div>
  )
})

// Virtualized List for Large Datasets
export function VirtualizedList({ items, itemHeight = 50, containerHeight = 400 }) {
  const [scrollTop, setScrollTop] = useState(0)

  const visibleItems = useMemo(() => {
    const startIndex = Math.floor(scrollTop / itemHeight)
    const endIndex = Math.min(
      startIndex + Math.ceil(containerHeight / itemHeight) + 1,
      items.length
    )

    return items.slice(startIndex, endIndex).map((item, index) => ({
      ...item,
      index: startIndex + index,
    }))
  }, [items, scrollTop, itemHeight, containerHeight])

  return (
    <div
      style={{ height: containerHeight, overflow: "auto" }}
      onScroll={(e) => setScrollTop(e.target.scrollTop)}
    >
      <div style={{ height: items.length * itemHeight, position: "relative" }}>
        {visibleItems.map((item) => (
          <div
            key={item.id}
            style={{
              position: "absolute",
              top: item.index * itemHeight,
              left: 0,
              right: 0,
              height: itemHeight,
              display: "flex",
              alignItems: "center",
              padding: "0 16px",
              borderBottom: "1px solid #eee",
            }}
          >
            {item.content}
          </div>
        ))}
      </div>
    </div>
  )
}

// Image Optimization Component
export function OptimizedImage({
  src,
  alt,
  width,
  height,
  placeholder = "#f0f0f0",
  ...props
}) {
  const [isLoaded, setIsLoaded] = useState(false)
  const [isInView, setIsInView] = useState(false)
  const imgRef = useRef()

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true)
          observer.disconnect()
        }
      },
      { threshold: 0.1 }
    )

    if (imgRef.current) {
      observer.observe(imgRef.current)
    }

    return () => observer.disconnect()
  }, [])

  return (
    <div
      ref={imgRef}
      style={{
        width,
        height,
        background: placeholder,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        overflow: "hidden",
      }}
      {...props}
    >
      {isInView && (
        <img
          src={src}
          alt={alt}
          onLoad={() => setIsLoaded(true)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            opacity: isLoaded ? 1 : 0,
            transition: "opacity 0.3s ease",
          }}
        />
      )}
      {!isLoaded && isInView && (
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            color: "#999",
          }}
        >
          Loading...
        </div>
      )}
    </div>
  )
}
```

## Testing and Quality Assurance

### Component Testing Strategies

```typescript
// Testing Utilities for Framer Components
import { render, screen, fireEvent, waitFor } from "@testing-library/react"
import { ComponentWrapper } from "framer"

// Test Helper Functions
export function renderFramerComponent(Component, props = {}) {
  return render(
    <ComponentWrapper>
      <Component {...props} />
    </ComponentWrapper>
  )
}

// Example Test Suite
describe("CustomButton Component", () => {
  test("renders with correct text", () => {
    renderFramerComponent(CustomButton, { children: "Click me" })
    expect(screen.getByText("Click me")).toBeInTheDocument()
  })

  test("calls onClick when clicked", () => {
    const handleClick = jest.fn()
    renderFramerComponent(CustomButton, {
      children: "Click me",
      onClick: handleClick,
    })

    fireEvent.click(screen.getByText("Click me"))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  test("shows loading state", () => {
    renderFramerComponent(CustomButton, {
      children: "Submit",
      loading: true,
    })

    expect(screen.getByText("Loading...")).toBeInTheDocument()
    expect(screen.getByRole("button")).toBeDisabled()
  })

  test("applies correct variant styles", () => {
    const { rerender } = renderFramerComponent(CustomButton, {
      variant: "primary",
      children: "Primary",
    })

    const button = screen.getByRole("button")
    expect(button).toHaveStyle({ backgroundColor: "#007AFF" })

    rerender(
      <ComponentWrapper>
        <CustomButton variant="secondary">Secondary</CustomButton>
      </ComponentWrapper>
    )

    expect(button).toHaveStyle({ backgroundColor: "#F2F2F7" })
  })
})

// Integration Test Example
describe("Form Integration", () => {
  test("validates and submits form", async () => {
    const handleSubmit = jest.fn()
    const validationSchema = {
      email: [
        { required: true, message: "Email is required" },
        { pattern: /\S+@\S+\.\S+/, message: "Invalid email format" },
      ],
    }

    renderFramerComponent(ContactForm, {
      onSubmit: handleSubmit,
      validationSchema,
    })

    // Test validation
    const emailInput = screen.getByPlaceholderText("Enter your email")
    fireEvent.blur(emailInput)

    await waitFor(() => {
      expect(screen.getByText("Email is required")).toBeInTheDocument()
    })

    // Test valid submission
    fireEvent.change(emailInput, { target: { value: "test@example.com" } })
    fireEvent.click(screen.getByText("Submit"))

    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        email: "test@example.com",
      })
    })
  })
})
```

This comprehensive guide covers advanced Framer development patterns, component architecture, animation techniques, data integration, and testing strategies. It provides the foundation for creating sophisticated interactive prototypes and design systems that bridge design and development workflows.
