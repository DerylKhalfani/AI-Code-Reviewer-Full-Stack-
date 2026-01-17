
Always Keep the code implementation simple. Don't add abstractions I didn't ask for. One file if possible.

# Project Context for Claude Code

## Project: AI Code Review Agent

An intelligent code review system that analyzes source code using LangGraph to orchestrate 9 analysis tools and generates conversational feedback like a senior engineer.

---

## Tech Stack

**Backend:** Python 3.11+, FastAPI, LangGraph, LangChain Anthropic, Claude Sonnet 4, Pydantic
**Frontend:** React 18, Vite, Monaco Editor, Tailwind CSS, Axios
**Deployment:** Railway (backend), Vercel (frontend)

---

## Architecture Flow

```
User Code → Frontend → /api/analyze → Validate (max 2000 lines) → Auto-detect language
    ↓
LangGraph Sequential Pipeline (9 tools):
    Security → Style → Complexity → Best Practices → Test Coverage
    → Performance → Accessibility → Dependency → Documentation
    ↓
Synthesis Node → Conversational Output → Display Results
```

---

## File Structure

**main.py** - FastAPI app with CORS, POST /api/analyze endpoint, Pydantic validation
**agent/state.py** - AgentState TypedDict (code, language, tool results, summary)
**agent/graph.py** - StateGraph with 9 analysis nodes + 1 synthesis node (sequential)
**agent/nodes.py** - Node functions: take state, call tool, return updated state
**tools/** - 9 independent analysis tools (regex + LLM hybrid)
**utils/language_detector.py** - Auto-detect language from syntax patterns
**utils/response_formatter.py** - Format conversational output prioritized by severity

---

## 9 Analysis Tools

1. **Security Analysis** - Hardcoded secrets, SQL injection, XSS, insecure crypto, command injection
2. **Style Check** - Naming conventions, line length, indentation, formatting, readability
3. **Complexity Analysis** - LOC, cyclomatic complexity, nesting depth, cognitive load
4. **Best Practices** - Error handling, logging, type hints, async/await, resource management
5. **Test Coverage** - Untested functions, missing edge cases, critical paths
6. **Performance Check** - Inefficient loops, unnecessary computations, N+1 queries, memory leaks
7. **Accessibility** - Alt text, contrast, ARIA labels, keyboard navigation (HTML/JS/React only)
8. **Dependency Scan** - Outdated packages, vulnerabilities, unused imports
9. **Documentation Quality** - Missing docstrings, inadequate comments, unclear names

All tools use **regex patterns + LLM validation** approach.

---

## Data Schemas

**Request:** `{ code: str (max 2000 lines), language: Optional[str] }`
**Issue:** `{ type: str, severity: str, message: str, line_number: int|None, suggestion: str|None }`
**Response:** `{ summary: str, issues: List[Issue], metrics: { total_issues, critical, high, medium, low } }`

---

## Key Constraints

**Input:** Max 2000 lines, non-empty, valid language or null (auto-detect)
**Execution:** Sequential (not parallel), 10s timeout per tool, failed tools don't crash analysis
**LLM Strategy:** GPT 5 nano for everything
**Output:** Valid JSON, conversational tone, actionable suggestions, critical issues first

---

## Common Patterns

### Tool Pattern
```python
def analyze_tool(code: str, language: str) -> List[Issue]:
    # 1. Regex to find candidates
    # 2. LLM to validate each
    # 3. Return structured Issues
```

### Node Pattern
```python
def tool_node(state: AgentState) -> AgentState:
    # 1. Extract code + language from state
    # 2. Call tool function
    # 3. Update state with results
    # 4. Return updated state
```

### LLM Prompt Pattern
```python
f"""Analyze this {language} code for {issue_type}.
Code: {snippet}
Return JSON: is_issue, severity, message, suggestion"""
```

---

## Frontend Components

**App.jsx** - Main state manager (code, language, loading, results, API calls)
**CodeInput.jsx** - Monaco Editor wrapper (syntax highlighting, line numbers, autocomplete)
**LanguageSelector.jsx** - Dropdown (auto-detect + manual selection)
**ResultsDisplay.jsx** - Results UI (summary, issues by type, severity badges, collapsible sections)

---

## Development Approach

**Human wants to:**
- Build mostly themselves with guided hints
- Understand every component deeply
- Learn LangGraph through building
- Get suggestions and alternatives, not full implementations
- Make architectural decisions with guidance

**When helping:**
- Explain concepts before code
- Show patterns and trade-offs
- Point out pitfalls
- Ask clarifying questions
- Let human implement after examples

**Decisions already made:**
✅ LangGraph (not basic LangChain)
✅ Sequential execution
✅ Conversational output
✅ Monaco editor
✅ Direct code paste (GitHub URL later)
✅ Auto-detect + manual language
✅ 2000 line limit
✅ Regex + LLM hybrid

---

## Environment Variables

**Backend:** `ANTHROPIC_API_KEY`, `CORS_ORIGINS`, `MAX_CODE_LINES`
**Frontend:** `VITE_API_URL` (localhost:8000 dev, Railway URL prod)

---

## Key Principles

1. **Quality over features** - 5 perfect tools > 9 half-working
2. **Iterative development** - End-to-end first, then expand
3. **User experience matters** - Conversational > technical accuracy
4. **Error handling** - Fail gracefully with helpful messages
5. **Learning by doing** - Understanding > copy-paste
