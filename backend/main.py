# this file is the entry point that 

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from agent.graph import graph_app
from agent.state import *

load_dotenv() 
api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="AI Code Review Agent") # creating the app

# allowing Next.js frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# code that is requested to be reviewed
class CodeRequest(BaseModel):
    code: str
    language: str | None = None
    
# response based on the code requested to be reviewed
class CodeResponse(BaseModel):
    summary: str # summary of the code
    issues: list # issues of the code
    metrics: dict

    

# Checking if server is running
@app.get('/health')
def health_check():
    return {'status': 'health'}

@app.post('/api/analyze')
def analyze_code(request: CodeRequest):

    code = request.code
    language = request.language
    # Validate input

    if not code.strip():
        raise HTTPException(status_code=400, detail='Code cannot be empty')
    
    lines = len(code.split('\n'))
    if lines >= 2000:
        raise HTTPException(status_code=400, detail='Line number exceeded')
    
    # Detecting language if not provided
    if language is None:
        language = 'python'

    
    # Calling langgraph pipeline
    initial_state = AgentState(
        code = code,
        language = language,
        style_issues = [],
        security_issues = [],
        best_practices_issues = [],
        test_coverage_issues = [],
        performance_issues = [],
        accessibility_issues = [],
        dependency_issues = [],
        documentation_issues = [],
        complexity_issues = [],

        all_issues = [],
        summary = ""
    )

    # Running the graph
    final_state = graph_app.invoke(initial_state)

    summary = final_state.summary
    issues = final_state.all_issues
    metrics = {'total_issues': len(issues),
               'critical': 0,
               'high': 0,
               'medium': 0,
               'low': 0}
    
    for issue in issues:
        severity = issue.severity.lower()

        if severity in metrics:
            metrics[severity] += 1

    return CodeResponse(
        summary = summary,
        issues = [issue.dict() for issue in issues],
        metrics = metrics
    )
        

    
