"""
A11y Compliant UI Module for the Mental Wellness Tracker.

This tool acts as an empathetic, always-available digital companion for students 
preparing for high-stakes board exams (e.g., NEET, JEE, CUET). By securely parsing 
journal logs, it uncovers hidden stress triggers while maintaining privacy.
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.capabilities.sanitization import sanitize_journal_input
from src.capabilities.crisis_router import detect_crisis
from src.capabilities.llm_engine import generate_wellness_response
from src.capabilities.memoization import get_daily_mindfulness_exercise

def main():
    st.set_page_config(page_title="Mental Wellness Tracker", page_icon="🧠")
    
    st.warning("Medical Disclaimer: This tool is an empathetic digital companion and NOT a licensed therapist or medical professional. If you are experiencing a crisis, please seek professional medical help immediately.")
    
    st.title("Mental Wellness Tracker")
    st.write("A safe space for students preparing for high-stakes exams.")
    
    st.subheader("Daily Mindfulness")
    st.info(get_daily_mindfulness_exercise())
    
    st.subheader("Journal Entry")
    
    journal_input = st.text_area(
        "How are you feeling today?", 
        height=150, 
        help="Type your daily journal entry here..."
    )
    
    if st.button("Submit Journal", help="Click to submit your journal entry for analysis"):
        if journal_input:
            sanitized_input = sanitize_journal_input(journal_input)
            
            if detect_crisis(sanitized_input):
                st.error("It sounds like you might be going through a very difficult time. Please know that you are not alone. Please reach out to a crisis hotline or a mental health professional immediately.")
            else:
                with st.spinner("Reflecting on your entry..."):
                    response = generate_wellness_response(sanitized_input)
                    st.success("Analysis Complete")
                    st.write("### Insights and CBT Strategies")
                    st.write(response)
        else:
            st.warning("Please enter some text in your journal.")

if __name__ == "__main__":
    main()
