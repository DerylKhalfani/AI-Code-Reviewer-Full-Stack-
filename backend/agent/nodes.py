# This file is for adding nodes for all tools and one to sum them up

import os
from .state import *
from typing import List
from tools.tools import * # importing tools
from openai import OpenAI

def security_node(state: AgentState) -> AgentState:
    issues = analyze_security_tool(state.code, state.language)
    state.security_issues = issues  # Fixed: removed type annotation
    return state

def style_node(state: AgentState) -> AgentState:
    issues = analyze_style_tool(state.code, state.language)
    state.style_issues = issues  # Fixed: removed type annotation
    return state

def complexity_node(state: AgentState) -> AgentState:
    issues = analyze_complexity_tool(state.code, state.language)
    state.complexity_issues = issues  # Fixed: removed type annotation
    return state

def best_practices_node(state: AgentState) -> AgentState:
    issues = analyze_best_practices_tool(state.code, state.language)
    state.best_practices_issues = issues  # Fixed: removed type annotation
    return state

def test_coverage_node(state: AgentState) -> AgentState:
    issues = analyze_test_coverage_tool(state.code, state.language)
    state.test_coverage_issues = issues  # Fixed: removed type annotation
    return state

def performance_node(state: AgentState) -> AgentState:
    issues = analyze_performance_tool(state.code, state.language)
    state.performance_issues = issues  # Fixed: removed type annotation
    return state

def dependency_node(state: AgentState) -> AgentState:
    issues = analyze_dependency_tool(state.code, state.language)
    state.dependency_issues = issues  # Fixed: removed type annotation
    return state

def documentation_node(state: AgentState) -> AgentState:
    issues = analyze_documentation_tool(state.code, state.language)
    state.documentation_issues = issues  # Fixed: removed type annotation
    return state

def accessibility_node(state: AgentState) -> AgentState:
    issues = analyze_accessibility_tool(state.code, state.language)
    state.accessibility_issues = issues  # Fixed: removed type annotation
    return state

def synthesis_node(state: AgentState) -> AgentState:
    """
    Returning all types of issues and its summaries
    """
    
    # adding all types of issue to all_issues
    state.all_issues.extend(state.security_issues)
    state.all_issues.extend(state.accessibility_issues)
    state.all_issues.extend(state.style_issues)
    state.all_issues.extend(state.documentation_issues)
    state.all_issues.extend(state.dependency_issues)
    state.all_issues.extend(state.performance_issues)
    state.all_issues.extend(state.test_coverage_issues)
    state.all_issues.extend(state.best_practices_issues)
    state.all_issues.extend(state.complexity_issues)
    
    # llm call for all issues to eget the summary
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.beta.chat.completions.parse(
        model = 'gpt-5-mini', # use a bit better model
        messages = [
            {'role': 'system', 'content': 
             """The summary should:                           
                - Prioritize critical issues first            
                - Group similar issues together               
                - Give an overall assessment ("Your code has 3
                  critical security issues, 5 style problems...")
                - Provide actionable next steps               
                - Be conversational, not a list'""" },
            {'role': 'user', 'content': f'Here are all the issues found: {state.all_issues}. Write a conversational summary like a senior engineer' }
        ]
    )

    state.summary = response.choices[0].message.content

    return state


    


