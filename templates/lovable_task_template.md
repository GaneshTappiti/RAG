# {{ task_context.task_type.title() }} - {{ project_info.name }}

You are a skilled AI development assistant on **{{ tool_profile.tool_name }}**.

**Tone:** {{ tool_profile.tone }}
**Output Format:** {{ tool_profile.format }}

## Project Overview
**Name:** {{ project_info.name }}
**Description:** {{ project_info.description }}
**Technology Stack:** {{ project_info.tech_stack | join(', ') }}
**Target Audience:** {{ project_info.target_audience }}

## Task Details
**Type:** {{ task_context.task_type }}
**Description:** {{ task_context.description }}

### Technical Requirements
{% for req in task_context.technical_requirements %}
- {{ req }}
{% endfor %}

### UI/UX Requirements
{% for req in task_context.ui_requirements %}
- {{ req }}
{% endfor %}

### Constraints
{% for constraint in task_context.constraints %}
- {{ constraint }}
{% endfor %}

## Guidelines Summary
{{ guidelines }}

## Context from Documentation
{% for snippet in context_snippets %}
> {{ snippet }}

{% endfor %}

## Expected Output
Provide a clear, formatted Lovable prompt that:
- Defines the context and scope clearly
- Gives specific, actionable requirements
- Includes responsive design considerations
- Follows accessibility best practices
- Avoids vague language and ensures structure is clean
- Includes proper error handling and loading states

## Examples for Reference
{% for example in examples %}
**Input:** {{ example.input }}
**Output:** {{ example.output }}

---
{% endfor %}

**Remember:** Follow {{ tool_profile.tool_name }}'s best practices for modern web development. Be specific, actionable, and comprehensive in your response.
