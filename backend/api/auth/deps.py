"""FastAPI dependencies for auth + current user resolution."""
from __future__ import annotations
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.utils.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


async def current_user(token: str | None = Depends(oauth2_scheme)) -> str:
    if not token:
        # Allow anonymous "dev" user when no token (for local dev). Lock down in prod.
        return "anonymous"
    try:
        payload = decode_token(token)
        return str(payload["sub"])
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
