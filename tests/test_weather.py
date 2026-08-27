from agentic_production.tools.weather import get_current_weather


def test_tokyo_weather_is_deterministic():
    result = get_current_weather("Tokyo")
    assert result["temperature_c"] == 15
    assert result["conditions"] == "rainy"
