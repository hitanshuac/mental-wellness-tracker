import json
import os
from src.capabilities.observability import log_error_to_json

def test_log_error_to_json(tmpdir, monkeypatch):
    test_log_path = os.path.join(str(tmpdir), "test_error_logs.json")
    monkeypatch.setattr("src.capabilities.observability.LOG_FILE_PATH", test_log_path)
    
    result = log_error_to_json("TestError", "test_component", "Test message")
    assert result is True
    assert os.path.exists(test_log_path)
    
    with open(test_log_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["error_type"] == "TestError"
        assert data[0]["component"] == "test_component"
        assert data[0]["message"] == "Test message"
        assert data[0]["status"] == "UNRESOLVED"
        
    # Test append
    log_error_to_json("SecondError", "test_component", "Second message")
    with open(test_log_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 2

def test_log_error_to_json_corrupted_file(tmpdir, monkeypatch):
    test_log_path = os.path.join(str(tmpdir), "test_error_logs.json")
    monkeypatch.setattr("src.capabilities.observability.LOG_FILE_PATH", test_log_path)
    
    with open(test_log_path, "w", encoding="utf-8") as f:
        f.write("{invalid json")
        
    result = log_error_to_json("RecoveryError", "test_component", "Recovered")
    assert result is True
    
    with open(test_log_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["error_type"] == "RecoveryError"
