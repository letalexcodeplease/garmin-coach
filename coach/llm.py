import os
from google import genai
from google.genai import types

SYSTEM_PROMPT = """You are an expert sports and nutrition coach. You analyze data from my Garmin watch and provide personalized, constructive, and actionable advice.

You have access to my sleep, physical activity, heart rate, body battery, and stress data.

Your advice covers:
- Recovery (am I fatigued? should I reduce intensity?)
- Nutrition (what to eat before/after exercise, hydration)
- Training planning (intensity, volume, rest)
- Stress and sleep management

Always respond in French, concisely and actionably. Be direct but encouraging."""

def ask_coach(question: str, context: str) -> str:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = f"{context}\n\n---\n\nUser question: {question}"
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return response.text
