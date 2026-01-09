import re
import os
from typing import List
from openai import OpenAI
from agent.state import Issue
from dotenv import load_dotenv

load_dotenv()

# Tools to be used as an specific analyzer issues

# Tool 1
# Security tools (Hybrid: regex and LLM)
def analyze_security_tool(code: str, language: str) -> List[Issue]:
    """
    Analyze code for security vulnerabilities
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    issues = []

    # Use regex to find potential secrets
    secret_patterns = [
      r'api_key\s*=\s*["\']([^"\']+)["\']',
      r'password\s*=\s*["\']([^"\']+)["\']',
      r'token\s*=\s*["\']([^"\']+)["\']',
      r'sk-[a-zA-Z0-9]{32,}',  # OpenAI API key pattern
    ]

    for pattern in secret_patterns:
        
        #Find pattern using regex
        matches = re.finditer(pattern, code, re.IGNORECASE)
        for match in matches:

            # line number
            line_number = code[:match.start()].count('\n') + 1

            response = client.beta.chat.completions.parse(
            model='gpt-5-nano',
            messages=[
                {'role':'system', 'content': 'You are a security expert.'},
                {'role':'user', 'content': f'Please analyze this code: \n{match} with its line number: {line_number}.'}
            ],
            response_format = Issue,
            )

            issues.append(response.choices[0].message.parsed)
    
    return issues


    
