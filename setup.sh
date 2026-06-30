#!/usr/bin/env bash
# ============================================================
# LEXI - Local development bootstrap script
# ============================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "▶ Creating Python virtual environment..."
python3 -m venv backend/.venv
# shellcheck disable=SC1091
source backend/.venv/bin/activate

echo "▶ Upgrading pip..."
pip install --upgrade pip wheel setuptools

echo "▶ Installing Python dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "▶ Creating .env from template..."
    cp .env.example .env
    echo "  Edit .env and add your API keys."
fi

echo "▶ Initializing local data directories..."
mkdir -p data/chroma data/faiss data/logs data/uploads

if [ -d "frontend" ]; then
    echo "▶ Installing frontend deps..."
    (cd frontend && npm install --silent || echo "Skipping frontend install (npm not available)")
fi

echo "✔ Setup complete. Activate with: source backend/.venv/bin/activate"
