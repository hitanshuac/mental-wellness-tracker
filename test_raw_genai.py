import os
from google import genai
from google.genai import types

try:
    import toml
    secrets = toml.load(".streamlit/secrets.toml")
    api_key = secrets["GEMINI_API_KEY"]
except Exception as e:
    api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = (
    "You are an empathetic digital companion helping students prepare for high-stakes exams "
    "like NEET, JEE, CUET, CAT, GATE, and UPSC. You are NOT a licensed therapist. Do not diagnose. "
    "Frame actionable advice using Cognitive Behavioral Therapy (CBT) to uncover hidden stress triggers. "
    "Provide a complete, structured, multi-paragraph response. Never end mid-sentence."
)

safety_settings = [
    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
]

journal_entry = "I am so stressed about my NEET exams, I feel like giving up."

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=journal_entry,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        safety_settings=safety_settings,
        temperature=0.7,
    ),
)

print("FINISH REASON:", response.candidates[0].finish_reason)
print("RAW TEXT:", repr(response.text))
