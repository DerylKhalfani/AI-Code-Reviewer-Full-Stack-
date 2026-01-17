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
            response_format = Issue, # json format
            )

            issues.append(response.choices[0].message.parsed)
    
    return issues

# Tool 2
# Style tools
def analyze_style_tool(code: str, language: str) -> List[Issue]:
    """                                                          
      Analyze code for style issues: naming, line length, spacing, 
      formatting                                                       
    """ 

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    issues = []

    special_patterns = [
        # Long lines (>120 chars)                            
        r'^.{121,}$',             
                                                            
        # No spaces around operators                         
        r'\w+=\w+',    # x=5                                  
        r'\w+-\w+',    # x-5                                  
        r'\w+==\w+',   # x==5                                 
                                                            
        # Inconsistent naming (camelCase vs snake_case)      
        r'def [a-z]+[A-Z]',  # camelCase function in Python   
        r'function [a-z]+_[a-z]+',  # snake_case function in JS 
                                                                                    
        # Multiple spaces                                    
        r'  +',                          
                                                            
        # Trailing whitespace                                
        r' +$',  
    ]

    for pattern in special_patterns:

        # Regex patterns to find candidates
        matches = re.finditer(pattern, code, re.MULTILINE)

        for match in matches:

            line_number = code[:match.start()].count('\n') + 1
            snippet = match.group(0)

            # LLM to validate
            response = client.beta.chat.completions.parse(
                model = 'gpt-5-nano',
                messages = [
                    {'role':'system', 'content': 'You are a style expert'},
                    {'role':'user', 'content':f'Analyze this {language} code for style issues: \n{snippet}\nLine: {line_number}\nIs this a style violation? If yes, suggest how to fix it.'}
                ],
                response_format=Issue
            )

            issues.append(response.choices[0].message.parsed)

    # Return List[Issue]
    return issues

# Tool 3
# Complexity tools
def analyze_complexity_tool(code: str, language: str) -> List[Issue]:
    """                                                          
      Analyze code for complexity issues: nesting, long functions, nested loops, long conditionals                             
    """ 

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    issues = []

    special_patterns = [
        # Deep nesting (count leading spaces/tabs)           
        r'^\s{16,}',  # 4+ levels of indentation (if using 4  spaces)                                              
                                                            
        # Long functions (find function start, count lines to next function)                                      
        r'^def \w+.*?(?=^def|\Z)',  # Python, use re.MULTILINE | re.DOTALL                                         
        r'^function \w+.*?(?=^function|\Z)',  # JS            
                                                            
        # Multiple nested loops                              
        r'for.*\n.*for.*\n.*for',  # 3 nested loops           
        r'while.*\n.*while',  # Nested while                  
                                                            
        # Long conditionals                                  
        r'if.*and.*and.*and',  # 4+ conditions                
        r'\|\|.*\|\|.*\|\|',  # Multiple OR conditions
    ]

    for pattern in special_patterns:

        # Regex patterns to find candidates
        matches = re.finditer(pattern, code, re.MULTILINE | re.DOTALL)

        for match in matches:
            # line number
            line_number = code[:match.start()].count('\n') + 1

            # LLM to validate
            response = client.beta.chat.completions.parse(
            model='gpt-5-nano',
            messages=[
                {'role':'system', 'content': 'You are a complexity expert.'},
                {'role':'user', 'content': f'Please analyze this code: \n{match} with its line number: {line_number}.'}
            ],
            response_format = Issue, # json format
            )

            issues.append(response.choices[0].message.parsed)
    
    # Return List[Issue]
    return issues

        

        

# Tool 4
# Best practices tool
def analyze_best_practices_tool(code: str, language: str) -> List[Issue]:
    """                                                          
      Analyze code for best practices issues: excpet, missing try-catch, missing type hints, magic numbers, TODO left in code                                                 
    """ 

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    issues = []

    special_patterns = [
        # Bare except (Python)                                           
        r'except\s*:',                                                    
                                                                        
        # Missing try-catch                                              
        r'open\(',  # File operations without try                         
        r'fetch\(',  # Network calls without catch                        
                                                                        
        # Missing type hints (Python)                                    
        r'def \w+\([^)]*\):(?!\s*->)',  # No return type                  
                                                                        
        # Unhandled promises (JS)                                        
        r'\.then\([^)]+\)(?!\s*\.catch)',                                 
                                                                        
        # Magic numbers                                                  
        r'\b\d{4,}\b',  # Numbers with 4+ digits                          
        r'if.*[<>]=?\s*\d+',  # Numbers in conditionals                   
                                                                        
        # TODO comments left in code                                     
        r'#\s*TODO',                                                      
        r'//\s*TODO',
    ]

    for pattern in special_patterns:

        # Regex patterns to find candidates
        matches = re.finditer(pattern, code)

        for match in matches:

            line_number = code[:match.start()].count('\n') + 1

            # LLM to validate
            response = client.beta.chat.completions.parse(
                model='gpt-5-nano',
                messages=[
                {'role':'system', 'content': 'You are a best practices expert.'},
                {'role':'user', 'content': f'Please analyze this code: \n{match} with its line number: {line_number}.'}
            ],
            response_format = Issue, # json format
            )

            issues.append(response.choices[0].message.parsed)


    # Return List[Issue]
    return issues

# Tool 5
# Test coverage tool
def analyze_test_coverage_tool(code: str, language: str) -> List[Issue]:
    """                                                          
      Analyze code for test_coverage issues: finding test files for all function definitions                                                  
    """ 

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    issues = []

    special_patterns = [
        # Find all function definitions                                  
        r'^def (\w+)\(',  # Python (use re.MULTILINE)                     
        r'^function (\w+)\(',  # JS                                       
        r'^\s*const \w+ = \([^)]*\) =>',  # Arrow functions               
                                                                        
        # Find test files                                                
        r'test_.*\.py',                                                   
        r'.*\.test\.js',                                                  
        r'.*\.spec\.js',
    ]

    for pattern in special_patterns:

        # Regex patterns to find candidates
        matches = re.finditer(pattern, code)

        for match in matches:

            line_number = code[:match.start()].count('\n') + 1

            # LLM to validate
            response = client.beta.chat.completions.parse(
                model='gpt-5-nano',
                messages=[
                {'role':'system', 'content': 'You are a test coverage expert.'},
                {'role':'user', 'content': f'Please analyze this code: \n{match} with its line number: {line_number}.'}
            ],
            response_format = Issue, # json format
            )

            issues.append(response.choices[0].message.parsed)


    # Return List[Issue]
    return issues

# Tool 6
# Performance tool
def analyze_performance_tool(code: str, language: str) -> List[Issue]:
    """                                                          
      Analyze code for performance issues: nested loops, list comprehensions, repeated operations, missing list comprehensions opportunities, N+1 query patterns                                                  
    """ 

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    issues = []

    special_patterns = [
        # Nested loops                                                   
        r'for.*in.*:\s*for.*in',  # Python                                
        r'for\s*\(.*\).*for\s*\(',  # JS/C-style                          
                                                                        
        # List comprehension in loop (Python)                            
        r'for.*:\s*.*\[.*for.*in.*\]',                                    
                                                                        
        # Repeated operations in loop                                    
        r'for.*:\s*.*\.append\(.*\)',  # Appending to same list many times
                                                                        
        # Missing list comprehension opportunities                       
        r'for.*:\s*\w+\.append\(',  # Could be list comp                  
                                                                        
        # N+1 query patterns (look for DB calls in loops)                
        r'for.*:\s*.*\.query\(',                                          
        r'for.*:\s*.*\.get\(',
    ]

    for pattern in special_patterns:

        # Regex patterns to find candidates
        matches = re.finditer(pattern, code)

        for match in matches:

            line_number = code[:match.start()].count('\n') + 1

            # LLM to validate
            response = client.beta.chat.completions.parse(
                model='gpt-5-nano',
                messages=[
                {'role':'system', 'content': 'You are a performance expert.'},
                {'role':'user', 'content': f'Please analyze this code: \n{match} with its line number: {line_number}.'}
            ],
            response_format = Issue, # json format
            )

            issues.append(response.choices[0].message.parsed)


    # Return List[Issue]
    return issues

# Tool 7
# Accessibility tool
def analyze_accessibility_tool(code: str, language: str) -> List[Issue]:
    """
    Analyze code for accessibility issues: image w/o alt, buttons w/o text-label, links w/o text, input w/o label
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    issues = []

    if language not in ['html', 'javascript', 'jsx', 'react', 'tsx']:
        return []
    
    special_patterns = [
        # Images without alt                                             
        r'<img(?![^>]*alt=)[^>]*>',                                       
                                                                        
        # Buttons without text/aria-label                                
        r'<button(?![^>]*aria-label=)[^>]*>\s*</button>',                 
                                                                        
        # Links without text                                             
        r'<a[^>]*>\s*</a>',                                               
                                                                        
        # Missing ARIA attributes                                        
        r'<div[^>]*onclick(?![^>]*role=)',  # clickable div without role  
                                                                        
        # Input without label                                            
        r'<input(?![^>]*aria-label=)(?![^>]*id=)',
    ]

    for pattern in special_patterns:

        # Regex patterns to find candidates
        matches = re.finditer(pattern, code)

        for match in matches:

            line_number = code[:match.start()].count('\n') + 1

            # LLM to validate
            response = client.beta.chat.completions.parse(
                model='gpt-5-nano',
                messages=[
                {'role':'system', 'content': 'You are a accessibility expert.'},
                {'role':'user', 'content': f'Please analyze this code: \n{match} with its line number: {line_number}.'}
            ],
            response_format = Issue, # json format
            )

            issues.append(response.choices[0].message.parsed)


    # Return List[Issue]
    return issues

# Tool 8
# Dependency tool
def analyze_dependency_tool(code: str, language: str) -> List[Issue]:
    """
    Analyze code for dependency issues: import statement (python and js)
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    issues = []

    special_patterns = [
        # Import statements                                              
        r'^import\s+(\w+)',  # Python                                     
        r'^from\s+(\w+)\s+import',  # Python                              
        r'import\s+{[^}]+}\s+from\s+["\']([^"\']+)["\']\s+(\w+)\s+from',  # JS named                     
                                                                        
        # Unused imports (find import, search if name appears elsewhere) 
        r'^import\s+(\w+).*$',  # Capture name, then search for it in code
                                                                        
        # Multiple imports from same package                             
        # Use collections.Counter after extracting all package names
    ]

    for pattern in special_patterns:

        # Regex patterns to find candidates
        matches = re.finditer(pattern, code)

        for match in matches:

            line_number = code[:match.start()].count('\n') + 1

            # LLM to validate
            response = client.beta.chat.completions.parse(
                model='gpt-5-nano',
                messages=[
                {'role':'system', 'content': 'You are a dependency expert.'},
                {'role':'user', 'content': f'Please analyze this code: \n{match} with its line number: {line_number}.'}
            ],
            response_format = Issue, # json format
            )

            issues.append(response.choices[0].message.parsed)


    # Return List[Issue]
    return issues

# Tool 9
# Documentation tool
def analyze_documentation_tool(code: str, language: str) -> List[Issue]:
    """
    Analyze code for documentation issues: functions w/o (docstrings, JsDoc), classes w/o docstrings, single letter variables (i,k)
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    issues = []

    special_patterns = [
        # Functions without docstrings (Python)                          
        r'def \w+\([^)]*\):\s*\n\s*(?!"""|\'\'\')(?!\s*#)',               
                                                                        
        # Functions without JSDoc (JS)                                   
        r'function \w+\([^)]*\)\s*{(?!\s*/\*\*)',                         
                                                                        
        # Classes without docstrings                                     
        r'class \w+.*:\s*\n\s*(?!""")',                                   
                                                                        
        # Single letter variable names (except i, j, k for loops)        
        r'\b([a-hln-z])\s*=',  # Exclude i,j,k,m                          
                                                                        
        # TODO/FIXME comments                                            
        r'#\s*(TODO|FIXME|XXX|HACK)',
    ]

    for pattern in special_patterns:

        # Regex patterns to find candidates
        matches = re.finditer(pattern, code)

        for match in matches:

            line_number = code[:match.start()].count('\n') + 1

            # LLM to validate
            response = client.beta.chat.completions.parse(
                model='gpt-5-nano',
                messages=[
                {'role':'system', 'content': 'You are a documentation expert.'},
                {'role':'user', 'content': f'Please analyze this code: \n{match} with its line number: {line_number}.'}
            ],
            response_format = Issue, # json format
            )

            issues.append(response.choices[0].message.parsed)


    # Return List[Issue]
    return issues



    
