"""SQLAlchemy ORM models."""
from __future__ import annotations
from datetime import datetime
from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False)
    data = Column(JSON, default=dict)


class MemoryFact(Base):
    __tablename__ = "memory_facts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True)
    key = Column(String, index=True)
    value = Column(Text)
    score = Column(Float, default=0.5)
    created_at = Column(DateTime, default=datetime.utcnow)


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, index=True)
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class TaskRun(Base):
    __tablename__ = "task_runs"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    goal = Column(Text)
    status = Column(String, default="pending")
    steps = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
