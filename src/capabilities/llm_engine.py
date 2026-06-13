"""
System Prompt Grounding Module for the Mental Wellness Tracker.

This tool acts as an empathetic, always-available digital companion for students
preparing for high-stakes board exams (e.g., NEET, JEE, CUET). By securely parsing
journal logs, it uncovers hidden stress triggers while maintaining privacy.
"""
import streamlit as st
from google import genai
from google.genai import types
from src.capabilities.observability import log_error_to_json
from src.capabilities.circuit_breaker import is_circuit_tripped, record_api_failure, reset_api_failure

FALLBACK_MESSAGE: str = (
    "I hear you, and it is completely normal to feel overwhelmed right now, "
    "especially with exams like JEE/NEET looming. Let's ground ourselves using "
    "CBT: Take a deep breath. What is one small, actionable step you can control "
    "today? Remember, your worth is not defined by a single test score."
)

SYSTEM_PROMPT: str = (
    "You are an empathetic digital companion helping students prepare for high-stakes exams "
    "like NEET, JEE, CUET, CAT, GATE, and UPSC. You are NOT a licensed therapist. Do not diagnose. "
    "Frame actionable advice using Cognitive Behavioral Therapy (CBT) to uncover hidden stress triggers. "
    "Provide a complete, structured, multi-paragraph response. Never end mid-sentence."
)


def generate_wellness_response(journal_entry: str, session_state: dict = None) -> str:
    """Generates a CBT-framed wellness response using Google Gemini.

    Args:
        journal_entry: The sanitized journal text from the student.
        session_state: Streamlit session state dict for circuit breaker tracking.

    Returns:
        A complete CBT-framed response string, or the fallback message on any error.
    """
    if session_state is None:
        session_state = {}

    if is_circuit_tripped(session_state):
        log_error_to_json("CircuitBreaker", "llm_engine", "Circuit breaker tripped due to 3 consecutive failures.")
        return FALLBACK_MESSAGE

    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        log_error_to_json("MissingSecret", "llm_engine", "GEMINI_API_KEY not found in st.secrets.")
        return FALLBACK_MESSAGE

    try:
        client = genai.Client(api_key=api_key)

        safety_settings = [
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_MEDIUM_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_MEDIUM_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_MEDIUM_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_MEDIUM_AND_ABOVE",
            ),
        ]

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=journal_entry,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                safety_settings=safety_settings,
                temperature=0.7,
                max_output_tokens=1024,
            ),
        )

        # Validate response integrity
        if not response.candidates:
            log_error_to_json("SafetyBlocked", "llm_engine", "No candidates returned (fully blocked).")
            return FALLBACK_MESSAGE

        candidate = response.candidates[0]
        finish_reason = candidate.finish_reason

        # STOP = normal completion; anything else = truncated/blocked
        if finish_reason is not None and str(finish_reason) != "STOP" and finish_reason != 1:
            log_error_to_json("SafetyTruncated", "llm_engine", f"finish_reason={finish_reason}")
            return FALLBACK_MESSAGE

        result_text = response.text.strip() if response.text else ""
        if not result_text or len(result_text) < 50:
            log_error_to_json("ShortResponse", "llm_engine", f"Too short ({len(result_text)} chars): {result_text}")
            return FALLBACK_MESSAGE

        reset_api_failure(session_state)
        return result_text

    except Exception as e:
        record_api_failure(session_state)
        log_error_to_json(type(e).__name__, "llm_engine", str(e))
        return FALLBACK_MESSAGE
