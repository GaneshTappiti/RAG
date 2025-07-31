"""
Enhanced Multi-Tool RAG Prompt Generator
Author: Enhanced RAG System
Description: Multi-stage prompt generator supporting various AI development tools
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Literal
from enum import Enum

class PromptStage(Enum):
    """Available prompt generation stages"""
    APP_SKELETON = "app_skeleton"
    PAGE_UI = "page_ui"
    FLOW_CONNECTIONS = "flow_connections"
    FEATURE_SPECIFIC = "feature_specific"
    DEBUGGING = "debugging"
    OPTIMIZATION = "optimization"

class SupportedTool(Enum):
    """Supported AI development tools"""
    LOVABLE = "lovable"
    UIZARD = "uizard"
    ADALO = "adalo"
    FLUTTERFLOW = "flutterflow"
    FRAMER = "framer"
    BUBBLE = "bubble"
    BOLT = "bolt"
    CURSOR = "cursor"
    CLINE = "cline"
    V0 = "v0"
    DEVIN = "devin"
    WINDSURF = "windsurf"
    ROOCODE = "roocode"
    MANUS = "manus"
    SAME_DEV = "same_dev"

@dataclass
class AppStructure:
    """Application structure for skeleton generation"""
    pages: List[str]
    components: List[str]
    features: List[str]
    navigation_flow: Dict[str, List[str]]

@dataclass
class PageSpec:
    """Page specification for UI generation"""
    page_name: str
    layout_type: str
    components: List[str]
    interactions: List[str]
    data_requirements: List[str]

@dataclass
class FlowConnection:
    """Flow connection for navigation mapping"""
    from_page: str
    to_page: str
    trigger: str
    animation: Optional[str] = None
    conditions: Optional[List[str]] = None

@dataclass
class TaskContext:
    """Enhanced context for a specific task type"""
    task_type: str
    project_name: str
    description: str
    stage: PromptStage
    technical_requirements: List[str]
    ui_requirements: List[str]
    constraints: List[str]
    target_tool: SupportedTool
    
    # Stage-specific data
    app_structure: Optional[AppStructure] = None
    page_spec: Optional[PageSpec] = None
    flow_connections: Optional[List[FlowConnection]] = None

@dataclass
class ProjectInfo:
    """Enhanced project information structure"""
    name: str
    description: str
    tech_stack: List[str]
    target_audience: str
    requirements: List[str]
    industry: Optional[str] = None
    complexity_level: Literal["simple", "medium", "complex"] = "medium"
    
@dataclass
class PromptingStrategy:
    """Prompting strategy configuration"""
    strategy_type: Literal["structured", "conversational", "meta", "reverse_meta", "iterative", "parallel", "planning_mode", "production_ready", "security_first"]
    template: str
    use_cases: List[str]
    effectiveness_score: float
    async_aware: bool = False  # For tools that handle asynchronous operations
    requires_confirmation: bool = False  # For tools that wait for user confirmation
    security_focused: bool = False  # For tools with security-first approaches

@dataclass
class ToolProfile:
    """Tool-specific configuration profile"""
    tool_name: str
    format: str
    tone: str
    preferred_use_cases: List[str]
    few_shot_examples: List[Dict[str, str]]
    prompting_guidelines: Dict[str, Any]
    categories: List[str]
    stage_templates: Dict[PromptStage, str]
    vector_namespace: str
    prompting_strategies: List[PromptingStrategy]
    constraints: List[str]
    optimization_tips: List[str]
    common_pitfalls: List[str]

@dataclass
class PromptResult:
    """Generated prompt result with metadata"""
    prompt: str
    stage: PromptStage
    tool: SupportedTool
    confidence_score: float
    sources: List[str]
    next_suggested_stage: Optional[PromptStage] = None
    regeneration_context: Optional[Dict[str, Any]] = None
    enhancement_suggestions: Optional[List[str]] = None
    applied_strategy: Optional[str] = None
    tool_specific_optimizations: Optional[List[str]] = None
