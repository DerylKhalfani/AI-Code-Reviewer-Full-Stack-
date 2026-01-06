# AI Code Review Agent - Architecture & Implementation Guide

## Project Overview
Build an AI agent using LangGraph that analyzes code and provides comprehensive feedback like a senior engineer - checking security, style, complexity, best practices, and 5 additional areas.

---

## File Structure

```
code-review-agent/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── graph.py               # LangGraph state machine
│   │   ├── state.py               # AgentState TypedDict definition
│   │   └── nodes.py               # Node functions for graph
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── security.py            # Tool 1: Security analysis
│   │   ├── style.py               # Tool 2: Style checking
│   │   ├── complexity.py          # Tool 3: Complexity metrics
│   │   ├── best_practices.py      # Tool 4: Best practices
│   │   ├── test_coverage.py       # Tool 5: Test suggestions
│   │   ├── performance.py         # Tool 6: Performance check
│   │   ├── accessibility.py       # Tool 7: A11y for frontend
│   │   ├── dependencies.py        # Tool 8: Dependency scan
│   │   └── documentation.py       # Tool 9: Doc quality
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── language_detector.py   # Auto-detect programming language
│   │   └── response_formatter.py  # Format conversational output
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Main component
│   │   ├── components/
│   │   │   ├── CodeInput.jsx      # Monaco editor wrapper
│   │   │   ├── LanguageSelector.jsx
│   │   │   ├── AnalyzeButton.jsx
│   │   │   └── ResultsDisplay.jsx # Shows analysis
│   │   ├── api/
│   │   │   └── client.js          # Axios API wrapper
│   │   └── main.jsx
│   ├── package.json
│   └── .env.example
└── README.md
```

---

## What Each Component Does

### Backend Components

#### **main.py**
- FastAPI application setup
- CORS middleware configuration
- POST `/api/analyze` endpoint - receives code, returns analysis
- GET `/health` endpoint - health check
- Request validation (max 2000 lines, non-empty code)

#### **agent/state.py**
- Define `AgentState` TypedDict that flows through the graph
- Contains: input code, detected language
- Contains: results from each tool (security_issues, style_issues, etc.)
- Contains: final summary and aggregated issues list

#### **agent/graph.py**
- Create StateGraph from LangGraph
- Add nodes for each analysis tool
- Define edges (flow from one node to next)
- Add synthesis node at end to aggregate all findings
- Compile graph into executable workflow

#### **agent/nodes.py**
- Define node functions that match graph structure
- Each node function: takes state, calls corresponding tool, returns updated state
- Example: `security_node(state) -> calls security tool -> returns state with security_issues populated`
- Synthesis node: aggregates all issues, generates conversational summary using LLM

#### **tools/security.py**
- Analyze code for security vulnerabilities
- Check for: hardcoded secrets (API keys, passwords), SQL injection patterns, XSS risks, insecure crypto
- Use: regex patterns for common patterns + LLM for complex analysis
- Return: List of Issue dicts with severity, message, line number, suggestion

#### **tools/style.py**
- Check code style and formatting
- Look for: naming conventions, line length, indentation, consistent formatting
- Use: regex for patterns + LLM for readability suggestions
- Return: List of style issues

#### **tools/complexity.py**
- Calculate complexity metrics
- Measure: lines of code, cyclomatic complexity, nesting depth, function count
- Use: simple parsing + counting
- Return: Dict with metrics + LLM interpretation of whether it's too complex

#### **tools/best_practices.py**
- Check adherence to best practices
- Look for: error handling, logging, type hints (Python), proper async usage
- Use: LLM analysis with specific prompts
- Return: List of best practice violations

#### **tools/test_coverage.py**
- Suggest areas that need tests
- Identify: functions without tests, edge cases not covered, critical paths
- Use: LLM to analyze code and suggest test cases
- Return: List of test suggestions

#### **tools/performance.py**
- Identify potential performance issues
- Look for: inefficient loops, unnecessary computations, N+1 queries, memory leaks
- Use: pattern matching + LLM analysis
- Return: List of performance concerns

#### **tools/accessibility.py**
- Check accessibility (mainly for frontend code)
- Look for: missing alt text, poor contrast, missing ARIA labels, keyboard navigation
- Use: regex patterns + LLM for semantic HTML
- Return: List of accessibility issues (empty if not frontend code)

#### **tools/dependencies.py**
- Check for vulnerable dependencies
- Look for: import statements, package.json references
- Use: pattern matching to identify packages + LLM to suggest updates
- Return: List of dependency concerns

#### **tools/documentation.py**
- Assess documentation quality
- Check: docstrings, comments, README, inline explanations
- Use: LLM to evaluate documentation completeness
- Return: List of documentation gaps

#### **utils/language_detector.py**
- Auto-detect programming language from code
- Check: file extensions in comments, syntax patterns, keywords
- Use: pattern matching + LLM as fallback
- Return: language string (python, javascript, typescript, etc.)

#### **utils/response_formatter.py**
- Format agent output into conversational response
- Generate: natural language summary of findings
- Prioritize: issues by severity
- Create: actionable recommendations
- Use: LLM to synthesize all findings into readable narrative

---

### Frontend Components

#### **App.jsx**
- Main application component
- Manage state: code input, language selection, loading, results
- Handle: analyze button click -> API call -> display results
- Layout: header, code input section, results section

#### **components/CodeInput.jsx**
- Wrapper around Monaco Editor
- Props: value, onChange, language
- Features: syntax highlighting, line numbers, auto-complete
- Size: full height editor

#### **components/LanguageSelector.jsx**
- Dropdown to manually select language
- Options: Auto-detect, Python, JavaScript, TypeScript, Java, Go, etc.
- Shows: detected language if auto-detect is on

#### **components/AnalyzeButton.jsx**
- Button to trigger analysis
- States: default, loading, disabled
- Shows: loading spinner when analyzing

#### **components/ResultsDisplay.jsx**
- Display analysis results
- Sections: conversational summary, issues by category
- For each issue: severity badge, message, line number, suggestion
- Features: collapsible sections, syntax highlighting for code snippets
- Show: "No issues found" if everything is clean

#### **api/client.js**
- Axios wrapper for API calls
- POST to `/api/analyze` with code and language
- Error handling: network errors, validation errors, server errors
- Returns: parsed JSON response

---

## Data Flow

### 1. User Input
- User types/pastes code into Monaco Editor
- Selects language (or keeps auto-detect)
- Clicks "Analyze" button

### 2. Frontend Processing
- CodeInput onChange updates state
- AnalyzeButton onClick triggers API call
- Loading state shows spinner

### 3. API Request
```
POST /api/analyze
{
  "code": "def example():\n    password = '123456'\n    return password",
  "language": "python"  // or null for auto-detect
}
```

### 4. Backend Processing
- FastAPI validates request (max lines, non-empty)
- Language detection (if not provided)
- Create initial AgentState with code + language
- Pass state through LangGraph
- Each node runs sequentially, updating state:
  - Security node -> finds hardcoded password
  - Style node -> checks formatting
  - Complexity node -> calculates metrics
  - ... (all 9 tools run)
- Synthesis node aggregates all findings
- Response formatter creates conversational summary

### 5. API Response
```json
{
  "summary": "I found 1 critical security issue and 2 minor style issues...",
  "issues": [
    {
      "type": "security",
      "severity": "critical",
      "message": "Hardcoded password detected on line 2",
      "line_number": 2,
      "suggestion": "Use environment variables: os.getenv('PASSWORD')"
    },
    ...
  ],
  "metrics": {
    "total_issues": 3,
    "critical": 1,
    "high": 0,
    "medium": 0,
    "low": 2
  }
}
```

### 6. Frontend Display
- ResultsDisplay receives response
- Shows conversational summary at top
- Groups issues by type (security, style, etc.)
- Each issue shown as card with severity badge
- Code snippets with line numbers highlighted

---

## LangGraph Structure

### State Machine Flow
```
START
  ↓
Initialize State (code, language)
  ↓
Security Analysis Node
  ↓
Style Analysis Node
  ↓
Complexity Analysis Node
  ↓
Best Practices Node
  ↓
Test Coverage Node
  ↓
Performance Node
  ↓
Accessibility Node
  ↓
Dependencies Node
  ↓
Documentation Node
  ↓
Synthesis Node (aggregate + summarize)
  ↓
END
```

### Why Sequential (Not Parallel)?
- Each analysis can build on previous findings
- Easier to debug and understand flow
- State accumulates through pipeline
- Still fast enough (each node is quick)
- Can parallelize later if needed

---

## Tool Implementation Strategy

### Each Tool Follows Pattern:

**1. Pattern Matching (Regex)**
- Fast, deterministic checks
- Common issues like hardcoded secrets
- Syntax violations

**2. LLM Analysis**
- Complex reasoning
- Context-dependent suggestions
- Semantic understanding

**3. Hybrid Approach**
- Use regex to find candidates
- Use LLM to validate and explain
- Best accuracy + performance

### Example: Security Tool Flow
```
1. Regex scan for patterns:
   - API_KEY = "..."
   - password = "..."
   - SELECT * FROM users WHERE id = ${input}

2. For each match:
   - Extract context (surrounding lines)
   - Ask LLM: "Is this a security issue? Why?"
   - Get severity and suggestion

3. Return structured issues
```

---

## Conversational Output Format

### Structure
```
[SUMMARY PARAGRAPH]
I analyzed your code and found X issues: Y critical, Z high, etc.
The most important issues to address are...

[CRITICAL ISSUES]
🔴 Critical: Hardcoded API key on line 15
   This exposes your credentials. Use environment variables instead.

[HIGH PRIORITY]
🟠 High: SQL injection vulnerability on line 42
   User input is directly concatenated. Use parameterized queries.

[MEDIUM PRIORITY]
🟡 Medium: Function 'process_data' has high complexity
   Consider breaking into smaller functions for readability.

[LOW PRIORITY]
🟢 Low: Missing docstring for function 'helper'
   Add a docstring to explain what this function does.

[RECOMMENDATIONS]
I recommend prioritizing the security issues first...
```

---

## What You Need to Build

### Day 1: Backend Foundation
- [ ] FastAPI setup with CORS
- [ ] Request/response models with Pydantic
- [ ] `/api/analyze` endpoint skeleton
- [ ] Language detector utility
- [ ] AgentState definition
- [ ] Basic LangGraph structure (empty nodes)

### Day 2: Tool Implementation (3-4 tools)
- [ ] Security tool (regex + LLM)
- [ ] Style tool
- [ ] Complexity tool
- [ ] Connect tools to graph nodes
- [ ] Test individual tools

### Day 3: Complete All Tools
- [ ] Remaining 6 tools
- [ ] Synthesis node with LLM
- [ ] Response formatter
- [ ] End-to-end backend testing

### Day 4: Frontend Basics
- [ ] React app with Vite
- [ ] Monaco Editor integration
- [ ] Language selector
- [ ] API client setup
- [ ] Basic layout

### Day 5: Frontend Polish
- [ ] ResultsDisplay component
- [ ] Issue cards with severity badges
- [ ] Collapsible sections
- [ ] Loading states
- [ ] Error handling

### Day 6: Integration & UX
- [ ] Test full flow
- [ ] Add inline annotations (stretch)
- [ ] Improve conversational output
- [ ] Handle edge cases
- [ ] Responsive design

### Day 7: Deploy & Document
- [ ] Deploy backend to Railway
- [ ] Deploy frontend to Vercel
- [ ] Write README with examples
- [ ] Test with real code samples
- [ ] Take screenshots for portfolio

---

## Key Decisions Made

✅ Input: Direct code paste (start simple)
✅ Tools: 9 total (4 core + 5 advanced)
✅ Framework: LangGraph (modern, explicit control)
✅ Output: Conversational with structured issues
✅ UI: Monaco editor with good + some impressive features
✅ Language: Auto-detect with manual override
✅ Limits: 2000 lines max
✅ Implementation: Regex + LLM hybrid

---

## Environment Variables Needed

**Backend (.env)**
```
ANTHROPIC_API_KEY=your_key_here
CORS_ORIGINS=http://localhost:5173
MAX_CODE_LINES=2000
```

**Frontend (.env)**
```
VITE_API_URL=http://localhost:8000
```

---

## Testing Strategy

### Manual Testing
- Test with Python code (various issues)
- Test with JavaScript code
- Test with TypeScript code
- Test empty input (should fail validation)
- Test huge input (should fail validation)
- Test with clean code (should find nothing)

### Real Examples to Test
- Code with hardcoded secrets
- Code with SQL injection
- Code with poor naming
- Code with high complexity
- Code without tests
- Well-written code (positive case)