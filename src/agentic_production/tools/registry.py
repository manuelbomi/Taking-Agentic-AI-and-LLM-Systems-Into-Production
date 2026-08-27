from dataclasses import dataclass
from typing import Callable, Any
from .weather import get_current_weather


@dataclass(frozen=True)
class ToolSpec:
    name: str
    function: Callable[..., Any]
    read_only: bool
    allowed_roles: frozenset[str]


TOOLS = {
    "get_current_weather": ToolSpec(
        name="get_current_weather",
        function=get_current_weather,
        read_only=True,
        allowed_roles=frozenset({"user", "operator", "admin"}),
    )
}


def functions_for_role(role: str) -> list[Callable[..., Any]]:
    """Return only tools the authenticated principal is allowed to expose to the model."""
    return [spec.function for spec in TOOLS.values() if role in spec.allowed_roles]
