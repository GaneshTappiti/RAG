# Debugging Patterns for Lovable.dev

## Common React Issues and Solutions

### Component Rendering Problems

#### Issue: Components Not Re-rendering

**Symptoms:**
- UI doesn't update when state changes
- Props changes don't trigger re-renders
- Components seem "frozen"

**Common Causes & Solutions:**

```javascript
// ❌ Mutating state directly
const [items, setItems] = useState([]);
const addItem = (newItem) => {
  items.push(newItem); // This won't trigger re-render
  setItems(items);
};

// ✅ Creating new array/object
const addItem = (newItem) => {
  setItems(prev => [...prev, newItem]);
};

// ❌ Modifying nested objects
const [user, setUser] = useState({ profile: { name: '' } });
const updateName = (name) => {
  user.profile.name = name; // Won't trigger re-render
  setUser(user);
};

// ✅ Proper immutable update
const updateName = (name) => {
  setUser(prev => ({
    ...prev,
    profile: { ...prev.profile, name }
  }));
};
```

#### Issue: Infinite Re-render Loops

**Symptoms:**
- Browser becomes unresponsive
- "Maximum update depth exceeded" error
- Console shows continuous render cycles

**Common Causes & Solutions:**

```javascript
// ❌ Creating new objects in render
function MyComponent() {
  const [count, setCount] = useState(0);
  
  // This creates a new object every render
  const config = { max: 100 };
  
  useEffect(() => {
    // This will run on every render
    console.log('Config changed');
  }, [config]);
  
  return <div>{count}</div>;
}

// ✅ Stable references
function MyComponent() {
  const [count, setCount] = useState(0);
  
  // Move outside component or use useMemo
  const config = useMemo(() => ({ max: 100 }), []);
  
  useEffect(() => {
    console.log('Config changed');
  }, [config]);
  
  return <div>{count}</div>;
}
```

### Hook Dependencies Issues

#### Missing Dependencies

```javascript
// ❌ Missing dependency
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, []); // Missing userId dependency
  
  return <div>{user?.name}</div>;
}

// ✅ Complete dependencies
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]); // Include all dependencies
  
  return <div>{user?.name}</div>;
}
```

#### Stale Closures

```javascript
// ❌ Stale closure in setTimeout
function Timer() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setCount(count + 1); // Uses stale count value
    }, 1000);
    
    return () => clearTimeout(timer);
  }, []); // Empty dependency array causes stale closure
  
  return <div>{count}</div>;
}

// ✅ Using functional update
function Timer() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setCount(prev => prev + 1); // Always uses current value
    }, 1000);
    
    return () => clearTimeout(timer);
  }, []); // Safe to use empty array now
  
  return <div>{count}</div>;
}
```

## Performance Debugging

### Identifying Unnecessary Re-renders

```javascript
// Debug component with React DevTools Profiler
function ExpensiveComponent({ data, onUpdate }) {
  console.log('ExpensiveComponent rendered');
  
  // Use React.memo to prevent unnecessary re-renders
  return React.memo(function ExpensiveComponent({ data, onUpdate }) {
    const processedData = useMemo(() => {
      return data.map(item => ({
        ...item,
        computed: expensiveCalculation(item)
      }));
    }, [data]);
    
    return (
      <div>
        {processedData.map(item => (
          <div key={item.id}>{item.computed}</div>
        ))}
      </div>
    );
  });
}

// Custom hook to track re-renders
function useWhyDidYouUpdate(name, props) {
  const previous = useRef();
  
  useEffect(() => {
    if (previous.current) {
      const allKeys = Object.keys({...previous.current, ...props});
      const changedProps = {};
      
      allKeys.forEach(key => {
        if (previous.current[key] !== props[key]) {
          changedProps[key] = {
            from: previous.current[key],
            to: props[key]
          };
        }
      });
      
      if (Object.keys(changedProps).length) {
        console.log('[why-did-you-update]', name, changedProps);
      }
    }
    
    previous.current = props;
  });
}
```

### Memory Leaks

```javascript
// ❌ Memory leak with event listeners
function Component() {
  useEffect(() => {
    const handleResize = () => console.log('resized');
    window.addEventListener('resize', handleResize);
    // Missing cleanup - memory leak!
  }, []);
  
  return <div>Component</div>;
}

// ✅ Proper cleanup
function Component() {
  useEffect(() => {
    const handleResize = () => console.log('resized');
    window.addEventListener('resize', handleResize);
    
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);
  
  return <div>Component</div>;
}

// ❌ Memory leak with subscriptions
function Component() {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    const subscription = dataService.subscribe(setData);
    // Missing unsubscribe - memory leak!
  }, []);
  
  return <div>{data.length} items</div>;
}

// ✅ Proper cleanup
function Component() {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    const subscription = dataService.subscribe(setData);
    
    return () => {
      subscription.unsubscribe();
    };
  }, []);
  
  return <div>{data.length} items</div>;
}
```

## State Management Issues

### Context Provider Problems

```javascript
// ❌ Provider causing unnecessary re-renders
function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  
  // This creates a new object every render
  const value = {
    user,
    setUser,
    theme,
    setTheme
  };
  
  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

// ✅ Stable context value
function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  
  // Memoize the context value
  const value = useMemo(() => ({
    user,
    setUser,
    theme,
    setTheme
  }), [user, theme]);
  
  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}
```

### State Update Timing

```javascript
// ❌ Incorrect state update timing
function Component() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    setCount(count + 1);
    setCount(count + 1); // Still uses old count value
    console.log(count); // Logs old value, state updates are batched
  };
  
  return <button onClick={handleClick}>{count}</button>;
}

// ✅ Proper state updates
function Component() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    setCount(prev => prev + 1);
    setCount(prev => prev + 1); // Uses updated value
    
    // Use useEffect to access updated state
    setTimeout(() => {
      console.log('Updated count will be available in next render');
    }, 0);
  };
  
  return <button onClick={handleClick}>{count}</button>;
}
```

## API and Async Issues

### Race Conditions

```javascript
// ❌ Race condition in useEffect
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    setLoading(true);
    fetchUser(userId).then(user => {
      setUser(user); // Wrong user if userId changed quickly
      setLoading(false);
    });
  }, [userId]);
  
  return loading ? <div>Loading...</div> : <div>{user?.name}</div>;
}

// ✅ Handling race conditions
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    let cancelled = false;
    
    setLoading(true);
    fetchUser(userId).then(user => {
      if (!cancelled) {
        setUser(user);
        setLoading(false);
      }
    });
    
    return () => {
      cancelled = true;
    };
  }, [userId]);
  
  return loading ? <div>Loading...</div> : <div>{user?.name}</div>;
}
```

### Error Boundaries

```javascript
// Error boundary component
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Log to error reporting service
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try again
          </button>
        </div>
      );
    }
    
    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Router>
    </ErrorBoundary>
  );
}
```

## Debugging Tools and Techniques

### React DevTools

```javascript
// Add component names for better debugging
const MyComponent = React.memo(function MyComponent(props) {
  // Component logic
});

// Use display names
MyComponent.displayName = 'MyComponent';

// Debugging hooks
function useDebugValue(value, format) {
  React.useDebugValue(value, format);
}

function useCustomHook(id) {
  const [data, setData] = useState(null);
  
  // This will show in React DevTools
  useDebugValue(data ? `Data loaded for ${id}` : 'Loading...');
  
  return data;
}
```

### Console Debugging

```javascript
// Conditional logging
const DEBUG = process.env.NODE_ENV === 'development';

function debugLog(message, data) {
  if (DEBUG) {
    console.group(message);
    console.log(data);
    console.trace();
    console.groupEnd();
  }
}

// Performance monitoring
function usePerformanceMonitor(componentName) {
  useEffect(() => {
    const start = performance.now();
    
    return () => {
      const end = performance.now();
      debugLog(`${componentName} render time`, `${end - start}ms`);
    };
  });
}
```

### Network Debugging

```javascript
// Request/response logging
const apiClient = axios.create();

if (process.env.NODE_ENV === 'development') {
  apiClient.interceptors.request.use(request => {
    console.log('🚀 Request:', request);
    return request;
  });
  
  apiClient.interceptors.response.use(
    response => {
      console.log('✅ Response:', response);
      return response;
    },
    error => {
      console.error('❌ Error:', error);
      return Promise.reject(error);
    }
  );
}
```

## Testing Strategies

### Component Testing

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Testing async components
test('loads user data', async () => {
  const mockUser = { id: 1, name: 'John Doe' };
  jest.spyOn(api, 'fetchUser').mockResolvedValue(mockUser);
  
  render(<UserProfile userId={1} />);
  
  expect(screen.getByText('Loading...')).toBeInTheDocument();
  
  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
  
  expect(api.fetchUser).toHaveBeenCalledWith(1);
});

// Testing user interactions
test('updates count on button click', async () => {
  const user = userEvent.setup();
  render(<Counter />);
  
  const button = screen.getByRole('button', { name: /increment/i });
  const count = screen.getByText('0');
  
  await user.click(button);
  
  expect(count).toHaveTextContent('1');
});
```
