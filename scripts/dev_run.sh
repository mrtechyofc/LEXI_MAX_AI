#!/usr/bin/env bash
set -euo pipefail
source backend/.venv/bin/activate
uvicorn backend.main:app --reload --port 8000
