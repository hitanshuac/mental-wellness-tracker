"""
System Prompt Grounding Module for the Mental Wellness Tracker.

This tool acts as an empathetic, always-available digital companion for students 
preparing for high-stakes board exams (e.g., NEET, JEE, CUET). By securely parsing 
journal logs, it uncovers hidden stress triggers while maintaining privacy.
"""
import streamlit as st
import google.generativeai as genai
import google.api_core.exceptions

def generate_wellness_response(journal_entry: str) -> str:
    """
    Context manager for the LLM to generate a CBT-framed wellness response.
    """
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
    
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_prompt,
        )
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_LOW_AND_ABOVE",
            }
        ]
        
        response = model.generate_content(
            journal_entry,
            safety_settings=safety_settings,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=250
            )
        )
        return response.text.strip()
    except google.api_core.exceptions.InvalidArgument as e:
        return f"Configuration Error: The API key may be invalid or the request was malformed. Details: {str(e)}"
    except google.api_core.exceptions.ResourceExhausted:
        return "The system is currently experiencing high traffic (Rate Limit). Please take a deep breath and try again in a few minutes."
    except google.api_core.exceptions.PermissionDenied:
        return "Access Denied: Please check if your API key has the correct permissions."
    except Exception as e:
        # Fallback for other unexpected errors
        return f"I'm here for you, but an unexpected error occurred: {str(e)}"
