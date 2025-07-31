# Lovable.dev - Advanced Prompting Guide

## Tool Overview

Lovable.dev is an AI-powered web development platform that excels at creating modern, responsive web applications using React, Next.js, and TypeScript. It specializes in building full-stack applications with clean, production-ready code.

## Core Capabilities

### Frontend Technologies
- **React 18+**: Component-based architecture with hooks
- **Next.js 14**: App Router, server components, API routes
- **TypeScript**: Full type safety and modern syntax
- **Tailwind CSS**: Utility-first styling framework
- **Shadcn/UI**: Pre-built component library

### Backend Integration
- **API Routes**: RESTful and GraphQL endpoints
- **Database**: Prisma ORM with PostgreSQL, MySQL, SQLite
- **Authentication**: NextAuth.js, Clerk, Auth0
- **Real-time**: WebSocket, Server-Sent Events
- **File Storage**: AWS S3, Cloudinary integration

### Deployment & DevOps
- **Vercel**: Seamless deployment and hosting
- **GitHub Integration**: Version control and CI/CD
- **Environment Management**: Development, staging, production
- **Performance Optimization**: Code splitting, lazy loading

## Prompting Best Practices

### Structure Your Requests

1. **Context First**: Always provide project context and goals
2. **Specific Requirements**: List technical and UI requirements
3. **Tech Stack**: Specify frameworks and libraries
4. **Success Criteria**: Define what "done" looks like

### Effective Prompt Patterns

#### App Structure Prompts
```
Build a [type] application using Next.js and TypeScript.

Core features:
- [Feature 1 with specific details]
- [Feature 2 with user interactions]
- [Feature 3 with data requirements]

Tech requirements:
- Next.js 14 with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- [Database/Auth solution]

UI requirements:
- Responsive design (mobile-first)
- Modern, clean interface
- Accessibility compliance
- [Specific design preferences]
```

#### Component Development
```
Create a [component name] component that:
- [Primary functionality]
- [User interactions]
- [Data props and types]
- [Styling requirements]

Include:
- TypeScript interfaces
- Proper error handling
- Loading states
- Responsive design
- Accessibility features
```

### Common Use Cases

#### E-commerce Applications
- Product catalogs with search and filtering
- Shopping cart and checkout flows
- User authentication and profiles
- Payment processing integration
- Order management systems

#### Dashboard Applications
- Data visualization with charts
- Real-time updates and notifications
- User management and permissions
- Settings and configuration panels
- Analytics and reporting features

#### Content Management
- CRUD operations for content
- Rich text editing capabilities
- Media upload and management
- SEO optimization features
- Multi-user collaboration

## Stage-Specific Guidelines

### App Skeleton Stage
Focus on:
- Project structure and folder organization
- Core page layouts and navigation
- Basic routing configuration
- Initial component hierarchy
- Database schema design

### Page UI Stage
Emphasize:
- Detailed component design
- User interaction patterns
- Form handling and validation
- Loading and error states
- Responsive behavior

### Flow Connections Stage
Prioritize:
- Navigation transitions
- User journey optimization
- State management between pages
- URL structure and routing
- Error boundary handling

## Performance Guidelines

### Code Quality
- Use TypeScript for type safety
- Implement proper error boundaries
- Follow React best practices (hooks, memo, callback)
- Optimize re-renders with useMemo and useCallback
- Use proper dependency arrays in useEffect

### Performance Optimization
- Implement code splitting with dynamic imports
- Use Next.js Image component for optimized images
- Minimize bundle size with tree shaking
- Implement proper caching strategies
- Use server components where appropriate

### SEO and Accessibility
- Proper heading hierarchy (h1-h6)
- Semantic HTML elements
- Alt text for images
- Keyboard navigation support
- Screen reader compatibility
- Meta tags and Open Graph

## Common Patterns and Solutions

### Authentication Flow
```typescript
// NextAuth.js setup with multiple providers
import NextAuth from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import CredentialsProvider from 'next-auth/providers/credentials'

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    CredentialsProvider({
      // Custom credential logic
    })
  ],
  pages: {
    signIn: '/auth/signin',
    signUp: '/auth/signup',
  },
  callbacks: {
    session: async ({ session, token }) => {
      // Custom session handling
      return session
    }
  }
}
```

### Database Operations
```typescript
// Prisma client with type safety
import { prisma } from '@/lib/prisma'

export async function getUsers() {
  try {
    const users = await prisma.user.findMany({
      include: {
        posts: true,
        profile: true,
      },
      orderBy: {
        createdAt: 'desc',
      },
    })
    return users
  } catch (error) {
    console.error('Database error:', error)
    throw new Error('Failed to fetch users')
  }
}
```

### API Route Pattern
```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    // Implementation logic
    const data = await fetchData()
    
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

## Error Handling Best Practices

### Client-Side Error Boundaries
```typescript
'use client'

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
      <button
        onClick={() => reset()}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Try again
      </button>
    </div>
  )
}
```

### Loading States
```typescript
import { Skeleton } from '@/components/ui/skeleton'

export function LoadingCard() {
  return (
    <div className="p-4 border rounded-lg">
      <Skeleton className="h-4 w-3/4 mb-2" />
      <Skeleton className="h-4 w-1/2 mb-4" />
      <Skeleton className="h-32 w-full" />
    </div>
  )
}
```

## Deployment Considerations

### Environment Variables
```bash
# .env.local
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### Vercel Deployment
- Automatic deployments from GitHub
- Environment variable management
- Custom domains and SSL
- Analytics and performance monitoring
- Preview deployments for pull requests

## Common Pitfalls to Avoid

1. **Hydration Mismatches**: Ensure server and client render the same content
2. **Missing Dependencies**: Include all dependencies in useEffect arrays
3. **Memory Leaks**: Clean up subscriptions and timeouts
4. **Poor Error Handling**: Always handle loading and error states
5. **Accessibility Issues**: Test with keyboard navigation and screen readers
6. **Performance Issues**: Avoid unnecessary re-renders and large bundle sizes
