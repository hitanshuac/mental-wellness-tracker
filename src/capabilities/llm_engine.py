"""
System Prompt Grounding Module for the Mental Wellness Tracker.

This tool acts as an empathetic, always-available digital companion for students 
preparing for high-stakes board exams (e.g., NEET, JEE, CUET). By securely parsing 
journal logs, it uncovers hidden stress triggers while maintaining privacy.
"""
import os
from openai import OpenAI

def generate_wellness_response(journal_entry: str) -> str:
    """
    Context manager for the LLM to generate a CBT-framed wellness response.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "dummy-key"))
    
    system_prompt = (
        "You are an empathetic digital companion helping students prepare for high-stakes exams "
        "like NEET, JEE, CUET, CAT, GATE, and UPSC. You are NOT a licensed therapist. Do not diagnose. "
        "Frame actionable advice using Cognitive Behavioral Therapy (CBT) to uncover hidden stress triggers."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": journal_entry}
            ],
            temperature=0.7,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "I'm here for you, but I'm having trouble connecting right now. Please take a deep breath and try again."
