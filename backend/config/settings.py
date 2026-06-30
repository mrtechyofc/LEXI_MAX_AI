"""Typed application configuration loaded from environment / .env."""
from __future__ import annotations

from functools import lru_cache
from typing import List, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General
    ENV: Literal["development", "staging", "production"] = Field("development", alias="LEXI_ENV")
    LOG_LEVEL: str = Field("INFO", alias="LEXI_LOG_LEVEL")
    SECRET_KEY: str = Field("change-me", alias="LEXI_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", alias="LEXI_JWT_ALGORITHM")
    JWT_EXPIRE_MINUTES: int = Field(60 * 24, alias="LEXI_JWT_EXPIRE_MINUTES")
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # LLM
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_LLM_PROVIDER: Literal["openai", "anthropic", "gemini", "ollama"] = "openai"
    DEFAULT_LLM_MODEL: str = "gpt-4o-mini"

    # DB
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/lexi.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Vector store
    VECTOR_BACKEND: Literal["chromadb", "faiss"] = "chromadb"
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    FAISS_PERSIST_DIR: str = "./data/faiss"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Voice
    STT_BACKEND: Literal["whisper", "openai-whisper-api"] = "whisper"
    WHISPER_MODEL: str = "base"
    TTS_BACKEND: Literal["coqui", "elevenlabs", "openai"] = "coqui"
    ELEVENLABS_API_KEY: str | None = None
    WAKE_WORD: str = "hey lexi"

    # Vision
    VISION_PROVIDER: str = "openai"

    # Observability
    PROMETHEUS_ENABLED: bool = True
    OTEL_EXPORTER_OTLP_ENDPOINT: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
