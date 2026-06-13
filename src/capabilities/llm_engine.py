"""
System Prompt Grounding Module for the Mental Wellness Tracker.

This tool acts as an empathetic, always-available digital companion for students 
preparing for high-stakes board exams (e.g., NEET, JEE, CUET). By securely parsing 
journal logs, it uncovers hidden stress triggers while maintaining privacy.
"""
import streamlit as st
import google.generativeai as genai
import google.api_core.exceptions
from src.capabilities.observability import log_error_to_json
from src.capabilities.circuit_breaker import is_circuit_tripped, record_api_failure, reset_api_failure

def generate_wellness_response(journal_entry: str, session_state: dict = None) -> str:
    """
    Context manager for the LLM to generate a CBT-framed wellness response.
    """
    if session_state is None:
        session_state = {}
        
    if is_circuit_tripped(session_state):
        log_error_to_json("CircuitBreaker", "llm_engine", "Circuit breaker tripped due to 3 consecutive failures.")
        return "Our servers are currently overwhelmed. The emergency circuit breaker has been tripped to protect the system. Please try again later."
        
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception:
        # Fallback if secrets are not configured
        pass
        
    system_prompt = (
        "You are an empathetic digital companion helping students prepare for high-stakes exams "
        "like NEET, JEE, CUET, CAT, GATE, and UPSC. You are NOT a licensed therapist. Do not diagnose. "
        "Frame actionable advice using Cognitive Behavioral Therapy (CBT) to uncover hidden stress triggers."
    )
    
    fallback_message = "I hear you, and it is completely normal to feel overwhelmed right now, especially with exams like JEE/NEET looming. Let's ground ourselves using CBT: Take a deep breath. What is one small, actionable step you can control today? Remember, your worth is not defined by a single test score."
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_prompt,
        )
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]
        
        response = model.generate_content(
            journal_entry,
            safety_settings=safety_settings,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=800
            )
        )
        
        # Validate response is not blocked or incomplete
        if not response.candidates:
            log_error_to_json("SafetyBlocked", "llm_engine", "Response had no candidates (fully blocked by safety filter).")
            return fallback_message
        
        candidate = response.candidates[0]
        finish_reason = getattr(candidate, "finish_reason", None)
        
        # finish_reason 1 = STOP (normal), 3 = SAFETY (blocked mid-gen)
        if finish_reason is not None and finish_reason != 1:
            log_error_to_json("SafetyTruncated", "llm_engine", f"Response truncated. finish_reason={finish_reason}")
            return fallback_message
        
        result_text = response.text.strip()
        if not result_text or len(result_text) < 30:
            log_error_to_json("ShortResponse", "llm_engine", f"Response too short ({len(result_text)} chars): {result_text}")
            return fallback_message
        
        reset_api_failure(session_state)
        return result_text
    except google.api_core.exceptions.InvalidArgument as e:
        record_api_failure(session_state)
        log_error_to_json("InvalidArgument", "llm_engine", str(e))
        return fallback_message
    except google.api_core.exceptions.ResourceExhausted as e:
        record_api_failure(session_state)
        log_error_to_json("ResourceExhausted", "llm_engine", str(e))
        return fallback_message
    except google.api_core.exceptions.PermissionDenied as e:
        record_api_failure(session_state)
        log_error_to_json("PermissionDenied", "llm_engine", str(e))
        return fallback_message
    except Exception as e:
        record_api_failure(session_state)
        log_error_to_json(type(e).__name__, "llm_engine", str(e))
        return fallback_message
