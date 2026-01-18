# Defines the data structure that flows through the LangGraph pipeline

from typing import TypedDict, List, Optional
from pydantic import BaseModel
from enum import Enum   

# Telling Python what keys exists and what type each value is

                        
                                                  
class Severity(str, Enum):                      
    CRITICAL = "critical"                       
    HIGH = "high"                               
    MEDIUM = "medium"                           
    LOW = "low"

class Issue(BaseModel):
    type: str
    severity: Severity # Forces 4 values
    message: str
    line_number: Optional[int]
    suggestion: Optional[str]

class AgentState(BaseModel):
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
