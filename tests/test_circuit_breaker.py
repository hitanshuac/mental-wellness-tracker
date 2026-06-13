from src.capabilities.circuit_breaker import is_circuit_tripped, record_api_failure, reset_api_failure

def test_circuit_breaker_logic():
    session_state = {}
    
    assert is_circuit_tripped(session_state) is False
    
    record_api_failure(session_state)
    assert is_circuit_tripped(session_state) is False
    
    record_api_failure(session_state)
    assert is_circuit_tripped(session_state) is False
    
    record_api_failure(session_state)
    assert is_circuit_tripped(session_state) is True
    assert session_state["api_consecutive_failures"] == 3
    
    reset_api_failure(session_state)
    assert is_circuit_tripped(session_state) is False
    assert session_state["api_consecutive_failures"] == 0
