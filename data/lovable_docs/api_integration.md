# API Integration Best Practices for Lovable.dev

## Overview

Modern web applications rely heavily on API integrations. This guide covers best practices for implementing robust, scalable API integrations in Lovable.dev projects.

## Authentication Patterns

### JWT Token Management

```javascript
// Token storage and management
class AuthService {
  static setToken(token) {
    localStorage.setItem('authToken', token);
  }
  
  static getToken() {
    return localStorage.getItem('authToken');
  }
  
  static removeToken() {
    localStorage.removeItem('authToken');
  }
  
  static isTokenValid(token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  }
}
```

### OAuth 2.0 Implementation

```javascript
// NextAuth.js configuration
import NextAuth from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'

export default NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
  ],
  callbacks: {
    async jwt({ token, account }) {
      if (account) {
        token.accessToken = account.access_token
      }
      return token
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken
      return session
    },
  },
})
```

## HTTP Client Configuration

### Axios Setup with Interceptors

```javascript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
apiClient.interceptors.request.use(
  (config) => {
    const token = AuthService.getToken();
    if (token && AuthService.isTokenValid(token)) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      AuthService.removeToken();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### Fetch API with Custom Hook

```javascript
// Custom hook for API calls
import { useState, useEffect } from 'react';

export function useApi(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(url, {
          headers: {
            'Authorization': `Bearer ${AuthService.getToken()}`,
            'Content-Type': 'application/json',
            ...options.headers,
          },
          ...options,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        setData(result);
        setError(null);
      } catch (err) {
        setError(err.message);
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}
```

## Error Handling Strategies

### Centralized Error Management

```javascript
// Error handling utility
export class ApiError extends Error {
  constructor(message, status, response) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.response = response;
  }
}

export const handleApiError = (error) => {
  if (error instanceof ApiError) {
    switch (error.status) {
      case 400:
        return 'Invalid request. Please check your input.';
      case 401:
        return 'Authentication required. Please log in.';
      case 403:
        return 'Access denied. You don\'t have permission.';
      case 404:
        return 'Resource not found.';
      case 429:
        return 'Too many requests. Please try again later.';
      case 500:
        return 'Server error. Please try again later.';
      default:
        return 'An unexpected error occurred.';
    }
  }
  return 'Network error. Please check your connection.';
};
```

### Retry Logic

```javascript
// Retry wrapper for API calls
export const withRetry = async (fn, maxRetries = 3, delay = 1000) => {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      
      // Don't retry on client errors (4xx)
      if (error.status >= 400 && error.status < 500) throw error;
      
      await new Promise(resolve => setTimeout(resolve, delay * attempt));
    }
  }
};
```

## Data Fetching Patterns

### React Query Implementation

```javascript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Data fetching hook
export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => apiClient.get('/users').then(res => res.data),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
}

// Mutation hook
export function useCreateUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (userData) => apiClient.post('/users', userData),
    onSuccess: () => {
      // Invalidate and refetch users
      queryClient.invalidateQueries(['users']);
    },
    onError: (error) => {
      console.error('Failed to create user:', error);
    },
  });
}
```

### SWR Implementation

```javascript
import useSWR, { mutate } from 'swr';

const fetcher = (url) => apiClient.get(url).then(res => res.data);

export function useUsers() {
  const { data, error, isLoading } = useSWR('/users', fetcher, {
    refreshInterval: 30000, // Refresh every 30 seconds
    revalidateOnFocus: false,
  });

  return {
    users: data,
    isLoading,
    isError: error,
  };
}

// Optimistic updates
export function updateUserOptimistically(userId, updates) {
  // Update cache immediately
  mutate('/users', (users) => 
    users.map(user => 
      user.id === userId ? { ...user, ...updates } : user
    ), false
  );

  // Send request
  return apiClient.patch(`/users/${userId}`, updates)
    .then(() => mutate('/users')) // Revalidate on success
    .catch(() => mutate('/users')); // Revert on error
}
```

## Real-time Features

### WebSocket Integration

```javascript
// WebSocket hook
import { useEffect, useRef, useState } from 'react';

export function useWebSocket(url) {
  const [lastMessage, setLastMessage] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('Connecting');
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket(url);
    
    ws.current.onopen = () => setConnectionStatus('Connected');
    ws.current.onclose = () => setConnectionStatus('Disconnected');
    ws.current.onmessage = (event) => {
      setLastMessage(JSON.parse(event.data));
    };

    return () => {
      ws.current.close();
    };
  }, [url]);

  const sendMessage = useCallback((message) => {
    if (ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  }, []);

  return { lastMessage, connectionStatus, sendMessage };
}
```

### Server-Sent Events

```javascript
// SSE hook for real-time updates
export function useServerSentEvents(url) {
  const [data, setData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const eventSource = new EventSource(url);

    eventSource.onopen = () => setIsConnected(true);
    eventSource.onmessage = (event) => {
      setData(JSON.parse(event.data));
    };
    eventSource.onerror = () => setIsConnected(false);

    return () => {
      eventSource.close();
      setIsConnected(false);
    };
  }, [url]);

  return { data, isConnected };
}
```

## Performance Optimization

### Request Deduplication

```javascript
// Request cache to prevent duplicate requests
const requestCache = new Map();

export const cachedApiCall = async (url, options = {}) => {
  const cacheKey = `${url}:${JSON.stringify(options)}`;
  
  if (requestCache.has(cacheKey)) {
    return requestCache.get(cacheKey);
  }

  const promise = apiClient(url, options);
  requestCache.set(cacheKey, promise);

  try {
    const result = await promise;
    // Remove from cache after successful completion
    setTimeout(() => requestCache.delete(cacheKey), 1000);
    return result;
  } catch (error) {
    // Remove from cache on error
    requestCache.delete(cacheKey);
    throw error;
  }
};
```

### Pagination Implementation

```javascript
// Infinite scroll pagination hook
export function useInfiniteUsers() {
  const [users, setUsers] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);

  const loadMore = useCallback(async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    try {
      const response = await apiClient.get(`/users?page=${page}&limit=20`);
      const newUsers = response.data.users;
      
      setUsers(prev => [...prev, ...newUsers]);
      setHasMore(newUsers.length === 20);
      setPage(prev => prev + 1);
    } catch (error) {
      console.error('Failed to load more users:', error);
    } finally {
      setLoading(false);
    }
  }, [page, loading, hasMore]);

  return { users, loadMore, hasMore, loading };
}
```

## Security Best Practices

### Input Validation

```javascript
// Input sanitization
import DOMPurify from 'dompurify';

export const sanitizeInput = (input) => {
  return DOMPurify.sanitize(input, { 
    ALLOWED_TAGS: [],
    ALLOWED_ATTRIBUTES: [],
  });
};

// Schema validation with Zod
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().min(18).max(120),
});

export const validateUserData = (data) => {
  return userSchema.safeParse(data);
};
```

### CSRF Protection

```javascript
// CSRF token handling
export const getCSRFToken = async () => {
  const response = await fetch('/api/csrf-token');
  const { token } = await response.json();
  return token;
};

// Include CSRF token in requests
apiClient.interceptors.request.use(async (config) => {
  if (['post', 'put', 'patch', 'delete'].includes(config.method)) {
    const csrfToken = await getCSRFToken();
    config.headers['X-CSRF-Token'] = csrfToken;
  }
  return config;
});
```
