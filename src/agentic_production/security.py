from dataclasses import dataclass
from fastapi import Header, HTTPException, status
from .config import get_settings


@dataclass(frozen=True)
class Principal:
    subject: str
    role: str
    tenant_id: str


async def authenticate(authorization: str | None = Header(default=None)) -> Principal:
    """Demo authentication adapter.

    Production: validate a JWT/OIDC access token against your identity provider,
    check issuer/audience/expiry/signature, and derive roles/tenant from trusted claims.
    """
    settings = get_settings()
    if settings.auth_mode == "dev":
        expected = f"Bearer {settings.dev_bearer_token}"
        if authorization != expected:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return Principal(subject="local-user", role="user", tenant_id="local")

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Configure an enterprise OIDC/JWT validator for non-dev environments",
    )
