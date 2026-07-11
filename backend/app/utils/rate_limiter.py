import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Custom zero-dependency token-bucket rate limiter middleware."""
    
    def __init__(self, app, rate: float = 2.0, capacity: float = 10.0):
        super().__init__(app)
        self.rate = rate  # Tokens refilled per second
        self.capacity = capacity  # Maximum burst capacity
        self.buckets = {}  # IP -> {"tokens": float, "last_update": float}

    def _get_bucket(self, ip: str) -> dict:
        now = time.time()
        if ip not in self.buckets:
            self.buckets[ip] = {"tokens": self.capacity, "last_update": now}
            return self.buckets[ip]
            
        bucket = self.buckets[ip]
        elapsed = now - bucket["last_update"]
        # Add elapsed tokens
        bucket["tokens"] = min(self.capacity, bucket["tokens"] + elapsed * self.rate)
        bucket["last_update"] = now
        return bucket

    async def dispatch(self, request: Request, call_next):
        # Allow health checks and docs without rate limiting
        if request.url.path in ["/health", "/docs", "/openapi.json"]:
            return await call_next(request)
            
        client_ip = request.client.host if request.client else "127.0.0.1"
        bucket = self._get_bucket(client_ip)
        
        if bucket["tokens"] < 1.0:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too Many Requests. Rate limit exceeded."}
            )
            
        bucket["tokens"] -= 1.0
        return await call_next(request)
