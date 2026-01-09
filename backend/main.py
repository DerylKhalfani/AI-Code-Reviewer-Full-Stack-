# this file is the entry point that 

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

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
    
    lines = code.split('\n').len()
    if lines >= 2000:
        raise HTTPException(status_code=400, detail='Line number exceeded')
    
    # Detecting language if not provided
    if language is None:
        language = 'python'

    
    # Calling langgraph pipeline

    
    # Formatting and returning
    # dummy for now
    response = {
        'summary': 'Analysis complete! No issues',
        'issues': [],
        'metrics': {
            'total_issues': 0,
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
    }

    return response

    
