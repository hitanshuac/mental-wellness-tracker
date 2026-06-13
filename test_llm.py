import sys
import os
import json
import streamlit as st

# Setup mock st.secrets
try:
    import toml
    secrets = toml.load(".streamlit/secrets.toml")
    st.secrets = secrets
except Exception as e:
    print("Could not load secrets:", e)

from src.capabilities.llm_engine import generate_wellness_response

print("Calling API...")
response = generate_wellness_response("I am so stressed about my NEET exams, I feel like giving up.")
print("RAW RESPONSE:")
print(repr(response))
