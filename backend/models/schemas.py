"""Pydantic schemas for the API surface."""
from __future__ import annotations
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    attachments: list[dict[str, Any]] = []


class ChatResponse(BaseModel):
    text: str
    session_id: str
    used_tools: list[str] = []
    used_agents: list[str] = []
    memory_hits: list[dict[str, Any]] = []


class MemoryWrite(BaseModel):
    text: str
    metadata: dict[str, Any] = {}


class MemoryQuery(BaseModel):
    query: str
    k: int = 8


class TaskCreate(BaseModel):
    goal: str


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(LoginRequest):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SystemStatus(BaseModel):
    service: str = "lexi"
    version: str
    env: str
    agents: list[str]
    tools: list[str]
    uptime_seconds: float
