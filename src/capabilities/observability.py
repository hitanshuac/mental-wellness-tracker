"""
Error Observability Module for the Mental Wellness Tracker.

This module provides structured JSON error logging for an empathetic,
always-available digital companion helping students preparing for
high-stakes board exams (e.g., NEET, JEE, CUET). It logs hidden stress
triggers in system failures to enable rapid remediation.
"""
import json
import os
from datetime import datetime, timezone

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "error_logs.json")

def log_error_to_json(error_type: str, component: str, message: str) -> bool:
    """
    Appends an error log entry to data/error_logs.json.
    Returns True if successful.
    """
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error_type": error_type,
        "component": component,
        "message": message,
        "status": "UNRESOLVED"
    }
    
    logs = []
    if os.path.exists(LOG_FILE_PATH):
        try:
            with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "session_errors" in data:
                    logs = data["session_errors"]
                elif isinstance(data, list):
                    logs = data
        except json.JSONDecodeError:
            logs = []
            
    logs.append(log_entry)
    
    with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)
        
    return True
