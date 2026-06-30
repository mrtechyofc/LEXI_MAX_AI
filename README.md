# LEXI — The Ultimate AI Assistant

```
██╗     ███████╗██╗  ██╗██╗
██║     ██╔════╝╚██╗██╔╝██║
██║     █████╗   ╚███╔╝ ██║
██║     ██╔══╝   ██╔██╗ ██║
███████╗███████╗██╔╝ ██╗██║
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝
```

LEXI is a **modular, production-grade AI Operating System** inspired by JARVIS.
It combines a central reasoning brain, multi-agent orchestration, long-term memory,
voice + vision, tool execution, and an observable runtime — all behind a clean
FastAPI + Next.js stack.

## High-level architecture

```
┌────────────────────────────────────────────────────────────────┐
│                          FRONTEND                              │
│  Next.js • TailwindCSS • Framer Motion • WebSocket client      │
└────────────────────────────────────────────────────────────────┘
                              │  REST / WS
┌────────────────────────────────────────────────────────────────┐
│                           BACKEND                              │
│                                                                │
│  ┌──────────────┐   ┌────────────────┐   ┌─────────────────┐   │
│  │  Core Brain  │──▶│  Agent Router  │──▶│ Specialized     │   │
│  │  + Router    │   │  (LangGraph)   │   │ Agents (10x)    │   │
│  └──────────────┘   └────────────────┘   └─────────────────┘   │
│         │                   │                     │            │
│         ▼                   ▼                     ▼            │
│  ┌──────────────┐   ┌────────────────┐   ┌─────────────────┐   │
│  │ Memory layer │   │ Tool registry  │   │ Voice / Vision  │   │
│  │ (FAISS+SQL)  │   │ (sandboxed)    │   │ pipelines       │   │
│  └──────────────┘   └────────────────┘   └─────────────────┘   │
│         │                   │                     │            │
│         └─────────┬─────────┴─────────┬───────────┘            │
│                   ▼                   ▼                        │
│            PostgreSQL / Redis    Celery workers                │
└────────────────────────────────────────────────────────────────┘
```

## Quickstart

```bash
# 1. Configure
cp .env.example .env  # fill in API keys

# 2. Bring up the stack (postgres, redis, backend, worker, frontend)
docker compose up --build

# 3. Open
# Frontend:   http://localhost:3000
# API docs:   http://localhost:8000/docs
# Grafana:    http://localhost:3001
```

## Local dev (no docker)

```bash
bash setup.sh                 # creates venv + installs deps
source backend/.venv/bin/activate
uvicorn backend.main:app --reload --port 8000
cd frontend && npm install && npm run dev
```

## Modules

| Module          | Path                | Purpose                           |
|-----------------|---------------------|-----------------------------------|
| Core Brain      | `backend/core/`     | Reasoning, routing, personality   |
| Agents          | `backend/agents/`   | Specialized LangGraph agents      |
| Memory          | `backend/memory/`   | Short/long-term + vector store    |
| Tools           | `backend/tools/`    | Sandboxed external capabilities   |
| Voice           | `backend/voice/`    | STT, TTS, wake-word, streaming    |
| Vision          | `backend/vision/`   | OCR, screen parsing, multimodal   |
| Task Engine     | `backend/tasks/`    | Planning, scheduling, execution   |
| API             | `backend/api/`      | REST + WebSocket surface          |
| Frontend        | `frontend/`         | Next.js console + dashboard       |

See `docs/` for deep dives on each subsystem, and `kubernetes/` for k8s manifests.

## License
MIT
