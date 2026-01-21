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
- Fixed import issues and Pydantic state mutations

### Done - Frontend ✅
- Step 1: Main Page (app/page.tsx) complete

### Working On
- Step 2: CodeInput Component (Monaco Editor)

---

## Frontend Plan (Simple)

### Step 1: Main Page (app/page.tsx) ✅
- [x] Replace default Next.js page
- [x] Add state management (code, language, loading, results, error)
- [x] Create handleAnalyze function (POST to API)
- [x] Build basic layout (2 column grid)
- [x] Add error handling and validation
- [x] Test end-to-end with backend
- [x] Fix text colors and styling

### Step 2: CodeInput Component (components/CodeInput.tsx)
- [x] Import Monaco Editor (dynamic, no SSR)
- [x] Props: value, onChange, language
- [x] Set height ~400px
- [x] Enable line numbers + syntax highlighting
- [x] Replace textarea in page.tsx

### Step 3: LanguageSelector (components/LanguageSelector.tsx)
- [x] Simple dropdown
- [x] Props: value, onChange
- [x] Options: python, javascript, typescript, java, go, etc.
- [x] Replace language text in page.tsx

### Step 4: ResultsDisplay (components/ResultsDisplays.tsx)
- [x] Show metrics cards (total, critical, high, medium, low)
- [x] Show summary section
- [] Show issues list (grouped by severity or type)
- [ ] Add loading state
- [ ] Add empty state
- [ ] Replace JSON display in page.tsx

### Step 5: Polish
- [ ] Improve error messages
- [ ] Add responsive design tweaks
- [ ] Add loading progress indicator
- [ ] Final styling polish
- [ ] Full end-to-end testing

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
