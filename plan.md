# AI Code Review Agent - Plan

**Last Updated:** 2026-01-19

---

## Current Status

**Phase:** Building Frontend

### Done - Backend ✅
- FastAPI with /api/analyze endpoint working
- AgentState model (state.py)
- 9 analysis tools (tools.py)
- 9 nodes + synthesis node (nodes.py)
- LangGraph pipeline (graph.py)
- Backend tested and working

### Working On
- Frontend components

---

## Frontend Plan (Simple)

### Step 1: Main Page (app/page.tsx)
- [ ] Replace default Next.js page
- [ ] Add state management (code, language, loading, results, error)
- [ ] Create handleAnalyze function (POST to API)
- [ ] Build basic layout

### Step 2: CodeInput Component (components/CodeInput.tsx)
- [ ] Import Monaco Editor (dynamic, no SSR)
- [ ] Props: value, onChange, language
- [ ] Set height ~400px
- [ ] Enable line numbers + syntax highlighting

### Step 3: LanguageSelector (components/LanguageSelector.tsx)
- [ ] Simple dropdown
- [ ] Props: value, onChange
- [ ] Options: python, javascript, typescript, java, go, etc.

### Step 4: ResultsDisplay (components/ResultsDisplays.tsx)
- [ ] Show metrics cards (total, critical, high, medium, low)
- [ ] Show summary section
- [ ] Show issues list (grouped by severity or type)
- [ ] Add loading state
- [ ] Add empty state

### Step 5: Polish
- [ ] Error handling (empty code, >2000 lines, API errors)
- [ ] Styling with Tailwind
- [ ] Test end-to-end with backend

---

## API Contract

**Request to:** `POST http://localhost:8000/api/analyze`
```json
{
  "code": "string",
  "language": "python"
}
```

**Response:**
```json
{
  "summary": "string",
  "issues": [
    {
      "type": "security",
      "severity": "critical|high|medium|low",
      "message": "string",
      "line_number": 10,
      "suggestion": "string"
    }
  ],
  "metrics": {
    "total_issues": 5,
    "critical": 1,
    "high": 2,
    "medium": 1,
    "low": 1
  }
}
```

---

## Notes
- Backend runs on port 8000
- Frontend (Next.js) on port 3000
- Analysis takes 30-60 seconds (9 tools sequentially)
- Max 2000 lines of code
