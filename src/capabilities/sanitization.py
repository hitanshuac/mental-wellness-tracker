"""
Input Sanitization Module for the Mental Wellness Tracker.

This tool acts as an empathetic, always-available digital companion for students 
preparing for high-stakes board exams (e.g., NEET, JEE, CUET). By securely parsing 
journal logs, it uncovers hidden stress triggers while maintaining privacy.
"""
import re

def sanitize_journal_input(text: str) -> str:
    """
    Strips HTML, escapes < > { }, truncates to 500 chars, and regex masks phone numbers.
    """
    if not isinstance(text, str):
        return ""
        
    # Truncate to 500 chars
    sanitized = text[:500]
    
    # Strip HTML tags
    sanitized = re.sub(r'<[^>]+>', '', sanitized)
    
    # Escape malicious characters
    sanitized = sanitized.replace('<', '&lt;').replace('>', '&gt;').replace('{', '&#123;').replace('}', '&#125;')
    
    # Mask phone numbers (simple sequence of 10-15 digits with optional basic separators)
    phone_pattern = r'(?:\b|\+)(?:\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}\b'
    sanitized = re.sub(phone_pattern, '[PHONE MASKED]', sanitized)
    
    return sanitized.strip()
