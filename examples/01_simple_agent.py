"""The prototype: useful, but not yet a production service."""
from google import genai
from google.genai import types
from agentic_production.tools.weather import get_current_weather

client = genai.Client()
config = types.GenerateContentConfig(tools=[get_current_weather], temperature=0.0)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the weather like in Tokyo right now? Should I bring an umbrella?",
    config=config,
)
print(response.text)
