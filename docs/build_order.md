# Step-by-Step Build Order

1. `setup.sh` — venv + dependencies
2. Copy `.env.example` to `.env`, fill in `OPENAI_API_KEY`
3. Run `uvicorn backend.main:app --reload`
4. Verify `GET /health` returns 200
5. Hit `POST /api/chat` with `{"message": "Hello LEXI"}`
6. Open `/docs` → try a tool invocation
7. `cd frontend && npm install && npm run dev`
8. Open http://localhost:3000 — chat, memory, tools, voice pages
9. `docker compose up --build` to bring up the full stack
10. (k8s) apply the manifests in `kubernetes/`
