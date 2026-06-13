# Project Handover

## Current State
The Mental Wellness Tracker MVP has been fully implemented as a pure Python Streamlit application. It acts as an empathetic digital companion for students preparing for high-stakes exams (e.g., NEET, JEE, CUET).

## Core Capabilities
- **A11y UI:** `src/ui/app.py`
- **Sanitization:** `src/capabilities/sanitization.py` (PII masking, Prompt Injection defense)
- **Crisis Router:** `src/capabilities/crisis_router.py` (Local RegEx-based emergency interception)
- **LLM Engine:** `src/capabilities/llm_engine.py` (CBT-framed OpenAI prompts)
- **Memoization:** `src/capabilities/memoization.py` (24hr TTL cache for mindfulness exercises)

## Test Coverage
- `pytest tests/` passes with 100% functional branch coverage over the pure functions in `sanitization.py` and `crisis_router.py`.

## Known Constraints
- The `OPENAI_API_KEY` must be provided in the environment or `.env` file for the LLM component to fully resolve.
- The project is strictly stateless to satisfy security heuristics; no database is utilized.
