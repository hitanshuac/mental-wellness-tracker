"""
Memoization Module for the Mental Wellness Tracker.

This tool acts as an empathetic, always-available digital companion for students 
preparing for high-stakes board exams (e.g., NEET, JEE, CUET). By securely parsing 
journal logs, it uncovers hidden stress triggers while maintaining privacy.
"""
import streamlit as st
import random

@st.cache_data(ttl=86400)
def get_daily_mindfulness_exercise() -> str:
    """
    Returns a daily mindfulness exercise, memoized for 24 hours to ensure high efficiency.
    """
    exercises = [
        "Box Breathing: Inhale for 4 seconds, hold for 4, exhale for 4, hold for 4. Repeat 4 times.",
        "5-4-3-2-1 Grounding: Acknowledge 5 things you see, 4 you can touch, 3 you hear, 2 you smell, and 1 you can taste.",
        "Mindful Observation: Focus entirely on a single object in the room for one minute."
    ]
    return random.choice(exercises)
