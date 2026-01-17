# AI Code Review Agent - Plan

**Last Updated:** 2026-01-13

---

## Current Status

**Phase:** Building backend tools and LangGraph pipeline

### Done
- FastAPI skeleton with /api/analyze endpoint
- AgentState model (state.py)
- Security tool (partial - needs Claude API switch)

### Working On
- 

### Next
- Build graph.py (LangGraph StateGraph with 10 nodes)
- Build nodes.py (node functions)
- Connect main.py to graph
- Frontend (React + Monaco Editor)

---

## 9 Tools Checklist

1. [ ] Security already fixed
2. [ ] Style already fixed
3. [ ] Complexity fixed
4. [ ] Best Practices fixed
5. [ ] Test Coverage fixed
6. [ ] Performance fixed
7. [ ] Accessibility fixed
8. [ ] Dependency fixed
9. [ ] Documentation fixed

---

## Known Issues

3. graph.py and nodes.py are empty

---

## Notes
- 2000 line limit
- Auto-detect language if not provided
