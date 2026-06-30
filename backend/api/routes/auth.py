"""Auth routes — register + login + me."""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from backend.api.auth.deps import current_user
from backend.database.models import User
from backend.database.session import session_scope
from backend.models.schemas import LoginRequest, RegisterRequest, TokenResponse
from backend.utils.security import create_access_token, hash_password, verify_password

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(body: RegisterRequest):
    async with session_scope() as s:
        exists = await s.scalar(select(User).where(User.email == body.email))
        if exists:
            raise HTTPException(409, "email already registered")
        uid = uuid.uuid4().hex
        s.add(User(id=uid, email=body.email, password_hash=hash_password(body.password)))
    return TokenResponse(access_token=create_access_token(uid, {"email": body.email}))


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    async with session_scope() as s:
        user = await s.scalar(select(User).where(User.email == body.email))
        if not user or not verify_password(body.password, user.password_hash):
            raise HTTPException(401, "invalid credentials")
    return TokenResponse(access_token=create_access_token(user.id, {"email": user.email}))


@router.get("/me")
async def me(uid: str = Depends(current_user)):
    return {"user_id": uid}
