"""
Circuit Breaker Module for the Mental Wellness Tracker.

This module implements a pure-memory circuit breaker pattern for an
empathetic, always-available digital companion helping students
preparing for high-stakes board exams (e.g., NEET, JEE, CUET). It
prevents endless API retry loops and uncovers hidden stress triggers
in system degradation.
"""


def is_circuit_tripped(session_state_dict: dict) -> bool:
    """
    Checks if the circuit breaker has tripped due to 3 or more consecutive failures.
    """
    failures = session_state_dict.get("api_consecutive_failures", 0)
    return failures >= 3

def record_api_failure(session_state_dict: dict) -> int:
    """
    Increments the consecutive API failure count.
    Returns the new failure count.
    """
    failures = session_state_dict.get("api_consecutive_failures", 0)
    failures += 1
    session_state_dict["api_consecutive_failures"] = failures
    return failures

def reset_api_failure(session_state_dict: dict) -> None:
    """
    Resets the consecutive API failure count on a successful request.
    """
    session_state_dict["api_consecutive_failures"] = 0
