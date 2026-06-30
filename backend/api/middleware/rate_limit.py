"""Simple in-memory rate limiter — token bucket per IP."""
from __future__ import annotations
import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, capacity: int = 60, refill_per_sec: float = 1.0) -> None:
        super().__init__(app)
        self.capacity = capacity
        self.refill = refill_per_sec
        self.buckets: dict[str, tuple[float, float]] = defaultdict(lambda: (capacity, time.time()))

    async def dispatch(self, request, call_next):
        ip = request.client.host if request.client else "unknown"
        tokens, last = self.buckets[ip]
        now = time.time()
        tokens = min(self.capacity, tokens + (now - last) * self.refill)
        if tokens < 1:
            return JSONResponse({"error": "rate limited"}, status_code=429)
        self.buckets[ip] = (tokens - 1, now)
        return await call_next(request)
