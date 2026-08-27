"""Use the SDK's native async client inside asynchronous services."""
import asyncio
from google import genai
from google.genai import types
from agentic_production.tools.weather import get_current_weather


async def main():
    client = genai.Client()
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents="What is the weather in Winston-Salem?",
        config=types.GenerateContentConfig(tools=[get_current_weather], temperature=0.0),
    )
    print(response.text)
    await client.aio.aclose()
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
