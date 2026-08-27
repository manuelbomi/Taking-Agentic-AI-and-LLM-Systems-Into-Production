from pydantic import BaseModel, Field


class WeatherResult(BaseModel):
    location: str
    temperature_c: float
    conditions: str
    source: str = "deterministic-demo-provider"


def get_current_weather(location: str) -> dict:
    """Get current weather for a location.

    This deterministic implementation keeps the repository runnable without a
    third-party weather account. Replace it with a real provider adapter in a
    real deployment; preserve the typed contract, timeout and error policy.
    """
    normalized = location.strip().lower()
    if not normalized:
        raise ValueError("location must not be empty")

    if "tokyo" in normalized:
        result = WeatherResult(location=location, temperature_c=15, conditions="rainy")
    elif "winston-salem" in normalized:
        result = WeatherResult(location=location, temperature_c=28, conditions="sunny")
    else:
        result = WeatherResult(location=location, temperature_c=22, conditions="partly cloudy")

    return result.model_dump()
