# Defines the data structure that flows through the LangGraph pipeline

from typing import TypedDict, List, Optional

# Telling Python what keys exists and what type each value is

class Issue(TypedDict):
    type: str
    severity: str
    message: str
    line_number: Optional[int]
    suggestion: Optional[str]

class AgentState(TypedDict):
    # Input Section
    code: str
    language: str

    # Tool
    # List of Issues
    style_issues: List[Issue] 
    security_issues: List[Issue]
    best_practices_issues: List[Issue]
    test_coverage_issues: List[Issue]
    performance_issues: List[Issue]
    accessibility_issues: List[Issue]
    dependency_issues: List[Issue]
    documentation_issues: List[Issue]
    complexity_issues: List[Issue]

    # Output section
    summary: str
    all_issues: List[Issue]
