import sys
import os

# Add src to path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.capabilities.sanitization import sanitize_journal_input
from src.capabilities.crisis_router import detect_crisis

def test_sanitize_journal_input_strips_html():
    input_text = "<p>I am feeling stressed</p> <script>alert(1)</script>"
    output = sanitize_journal_input(input_text)
    assert "I am feeling stressed alert(1)" in output
    assert "<p>" not in output

def test_sanitize_journal_input_escapes_chars():
    input_text = "What is {this} > that < here?"
    output = sanitize_journal_input(input_text)
    assert "&#123;this&#125;" in output
    assert "&gt; that &lt;" in output

def test_sanitize_journal_input_truncates():
    input_text = "A" * 600
    output = sanitize_journal_input(input_text)
    assert len(output) == 500

def test_sanitize_journal_input_masks_phone():
    input_text = "My phone is 123-456-7890."
    output = sanitize_journal_input(input_text)
    assert "My phone is [PHONE MASKED]." in output

def test_detect_crisis_true():
    input_text = "I am hopeless and want to self-harm."
    assert detect_crisis(input_text) is True

def test_detect_crisis_false():
    input_text = "I am just really stressed about my exams tomorrow."
    assert detect_crisis(input_text) is False

def test_detect_crisis_case_insensitive():
    input_text = "I feel HOPELESS today."
    assert detect_crisis(input_text) is True
