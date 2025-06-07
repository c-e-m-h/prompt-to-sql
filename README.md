# Prompt to SQL Demo

A tiny web app that lets users type natural-language questions (e.g., "Show me total paying customers by region for Q1 2025") and get instant analytics from a demo e-commerce database. Powered by OpenAI and FastAPI.

## Tech Stack
- **Backend:** FastAPI (Python), SQLAlchemy, OpenAI API
- **Database:** PostgreSQL
- **Frontend:** Next.js (React 18)

## High-Level Workflow
```
Prompt (user)
   │
   ▼
LLM Agent (OpenAI)
   │
   ▼
FastAPI /query endpoint
   │
   ▼
PostgreSQL (demo DB)
   │
   ▼
Next.js UI (table + chart)
```

## Getting Started
1. Clone the repo.
2. (Coming soon) Copy `.env.example` to `.env` and fill in your secrets.
3. Run with Docker Compose: `docker-compose up --build`
4. Visit the frontend at `http://localhost:3000`.
5. (Optional) Test the backend at `http://localhost:8000/docs`.

## Folders
- `backend/` — FastAPI app, agent, DB, auth, tests
- `frontend/` — Next.js app, UI components
- `data/` — SQL seed and (optional) CSVs

## Expanding the Project:

- [ ] Improving the prompt-to-SQL agent (e.g., add schema introspection, error handling)
- [ ] Adding authentication (JWT, etc.)
- [ ] Adding charting/visualization (if you want to use Recharts or similar)
- [ ] Adding more sample data or analytics features

---
*For demo use only. Not production-ready.* 