# System Prompts Integration Guide

## Overview

This guide consolidates the best practices, patterns, and prompting strategies from leading AI development tools including Cursor, Cline, v0, Devin AI, Lovable, Same.dev, Windsurf, RooCode, and many others.

## Universal AI Tool Patterns

### 1. Tool Calling Best Practices

#### Schema Adherence (From Cursor/Windsurf)
```markdown
CRITICAL RULES:
- ALWAYS follow tool call schema exactly as specified
- Provide ALL required parameters
- NEVER call tools that are not explicitly provided
- NEVER refer to tool names when speaking to users
- Use natural language descriptions instead
```

#### Parameter Validation (From Cline/RooCode)
```markdown
Before calling any tool:
1. Analyze what information you already have
2. Determine what information you need
3. Check if all required parameters are available or can be inferred
4. If missing required parameters, ask user rather than making assumptions
5. DO NOT ask for optional parameters unless necessary
```

#### Sequential vs Parallel Processing (From Cursor/Same.dev)
```markdown
- Use parallel tool calls when operations are independent
- Use sequential calls when each step depends on the previous result
- Reflect on tool results before proceeding to next action
- Wait for confirmation of critical operations before continuing
```

### 2. Code Generation Patterns

#### Progressive Enhancement (From v0/Lovable)
```markdown
Phase 1: Core Structure
- Basic functionality implementation
- Essential component hierarchy
- Fundamental user interactions

Phase 2: User Experience
- Enhanced UI/UX elements
- Responsive design implementation
- Accessibility features
- Error handling and loading states

Phase 3: Advanced Features
- Performance optimizations
- Advanced interactions
- Integration enhancements
- Testing and validation
```

#### File Organization (From Cline/RooCode)
```markdown
Project Structure Best Practices:
- Create dedicated project directories
- Use appropriate file paths and naming conventions
- Structure projects logically for the specific type
- Make projects easily runnable without additional setup
- Split functionality into smaller, focused modules
- Extract related functionalities into separate files
```

### 3. Context Management

#### Reading Before Writing (From Cursor/Orchids)
```markdown
MANDATORY RULES:
- MUST read file contents before editing (unless creating new files)
- Understand surrounding context, especially imports and dependencies
- Consider existing patterns and conventions
- Analyze framework choices and coding standards
- Never assume file contents without verification
```

#### Context Optimization (From Lovable/Cline)
```markdown
Context Usage:
- NEVER read files already provided in context
- Use search tools to find relevant code patterns
- Batch related operations together
- Maintain awareness of project dependencies
- Update references when making changes
```

### 4. Error Handling and Debugging

#### Systematic Debugging (From Same.dev/Warp)
```markdown
Debugging Methodology:
1. Address root cause, not symptoms
2. Add descriptive logging and error messages
3. Create test functions to isolate problems
4. Use debugging tools FIRST before examining code
5. Analyze debugging output before making changes
```

#### Linter Error Management (From Cursor)
```markdown
Linter Error Rules:
- Fix errors if solution is clear
- Do not make uneducated guesses
- Maximum 3 attempts to fix errors on same file
- Stop and ask user for guidance after 3rd attempt
- Ensure changes are compatible with existing codebase
```

## Tool-Specific Optimization Patterns

### Cursor Agent Patterns
```markdown
Key Strategies:
- Immediate action bias - execute plans without waiting for confirmation
- Beautiful, modern UI with best UX practices
- Read file contents before making substantial edits
- Use parallel tool calls when operations are independent
- Clean up temporary files after task completion
```

### Cline/RooCode Patterns
```markdown
Key Strategies:
- Step-by-step iterative approach
- Wait for user confirmation after each tool use
- Use <thinking> tags for analysis before tool calls
- Prefer dedicated tools over shell commands
- Combine tools for comprehensive analysis
```

### v0 Development Patterns
```markdown
Key Strategies:
- Production-ready code with no placeholders
- Component-based architecture
- Semantic HTML with proper ARIA support
- Responsive design with mobile-first approach
- Strong TypeScript typing throughout
```

### Lovable Development Patterns
```markdown
Key Strategies:
- C.L.E.A.R. framework implementation
- Beautiful, responsive designs by default
- Toast notifications for user feedback
- Search-replace for targeted changes
- Debug tools first, then code modifications
```

### Devin AI Patterns
```markdown
Key Strategies:
- Planning vs Standard mode distinction
- Comprehensive context gathering before implementation
- Security-first approach (never expose secrets)
- Framework-aware development
- Git best practices with descriptive commits
```

## Advanced Prompting Techniques

### 1. Meta-Prompting Patterns (From Multiple Tools)

#### Self-Improvement Loop
```markdown
Prompt Enhancement Cycle:
1. Analyze current prompt effectiveness
2. Identify areas for improvement (clarity, specificity, context)
3. Generate enhanced version with better structure
4. Test enhanced prompt and collect feedback
5. Iterate based on results
```

#### Multi-Modal Reasoning
```markdown
Planning Integration:
- Use mermaid diagrams for complex workflows
- Create visual architecture representations
- Implement todo lists for complex multi-step tasks
- Use progressive disclosure for complex features
```

### 2. Domain-Specific Patterns

#### Web Development (From v0/Same.dev)
```markdown
Web App Creation:
- Beautiful, modern UI with best UX practices
- Responsive design from mobile-first
- Accessibility compliance (ARIA, semantic HTML)
- Performance optimization considerations
- Security best practices implementation
```

#### Database Integration (From Bolt/Supabase patterns)
```markdown
Database Best Practices:
- Row Level Security (RLS) for every table
- Descriptive migration summaries
- Type safety throughout application
- Foreign key constraints for data integrity
- Default values for consistency
```

### 3. Quality Assurance Patterns

#### Testing Integration (From Kiro/Manus)
```markdown
Test-Driven Development:
- Write tests before implementing features
- Incremental progress with early testing
- No big jumps in complexity
- Each step builds on previous steps
- Integration testing for connected components
```

#### Documentation Standards (From Multiple Tools)
```markdown
Documentation Requirements:
- Clear, specific task definitions
- Complete technical context
- Success criteria definition
- Tool-specific optimizations noted
- Progressive complexity maintenance
```

## Implementation Guidelines

### 1. Project Initialization

#### Setup Phase
```markdown
1. Analyze project requirements and tech stack
2. Create appropriate directory structure
3. Set up configuration files and dependencies
4. Establish coding standards and conventions
5. Initialize version control with proper gitignore
```

#### Knowledge Base Integration
```markdown
Before Any Coding (Lovable Pattern):
1. Upload Project Requirements Document (PRD)
2. Include tech stack specifications
3. Add UI/UX guidelines and design system
4. Specify out-of-scope features explicitly
5. Define project constraints and limitations
```

### 2. Development Workflow

#### Incremental Development
```markdown
Session Structure:
Session 1: Basic structure and core functionality
Session 2: User interface and essential interactions
Session 3: Data integration and business logic
Session 4: Advanced features and optimizations
Session 5: Testing, debugging, and refinement
```

#### Code Quality Maintenance
```markdown
Quality Checks:
- Functionality matches requirements
- Code quality meets established standards
- Accessibility guidelines followed
- Responsive design verified
- Performance benchmarks met
- Documentation updated appropriately
```

### 3. Error Recovery and Adaptation

#### Failure Handling
```markdown
When Things Go Wrong:
1. Analyze root cause systematically
2. Gather additional context if needed
3. Adapt approach based on new information
4. Communicate changes to user
5. Learn from failures for future improvements
```

#### Context Adaptation
```markdown
Dynamic Adjustment:
- Monitor tool effectiveness continuously
- Adapt strategies based on project type
- Switch approaches when current method fails
- Maintain backward compatibility when possible
- Document lessons learned for future reference
```

## Integration with Enhanced RAG System

### 1. Pattern Recognition
- Identify project type and optimal tool patterns
- Match user requirements to appropriate frameworks
- Select best practices based on technical context
- Adapt prompting style to tool capabilities

### 2. Strategy Selection
- Analyze user intent and technical requirements
- Choose appropriate development methodology
- Select optimal tool-specific patterns
- Implement progressive enhancement approach

### 3. Quality Optimization
- Monitor prompt effectiveness continuously
- Collect feedback for iterative improvement
- Maintain pattern library for reuse
- Update strategies based on new tool capabilities

## Conclusion

This integration guide provides a comprehensive framework for leveraging the best practices from leading AI development tools. By implementing these patterns systematically, you can significantly improve the quality and effectiveness of AI-assisted development across various platforms and project types.

The key to success is understanding that different tools excel in different scenarios, and the best approach often involves combining strategies from multiple sources while maintaining consistency with the specific tool's strengths and limitations.
