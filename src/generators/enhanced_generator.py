"""
Enhanced Multi-Tool RAG Prompt Generator with Advanced Prompting Strategies
Incorporates best practices from Lovable.dev, Bolt.new, and other AI development tools
"""

import os
import yaml
import chromadb
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from src.core.types import (
    PromptStage, SupportedTool, TaskContext, PromptResult, 
    ToolProfile, PromptingStrategy, AppStructure, PageSpec, FlowConnection
)

class EnhancedMultiToolGenerator:
    """Enhanced prompt generator with advanced strategies and tool-specific optimizations"""
    
    def __init__(self, data_directory: str = "data", chroma_directory: str = "chroma_gemini"):
        self.data_dir = Path(data_directory)
        self.chroma_client = chromadb.PersistentClient(path=chroma_directory)
        self.tool_profiles = self._load_tool_profiles()
        self.prompting_strategies = self._load_prompting_strategies()
        
    def _load_tool_profiles(self) -> Dict[str, ToolProfile]:
        """Load enhanced tool profiles with prompting strategies"""
        profiles = {}
        
        # Lovable profile with C.L.E.A.R. framework
        profiles[SupportedTool.LOVABLE.value] = ToolProfile(
            tool_name="Lovable.dev",
            format="structured_sections",
            tone="expert_casual",
            preferred_use_cases=[
                "react_development", "ui_scaffolding", "supabase_integration",
                "component_optimization", "responsive_design"
            ],
            few_shot_examples=[
                {
                    "input": "Create a task management dashboard",
                    "output": "Build a React dashboard with task CRUD operations, filtering, and real-time updates using Supabase. Include responsive design with Tailwind CSS and shadcn/ui components."
                }
            ],
            prompting_guidelines={
                "framework": "C.L.E.A.R",
                "knowledge_base_required": True,
                "incremental_development": True,
                "mode_awareness": ["chat", "default"]
            },
            categories=["web_development", "frontend", "fullstack"],
            stage_templates={
                PromptStage.APP_SKELETON: "lovable_skeleton_template",
                PromptStage.PAGE_UI: "lovable_ui_template",
                PromptStage.FLOW_CONNECTIONS: "lovable_flow_template"
            },
            vector_namespace="lovable_docs",
            prompting_strategies=[
                PromptingStrategy(
                    strategy_type="structured",
                    template="Context: {context}\nTask: {task}\nGuidelines: {guidelines}\nConstraints: {constraints}",
                    use_cases=["complex_features", "new_projects"],
                    effectiveness_score=0.9
                ),
                PromptingStrategy(
                    strategy_type="conversational",
                    template="Let's {action}. {description} {technical_details}",
                    use_cases=["feature_additions", "debugging"],
                    effectiveness_score=0.8
                )
            ],
            constraints=[
                "react_typescript_only",
                "supabase_backend",
                "tailwind_styling",
                "responsive_required"
            ],
            optimization_tips=[
                "Use Knowledge Base extensively",
                "Implement incremental development",
                "Leverage Chat mode for planning",
                "Be explicit about constraints"
            ],
            common_pitfalls=[
                "overly_complex_single_prompts",
                "insufficient_context",
                "ignoring_knowledge_base"
            ]
        )
        
        # Bolt.new profile with enhancement features
        profiles[SupportedTool.BOLT.value] = ToolProfile(
            tool_name="Bolt.new",
            format="enhanced_prompts",
            tone="technical_precise",
            preferred_use_cases=[
                "rapid_prototyping", "web_applications", "javascript_projects",
                "iterative_development", "code_refinement"
            ],
            few_shot_examples=[
                {
                    "input": "Todo app",
                    "output": "Create a React todo application with TypeScript, featuring task creation, editing, deletion, and filtering. Include local storage persistence, responsive design with Tailwind CSS, and accessibility features."
                }
            ],
            prompting_guidelines={
                "enhancement_feature": True,
                "file_targeting": True,
                "webcontainer_aware": True,
                "incremental_changes": True
            },
            categories=["web_development", "prototyping", "javascript"],
            stage_templates={
                PromptStage.APP_SKELETON: "bolt_architecture_template",
                PromptStage.PAGE_UI: "bolt_component_template",
                PromptStage.FLOW_CONNECTIONS: "bolt_integration_template"
            },
            vector_namespace="bolt_docs",
            prompting_strategies=[
                PromptingStrategy(
                    strategy_type="structured",
                    template="Enhanced detailed prompt with complete specifications and constraints",
                    use_cases=["complex_applications", "production_ready"],
                    effectiveness_score=0.95
                )
            ],
            constraints=[
                "webcontainer_limitations",
                "browser_compatible_only",
                "no_native_binaries"
            ],
            optimization_tips=[
                "Use enhance prompt feature",
                "Target specific files",
                "Lock critical files",
                "Break into incremental steps"
            ],
            common_pitfalls=[
                "context_window_overflow",
                "too_many_simultaneous_changes",
                "webcontainer_incompatible_requests"
            ]
        )
        
        return profiles
    
    def _load_prompting_strategies(self) -> Dict[str, List[PromptingStrategy]]:
        """Load advanced prompting strategies"""
        return {
            "meta_prompting": [
                PromptingStrategy(
                    strategy_type="meta",
                    template="Review my prompt: '{original_prompt}' and suggest improvements for clarity, specificity, and effectiveness.",
                    use_cases=["prompt_optimization", "learning"],
                    effectiveness_score=0.85
                )
            ],
            "reverse_meta": [
                PromptingStrategy(
                    strategy_type="reverse_meta",
                    template="Summarize what we accomplished: {results}. Create a reusable prompt template for similar tasks.",
                    use_cases=["knowledge_capture", "template_creation"],
                    effectiveness_score=0.8
                )
            ]
        }
    
    def generate_enhanced_prompt(
        self,
        context: TaskContext,
        strategy: str = "auto",
        include_optimizations: bool = True
    ) -> PromptResult:
        """Generate enhanced prompt with advanced strategies"""
        
        # Get tool profile
        tool_profile = self.tool_profiles.get(context.target_tool.value)
        if not tool_profile:
            raise ValueError(f"Unsupported tool: {context.target_tool}")
        
        # Retrieve relevant context from vector database
        collection = self.chroma_client.get_or_create_collection(
            name=tool_profile.vector_namespace
        )
        
        # Query for relevant examples and documentation
        query_results = collection.query(
            query_texts=[f"{context.task_type} {context.description}"],
            n_results=5
        )
        
        # Determine optimal prompting strategy
        if strategy == "auto":
            strategy = self._determine_optimal_strategy(context, tool_profile)
        
        # Generate base prompt
        base_prompt = self._generate_base_prompt(context, tool_profile, query_results)
        
        # Apply tool-specific optimizations
        if include_optimizations:
            optimized_prompt = self._apply_tool_optimizations(
                base_prompt, context, tool_profile
            )
        else:
            optimized_prompt = base_prompt
        
        # Calculate confidence score
        confidence = self._calculate_confidence_score(context, query_results, tool_profile)
        
        # Prepare enhancement suggestions
        enhancement_suggestions = self._generate_enhancement_suggestions(
            context, tool_profile
        )
        
        # Determine next suggested stage
        next_stage = self._suggest_next_stage(context)
        
        return PromptResult(
            prompt=optimized_prompt,
            stage=context.stage,
            tool=context.target_tool,
            confidence_score=confidence,
            sources=[doc for doc in query_results['documents'][0]] if query_results['documents'] else [],
            next_suggested_stage=next_stage,
            enhancement_suggestions=enhancement_suggestions,
            applied_strategy=strategy,
            tool_specific_optimizations=tool_profile.optimization_tips
        )
    
    def _determine_optimal_strategy(self, context: TaskContext, profile: ToolProfile) -> str:
        """Determine the best prompting strategy based on context"""
        if context.stage == PromptStage.APP_SKELETON:
            return "structured"
        elif len(context.technical_requirements) > 5:
            return "structured"
        elif context.stage in [PromptStage.DEBUGGING, PromptStage.OPTIMIZATION]:
            return "conversational"
        else:
            return "conversational"
    
    def _generate_base_prompt(
        self,
        context: TaskContext,
        profile: ToolProfile,
        query_results: Dict
    ) -> str:
        """Generate base prompt using tool-specific templates"""
        
        if profile.tool_name == "Lovable.dev":
            return self._generate_lovable_prompt(context, query_results)
        elif profile.tool_name == "Bolt.new":
            return self._generate_bolt_prompt(context, query_results)
        else:
            return self._generate_generic_prompt(context, query_results)
    
    def _generate_lovable_prompt(self, context: TaskContext, query_results: Dict) -> str:
        """Generate Lovable-optimized prompt using C.L.E.A.R. framework"""
        
        # Structured format for complex tasks
        if context.stage == PromptStage.APP_SKELETON:
            return f"""Context: You are building a {context.project_name} using Lovable with React, TypeScript, and Supabase.

Task: {context.description}

Guidelines:
- Use modern React patterns with TypeScript
- Implement responsive design with Tailwind CSS
- Integrate Supabase for backend functionality
- Follow accessibility best practices
- Use shadcn/ui components for consistent UI

Technical Requirements:
{chr(10).join(f"- {req}" for req in context.technical_requirements)}

UI Requirements:
{chr(10).join(f"- {req}" for req in context.ui_requirements)}

Constraints:
{chr(10).join(f"- {constraint}" for constraint in context.constraints)}

Before starting, please confirm you understand the project requirements from the Knowledge Base."""
        
        else:
            # Conversational format for incremental development
            return f"""Let's {context.task_type.lower().replace('_', ' ')} for the {context.project_name} project.

{context.description}

Requirements:
{chr(10).join(f"- {req}" for req in context.technical_requirements + context.ui_requirements)}

Please ensure the implementation maintains consistency with existing components and follows our established patterns."""
    
    def _generate_bolt_prompt(self, context: TaskContext, query_results: Dict) -> str:
        """Generate Bolt.new optimized prompt for enhancement feature"""
        
        base_description = f"""Create a {context.task_type.lower().replace('_', ' ')} for {context.project_name}.

Core Functionality:
{context.description}

Technical Specifications:
{chr(10).join(f"- {req}" for req in context.technical_requirements)}

UI/UX Requirements:
{chr(10).join(f"- {req}" for req in context.ui_requirements)}

Constraints:
{chr(10).join(f"- {constraint}" for constraint in context.constraints)}"""

        # Add stage-specific details
        if context.stage == PromptStage.APP_SKELETON:
            base_description += f"""

Architecture Requirements:
- Modern web application structure
- Component-based organization
- Proper state management
- Responsive design implementation
- Performance optimization"""
        
        return base_description
    
    def _generate_generic_prompt(self, context: TaskContext, query_results: Dict) -> str:
        """Generate generic prompt for other tools"""
        return f"""Project: {context.project_name}
Task: {context.task_type.replace('_', ' ').title()}

Description: {context.description}

Technical Requirements:
{chr(10).join(f"- {req}" for req in context.technical_requirements)}

UI Requirements:
{chr(10).join(f"- {req}" for req in context.ui_requirements)}

Constraints:
{chr(10).join(f"- {constraint}" for constraint in context.constraints)}

Please implement this feature following best practices for {context.target_tool.value}."""
    
    def _apply_tool_optimizations(
        self,
        base_prompt: str,
        context: TaskContext,
        profile: ToolProfile
    ) -> str:
        """Apply tool-specific optimizations"""
        
        optimized = base_prompt
        
        # Lovable-specific optimizations
        if profile.tool_name == "Lovable.dev":
            if context.stage == PromptStage.DEBUGGING:
                optimized += "\n\nPlease use Chat mode to discuss the issue before implementing changes."
            
            if "responsive" in context.ui_requirements:
                optimized += "\n\nEnsure mobile-first responsive design using Tailwind breakpoints (sm:, md:, lg:)."
        
        # Bolt.new specific optimizations
        elif profile.tool_name == "Bolt.new":
            optimized = f"[Note: Consider using the Enhance Prompt feature ⭐ for this request]\n\n{optimized}"
            
            if len(context.technical_requirements) > 3:
                optimized += "\n\nSuggestion: Break this into smaller, incremental changes for better results."
        
        return optimized
    
    def _calculate_confidence_score(
        self,
        context: TaskContext,
        query_results: Dict,
        profile: ToolProfile
    ) -> float:
        """Calculate confidence score for the generated prompt"""
        score = 0.5  # Base score
        
        # Boost for relevant documentation
        if query_results.get('documents') and query_results['documents'][0]:
            score += 0.2
        
        # Boost for complete requirements
        if context.technical_requirements and context.ui_requirements:
            score += 0.2
        
        # Boost for appropriate tool selection
        if context.task_type in profile.preferred_use_cases:
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_enhancement_suggestions(
        self,
        context: TaskContext,
        profile: ToolProfile
    ) -> List[str]:
        """Generate suggestions for prompt enhancement"""
        suggestions = []
        
        if not context.technical_requirements:
            suggestions.append("Add specific technical requirements for better results")
        
        if not context.constraints:
            suggestions.append("Define constraints to avoid scope creep")
        
        if profile.tool_name == "Lovable.dev" and context.stage == PromptStage.APP_SKELETON:
            suggestions.append("Consider setting up Knowledge Base with project requirements")
        
        if profile.tool_name == "Bolt.new":
            suggestions.append("Use the enhance prompt feature for more detailed specifications")
        
        return suggestions
    
    def _suggest_next_stage(self, context: TaskContext) -> Optional[PromptStage]:
        """Suggest the next logical development stage"""
        stage_progression = {
            PromptStage.APP_SKELETON: PromptStage.PAGE_UI,
            PromptStage.PAGE_UI: PromptStage.FLOW_CONNECTIONS,
            PromptStage.FLOW_CONNECTIONS: PromptStage.FEATURE_SPECIFIC,
            PromptStage.FEATURE_SPECIFIC: PromptStage.OPTIMIZATION
        }
        return stage_progression.get(context.stage)
    
    def generate_meta_prompt(self, original_prompt: str, context: TaskContext) -> str:
        """Generate meta prompt for prompt improvement"""
        return f"""Please analyze and improve this prompt for {context.target_tool.value}:

Original Prompt:
"{original_prompt}"

Analysis Criteria:
1. Clarity and specificity
2. Completeness of requirements
3. Tool-specific optimization
4. Constraint definition
5. Expected outcome clarity

Please provide:
1. Identified weaknesses
2. Improved version
3. Explanation of changes
4. Tool-specific recommendations"""
    
    def generate_reverse_meta_prompt(self, results: str, context: TaskContext) -> str:
        """Generate reverse meta prompt for knowledge capture"""
        return f"""Please create a reusable prompt template based on this successful implementation:

Project Context: {context.project_name}
Task Type: {context.task_type}
Tool Used: {context.target_tool.value}

Results Achieved:
{results}

Please provide:
1. Summary of what worked well
2. Reusable prompt template
3. Key success factors
4. Potential variations for similar tasks"""

# Example usage and testing
if __name__ == "__main__":
    generator = EnhancedMultiToolGenerator()
    
    # Test Lovable prompt generation
    lovable_context = TaskContext(
        task_type="user_authentication",
        project_name="TaskMaster Pro",
        description="Implement secure user authentication with email/password login, signup, and protected routes",
        stage=PromptStage.APP_SKELETON,
        technical_requirements=[
            "Supabase Auth integration",
            "TypeScript implementation",
            "Protected route middleware",
            "Form validation"
        ],
        ui_requirements=[
            "Responsive login/signup forms",
            "Loading states",
            "Error message display",
            "Clean, modern design"
        ],
        constraints=[
            "No social login",
            "Email verification required",
            "Mobile-first design"
        ],
        target_tool=SupportedTool.LOVABLE
    )
    
    result = generator.generate_enhanced_prompt(lovable_context)
    print("Lovable Enhanced Prompt:")
    print("=" * 50)
    print(result.prompt)
    print(f"\nConfidence Score: {result.confidence_score}")
    print(f"Applied Strategy: {result.applied_strategy}")
    print("\nEnhancement Suggestions:")
    for suggestion in result.enhancement_suggestions or []:
        print(f"- {suggestion}")
