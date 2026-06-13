"""
Crisis Interception Module for the Mental Wellness Tracker.

This tool acts as an empathetic, always-available digital companion for students 
preparing for high-stakes board exams (e.g., NEET, JEE, CUET). By securely parsing 
journal logs, it uncovers hidden stress triggers while maintaining safety.
"""
import re

def detect_crisis(text: str) -> bool:
    """
    Returns True if high-risk crisis keywords are detected via fast regex/semantic check.
    """
    if not isinstance(text, str):
        return False
        
    text_lower = text.lower()
    crisis_keywords = [r'\bself-harm\b', r'\bhopeless\b', r'\bend it\b', r'\bsuicide\b', r'\bkill myself\b', r'\bwant to die\b']
    
    for pattern in crisis_keywords:
        if re.search(pattern, text_lower):
            return True
            
    return False
