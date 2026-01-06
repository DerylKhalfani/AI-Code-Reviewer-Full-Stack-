# Project Context for Claude Code

## Project: AI Code Review Agent

### What We're Building
An intelligent code review system that analyzes source code and provides comprehensive feedback similar to a senior engineer's code review. The system uses LangGraph to orchestrate 9 different analysis tools and generates conversational, actionable feedback.

---

## Tech Stack

**Backend:**
- Python 3.11+
- FastAPI - REST API framework
- LangGraph - Agent orchestration framework
- LangChain Anthropic - LLM integration
- Claude Sonnet 4 - Primary LLM
- Pydantic - Data validation

**Frontend:**
- React 18
- Vite - Build tool
- Monaco Editor - Code editor component
- Tailwind CSS - Styling
- Axios - HTTP client

**Deployment:**
- Railway - Backend hosting
- Vercel - Frontend hosting

---

## Architecture Overview

### System Flow
```
User pastes code into Monaco Editor
    ↓
Frontend sends POST to /api/analyze
    ↓
Backend validates input (max 2000 lines)
    ↓
Auto-detect or use manual language selection
    ↓
Create AgentState with code + language
    ↓
LangGraph executes sequential pipeline:
    - Security Analysis
    - Style Check
    - Complexity Analysis
    - Best Practices
    - Test Coverage Suggestions
    - Performance Check
    - Accessibility Check
    - Dependency Scan
    - Documentation Quality
    ↓
Synthesis node aggregates findings
    ↓
Response formatter creates conversational output
    ↓
Return JSON to frontend
    ↓
Display results with severity badges and suggestions
```

---

## Key Components

### Backend Structure

**main.py** - FastAPI application entry point
- CORS middleware for frontend communication
- POST /api/analyze - main analysis endpoint
- Request validation using Pydantic
- Error handling for invalid inputs

**agent/state.py** - State definition
- AgentState TypedDict that flows through graph
- Contains input (code, language)
- Contains results from each tool
- Contains final summary and aggregated issues

**agent/graph.py** - LangGraph state machine
- StateGraph with 9 analysis nodes + 1 synthesis node
- Sequential execution (each node runs after previous)
- Nodes update shared state
- Compiled graph returns final state

**agent/nodes.py** - Node implementations
- Each node function takes state, calls tool, returns updated state
- Pattern: `def security_node(state: AgentState) -> AgentState`
- Synthesis node uses LLM to create conversational summary

**tools/** - Analysis implementations
- Each tool is independent, reusable function
- Takes code and language as input
- Returns structured issues (type, severity, message, line, suggestion)
- Uses hybrid approach: regex patterns + LLM reasoning

**utils/language_detector.py** - Auto-detect programming language
- Checks syntax patterns and keywords
- Returns language string (python, javascript, typescript, etc.)

**utils/response_formatter.py** - Format conversational output
- Takes all issues and creates natural language summary
- Prioritizes by severity
- Generates actionable recommendations

---

## Analysis Tools (9 Total)

### Tool 1: Security Analysis
**Purpose:** Find security vulnerabilities
**Checks:**
- Hardcoded secrets (API keys, passwords, tokens)
- SQL injection patterns
- XSS vulnerabilities
- Insecure cryptography
- Command injection risks

**Implementation:** Regex for common patterns + LLM for complex analysis

### Tool 2: Style Check
**Purpose:** Code formatting and style
**Checks:**
- Naming conventions
- Line length
- Indentation consistency
- Formatting standards
- Code readability

**Implementation:** Regex for patterns + LLM for readability suggestions

### Tool 3: Complexity Analysis
**Purpose:** Measure code complexity
**Checks:**
- Lines of code
- Cyclomatic complexity
- Nesting depth
- Function count
- Cognitive load

**Implementation:** Simple parsing + LLM interpretation

### Tool 4: Best Practices
**Purpose:** Language-specific best practices
**Checks:**
- Error handling
- Proper logging
- Type hints (Python)
- Async/await usage
- Resource management

**Implementation:** LLM analysis with specific prompts

### Tool 5: Test Coverage Suggestions
**Purpose:** Identify untested code
**Checks:**
- Functions without tests
- Edge cases not covered
- Critical paths missing tests

**Implementation:** LLM to suggest test cases

### Tool 6: Performance Check
**Purpose:** Find performance bottlenecks
**Checks:**
- Inefficient loops
- Unnecessary computations
- N+1 query patterns
- Memory leak risks

**Implementation:** Pattern matching + LLM analysis

### Tool 7: Accessibility Check
**Purpose:** Frontend accessibility (only for HTML/JS/React)
**Checks:**
- Missing alt text
- Poor contrast
- Missing ARIA labels
- Keyboard navigation issues

**Implementation:** Regex patterns + LLM for semantic HTML

### Tool 8: Dependency Scan
**Purpose:** Identify problematic dependencies
**Checks:**
- Outdated packages
- Known vulnerabilities
- Unused imports

**Implementation:** Pattern matching for imports + LLM suggestions

### Tool 9: Documentation Quality
**Purpose:** Assess code documentation
**Checks:**
- Missing docstrings
- Inadequate comments
- Unclear variable names
- Missing README sections

**Implementation:** LLM evaluation of documentation completeness

---

## Data Models

### Request Schema
```python
{
  "code": str,              # Required, max 2000 lines
  "language": Optional[str] # None = auto-detect
}
```

### Issue Schema
```python
{
  "type": str,              # security, style, complexity, etc.
  "severity": str,          # critical, high, medium, low
  "message": str,           # Description of issue
  "line_number": int | None,# Specific line if applicable
  "suggestion": str | None  # How to fix it
}
```

### Response Schema
```python
{
  "summary": str,           # Conversational summary
  "issues": List[Issue],    # All issues found
  "metrics": {
    "total_issues": int,
    "critical": int,
    "high": int,
    "medium": int,
    "low": int
  }
}
```

---

## Frontend Components

### App.jsx
Main application component that manages:
- Code input state
- Language selection state
- Loading state
- Analysis results state
- API call orchestration

### CodeInput.jsx
Monaco Editor wrapper with:
- Syntax highlighting
- Line numbers
- Auto-complete
- Configurable language

### LanguageSelector.jsx
Dropdown for language selection:
- Auto-detect option
- Manual selection for: Python, JavaScript, TypeScript, Java, Go, etc.
- Shows detected language

### ResultsDisplay.jsx
Display analysis results:
- Conversational summary at top
- Issues grouped by type
- Severity badges (red, orange, yellow, green)
- Collapsible sections
- Code snippets with line highlighting

---

## Important Constraints

### Input Validation
- Maximum 2000 lines of code
- Code cannot be empty
- Language must be valid or null (auto-detect)

### Tool Execution
- Sequential execution (not parallel)
- Each tool has timeout of 10 seconds
- Failed tools don't crash entire analysis
- Continue with remaining tools if one fails

### LLM Usage
- Use Claude Haiku for individual tool analysis (fast, cheap)
- Use Claude Sonnet for synthesis (better quality)
- Keep prompts concise to minimize tokens
- Include relevant context only

### Response Format
- Always return valid JSON
- Conversational tone, not technical jargon
- Actionable suggestions, not just problems
- Prioritize critical issues first

---

## Development Approach

### The human wants to:
1. Build this mostly themselves with Claude Code as a guide
2. Understand every component deeply
3. Learn LangGraph through building
4. Get hints and suggestions, not full implementations
5. Make architectural decisions with guidance

### When helping:
- Explain concepts before suggesting code
- Show patterns and best practices
- Point out potential pitfalls
- Suggest alternatives with trade-offs
- Ask clarifying questions when requirements are ambiguous
- Provide examples but let human implement

### What human has already decided:
✅ LangGraph for agent framework (not basic LangChain)
✅ Sequential tool execution (not parallel)
✅ Conversational output format
✅ Monaco editor for frontend
✅ Direct code paste input (GitHub URL later)
✅ Auto-detect + manual language selection
✅ 2000 line limit
✅ Regex + LLM hybrid approach for tools

---

## Common Patterns

### Tool Implementation Pattern
```python
def analyze_tool(code: str, language: str) -> List[Issue]:
    """
    1. Use regex to find potential issues
    2. For each candidate, use LLM to validate
    3. Return structured Issue objects
    """
    pass
```

### Node Implementation Pattern
```python
def tool_node(state: AgentState) -> AgentState:
    """
    1. Extract code and language from state
    2. Call corresponding tool function
    3. Update state with results
    4. Return updated state
    """
    pass
```

### LLM Prompt Pattern
```python
prompt = f"""
Analyze this {language} code for {specific_issue_type}.

Code:
{code_snippet}

Return JSON with:
- is_issue: boolean
- severity: critical|high|medium|low
- message: description
- suggestion: how to fix
"""
```

---

## Testing Strategy

### During Development
- Test each tool independently first
- Use simple code examples with known issues
- Verify issue detection accuracy
- Check response formatting

### Example Test Cases
- Python code with hardcoded password
- JavaScript code with SQL injection
- TypeScript code with high complexity
- Code with no issues (should return clean report)
- Empty code (should fail validation)
- 3000+ line code (should fail validation)

---

## Deployment Configuration

### Backend Environment Variables
```
ANTHROPIC_API_KEY=sk-ant-...
CORS_ORIGINS=http://localhost:5173,https://yourapp.vercel.app
MAX_CODE_LINES=2000
```

### Frontend Environment Variables
```
VITE_API_URL=http://localhost:8000  # Dev
VITE_API_URL=https://your-railway-app.up.railway.app  # Prod
```

---

## Next Project (Week 2)

After completing this code review agent, the human will build:
- **Universal Documentation Q&A System**
- Uses Advanced RAG (not GraphRAG initially)
- Supports any document type (medical, legal, technical, business)
- Agent-controlled RAG retrieval
- LangChain for RAG utilities
- Context-aware responses with citations

This context helps you understand the broader learning path.

---

## Key Principles

1. **Quality over features** - Better to have 5 tools working perfectly than 9 half-working
2. **Iterative development** - Get one thing working end-to-end, then add more
3. **User experience matters** - Conversational output is more important than technical accuracy
4. **Error handling** - Always fail gracefully with helpful messages
5. **Learning by doing** - Human wants to understand, not just copy-paste

---

## When Human Asks for Help

### Good responses:
- "Let's think about how this tool should work. What patterns would you check for?"
- "Here's how LangGraph nodes typically update state: [pattern]. Want to try implementing it?"
- "I notice this might cause an issue with [X]. Have you considered [Y] approach?"
- "The trade-off here is [A] vs [B]. Which fits your use case better?"

### Avoid:
- Dumping full file implementations without explanation
- Making decisions without discussing options
- Assuming understanding of advanced concepts
- Providing code without context of why it works

---

## Timeline Expectations

**Day 1-2:** Backend foundation + LangGraph basics + 1-2 tools working
**Day 3-4:** Complete all 9 tools + synthesis node
**Day 5-6:** Frontend + integration
**Day 7:** Deploy + polish + documentation

This is an aggressive timeline. If human is behind schedule, help prioritize core features over nice-to-haves.

---

## Success Metrics

### Project is successful when:
✅ Can analyze real code samples
✅ Finds actual security issues
✅ Provides helpful suggestions
✅ Conversational output is clear
✅ Frontend is usable
✅ Deployed and accessible
✅ Human understands architecture
✅ Ready to demo in interview

### Bonus achievements:
- GitHub URL input working
- Inline code annotations
- Multiple language support tested
- Performance is acceptable (<10 seconds)
- Error messages are helpful
- Mobile responsive design
