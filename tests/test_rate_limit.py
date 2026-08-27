import pytest
from agentic_production.rate_limit import InMemoryRateLimiter


@pytest.mark.asyncio
async def test_rate_limit():
    limiter = InMemoryRateLimiter(requests_per_minute=2)
    assert await limiter.allow("u") is True
    assert await limiter.allow("u") is True
    assert await limiter.allow("u") is False
