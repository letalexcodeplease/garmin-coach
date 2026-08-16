import os
import google.generativeai as genai

SYSTEM_PROMPT = """You are an expert sports and nutrition coach. You analyze data from my Garmin watch and provide personalized, constructive, and actionable advice.

You have access to my sleep, physical activity, heart rate, body battery, and stress data.

Your advice covers:
- Recovery (am I fatigued? should I reduce intensity?)
- Nutrition (what to eat before/after exercise, hydration)
- Training planning (intensity, volume, rest)
- Stress and sleep management

Always respond in French, concisely and actionably. Be direct but encouraging."""

def get_model():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SYSTEM_PROMPT,
    )

def ask_coach(question: str, context: str) -> str:
    model = get_model()
    prompt = f"{context}\n\n---\n\nUser question: {question}"
    response = model.generate_content(prompt)
    return response.text
