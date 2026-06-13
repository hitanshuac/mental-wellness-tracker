"""
A11y Compliant UI Module for the Mental Wellness Tracker.
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.capabilities.sanitization import sanitize_journal_input
from src.capabilities.crisis_router import detect_crisis
from src.capabilities.llm_engine import generate_wellness_response
from src.capabilities.memoization import get_daily_mindfulness_exercise

def main() -> None:
    """Renders the A11y-compliant Streamlit frontend for the Mental Wellness Tracker."""
    st.set_page_config(page_title="Mental Wellness Tracker", layout="centered")
    
    # --- VISUAL SERENITY (CSS Injection) ---
    st.markdown("""
        <style>
        div[data-baseweb="select"] > div, div[data-baseweb="textarea"] > div, div[data-baseweb="slider"] {
            border-radius: 10px !important;
        }
        h1, h2, h3 {
            font-family: 'Helvetica Neue', sans-serif;
        }
        /* Hide the misleading "Press Ctrl+Enter to apply" text */
        div[data-testid="InputInstructions"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 1. FDA/Medical Compliance Banner
    st.warning("Medical Disclaimer: This tool is an empathetic digital companion and NOT a licensed therapist or medical professional. If you are experiencing a crisis, please seek professional medical help immediately.")
    
    st.title("Mental Wellness Tracker")
    st.write("An empathetic, always-available digital companion for students preparing for high-stakes board exams (e.g., NEET, JEE, CUET). Uncover hidden stress triggers safely.")
    
    st.subheader("Daily Mindfulness")
    st.info(get_daily_mindfulness_exercise())
    
    st.subheader("Check-In")
    
    # --- PSYCHOLOGICAL UPGRADES (With ARIA A11y compliance) ---
    col1, col2 = st.columns(2)
    with col1:
        emotion = st.selectbox(
            "Primary Emotion", 
            ["Overwhelmed", "Anxious", "Burned Out", "Panicked", "Numb", "Doubtful"],
            help="Affect Labeling: Select the emotion that best describes how you feel right now."
        )
    with col2:
        stress_level = st.slider(
            "Stress Intensity (1-10)", 
            min_value=1, max_value=10, value=6,
            help="SUDS Scale: Rate the intensity of your stress. 1 is mild, 10 is severe."
        )
    
    journal_input = st.text_area(
        "Journal Entry", 
        height=150, 
        placeholder="What is weighing on your mind today?",
        help="Type your daily journal entry here to receive CBT-based support."
    )
    
    # State Management for Throttling
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False

    def on_submit():
        st.session_state.is_generating = True

    # A11y ARIA Compliant Button
    st.button(
        "Submit Check-In", 
        help="Click to submit your emotional state and journal for analysis", 
        disabled=st.session_state.is_generating, 
        on_click=on_submit
    )
    
    # Core Logic Execution
    if st.session_state.is_generating:
        if journal_input:
            with st.spinner("Taking a deep breath... reflecting on your thoughts..."):
                sanitized_input = sanitize_journal_input(journal_input)
                
                # Crisis router checks locally before any API calls
                if detect_crisis(sanitized_input):
                    st.error("**Emergency Support:** It sounds like you might be going through a very difficult time. Please reach out to a crisis hotline or a mental health professional immediately. You are not alone.")
                else:
                    # Pass the new psychological context to the LLM Engine
                    response = generate_wellness_response(sanitized_input, emotion, stress_level, st.session_state)
                    st.success("Analysis Complete")
                    st.write("### Insights and CBT Strategies")
                    st.write(response)
        else:
            st.warning("Please enter some text in your journal.")
            
        st.session_state.is_generating = False

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        from src.capabilities.observability import log_error_to_json
        log_error_to_json(type(e).__name__, "app_main_crash", str(e))
        st.error(f"A critical system error occurred: {str(e)}")
