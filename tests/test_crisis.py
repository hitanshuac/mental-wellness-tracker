import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.capabilities.crisis_router import detect_crisis

def test_detect_crisis_empty_input():
    assert detect_crisis("") is False
    assert detect_crisis(None) is False

def test_detect_crisis_true_cases():
    assert detect_crisis("I am hopeless and want to self-harm.") is True
    assert detect_crisis("I want to end it.") is True
    assert detect_crisis("Thoughts of suicide are overwhelming.") is True
    assert detect_crisis("I think I am going to kill myself.") is True

def test_detect_crisis_false_cases():
    assert detect_crisis("I am just really stressed about my exams tomorrow.") is False
    assert detect_crisis("I need to study more, I feel unprepared.") is False
    assert detect_crisis("end iteration") is False # Partial match test

def test_detect_crisis_case_insensitive():
    assert detect_crisis("I feel HOPELESS today.") is True
    assert detect_crisis("Self-Harm is on my mind.") is True
