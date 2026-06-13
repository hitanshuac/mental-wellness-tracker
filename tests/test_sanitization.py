import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.capabilities.sanitization import sanitize_journal_input

def test_sanitize_journal_input_empty():
    assert sanitize_journal_input("") == ""
    assert sanitize_journal_input(None) == ""

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
    
def test_sanitize_journal_input_masks_international_phone():
    input_text = "Call me at +1 (555) 123-4567 anytime."
    output = sanitize_journal_input(input_text)
    assert "Call me at [PHONE MASKED] anytime." in output
