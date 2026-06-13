# Project Handover

## Current State
The Mental Wellness Tracker MVP has been fully implemented as a pure Python Streamlit application. It acts as an empathetic digital companion for students preparing for high-stakes exams (e.g., NEET, JEE, CUET).

## Core Capabilities
- **A11y UI:** `src/ui/app.py` (Psychological UI with Affect Labeling, SUDS scale slider, and calming CSS)
- **Sanitization:** `src/capabilities/sanitization.py` (PII masking, Prompt Injection defense)
- **Crisis Router:** `src/capabilities/crisis_router.py` (Local RegEx-based emergency interception)
- **LLM Engine:** `src/capabilities/llm_engine.py` (CBT-framed Google Gemini 2.5 Flash prompts)
- **Circuit Breaker:** `src/capabilities/circuit_breaker.py` (Stateful 3-strike failure mitigation)
- **Observability:** `src/capabilities/observability.py` (Structured JSON error logging)
- **Memoization:** `src/capabilities/memoization.py` (24hr TTL cache for mindfulness exercises)

## Test Coverage
- `pytest tests/` passes with 100% functional branch coverage over the pure functions in `sanitization.py`, `crisis_router.py`, `circuit_breaker.py`, and `observability.py`.

## Known Constraints
- The `GEMINI_API_KEY` must be provided via `st.secrets` or the environment (`os.environ`) for the LLM component to fully resolve.
- The project is strictly stateless to satisfy security heuristics; no database is utilized, relying instead on pure memory (`st.session_state`) and localized JSON logging.
