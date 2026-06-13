"""
System Prompt Grounding Module for the Mental Wellness Tracker.
"""
import streamlit as st
from google import genai
from google.genai import types
import re
from src.capabilities.observability import log_error_to_json
from src.capabilities.circuit_breaker import is_circuit_tripped, record_api_failure, reset_api_failure

FALLBACK_MESSAGE: str = (
    "I hear you, and it is completely normal to feel overwhelmed right now, "
    "especially with exams like JEE/NEET looming. Let's ground ourselves using "
    "CBT: Take a deep breath. What is one small, actionable step you can control "
    "today? Remember, your worth is not defined by a single test score."
)

SYSTEM_PROMPT_BASE: str = (
    "You are an empathetic digital companion helping students prepare for high-stakes exams "
    "like NEET, JEE, CUET, CAT, GATE, and UPSC. You are NOT a licensed therapist. Do not diagnose. "
    "Frame actionable advice using Cognitive Behavioral Therapy (CBT) to uncover hidden stress triggers. "
    "CRITICAL: Do not use any emojis. Do not use any XML or HTML tags. Respond in plain text and standard markdown only."
)

@st.cache_data(ttl=3600, show_spinner=False)
def _cached_llm_call(journal_entry: str, emotion: str, stress_level: int) -> str:
    """Memoized LLM generation that adapts to the SUDS scale and Affect Labeling."""
    import os
    try:
        # Hugging Face Docker Spaces inject secrets as environment variables.
        # Local Streamlit uses secrets.toml.
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            try:
                api_key = st.secrets["GEMINI_API_KEY"]
            except Exception:
                pass
                
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing from environment variables and secrets.")
            
        client = genai.Client(api_key=api_key)

        # Dynamically inject the psychological context into the system prompt
        dynamic_instruction = (
            f"{SYSTEM_PROMPT_BASE}\n\n"
            f"The student has identified their primary emotion as '{emotion}' "
            f"and rated their stress intensity at a {stress_level}/10. "
            f"Tailor your CBT grounding techniques specifically to this emotional state and severity."
        )

        config = types.GenerateContentConfig(
            system_instruction=dynamic_instruction,
            temperature=0.7,
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_MEDIUM_AND_ABOVE"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
            ]
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=journal_entry,
            config=config
        )

        result_text = response.text.strip() if response.text else ""
        
        # Scrub any experimental thought blocks
        result_text = re.sub(r'<think>.*?(?:</think>|$)', '', result_text, flags=re.DOTALL | re.IGNORECASE)
        result_text = result_text.strip()

        if not result_text:
            raise ValueError("Empty response from Gemini 2.5 API.")

        return result_text
    except Exception as e:
        raise e

def generate_wellness_response(journal_entry: str, emotion: str, stress_level: int, session_state: dict = None) -> str:
    """Wrapper that handles circuit breaking around the cached API call."""
    if session_state is None:
        session_state = {}

    if is_circuit_tripped(session_state):
        return FALLBACK_MESSAGE

    try:
        result = _cached_llm_call(journal_entry, emotion, stress_level)
        reset_api_failure(session_state)
        return result
    except Exception as e:
        record_api_failure(session_state)
        log_error_to_json(type(e).__name__, "llm_engine_crash", str(e))
        return FALLBACK_MESSAGE
