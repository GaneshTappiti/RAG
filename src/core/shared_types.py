"""
Shared data types for Lovable.dev prompt generator
Description: Common data structures used across all modules
"""

from dataclasses import dataclass
from typing import List

@dataclass
class TaskContext:
    """Context for a specific task type"""
    task_type: str
    project_name: str
    description: str
    technical_requirements: List[str]
    ui_requirements: List[str]
    constraints: List[str]

@dataclass
class ProjectInfo:
    """Project information structure"""
    name: str
    description: str
    tech_stack: List[str]
    target_audience: str
    requirements: List[str]
