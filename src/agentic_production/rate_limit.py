import asyncio
import time
from collections import defaultdict, deque


class InMemoryRateLimiter:
    """Small single-process limiter for tests/local development only.

    In production, enforce coarse limits at the API gateway and use a distributed
    store (for example Redis) for application-level quotas shared by replicas.
    """

    def __init__(self, requests_per_minute: int = 60):
        self.limit = requests_per_minute
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = asyncio.Lock()

    async def allow(self, key: str) -> bool:
        now = time.monotonic()
        cutoff = now - 60.0
        async with self._lock:
            q = self._events[key]
            while q and q[0] < cutoff:
                q.popleft()
            if len(q) >= self.limit:
                return False
            q.append(now)
            return True
