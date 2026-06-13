# Technical Architecture Document (TAD)

## 1. System Context
The system is an empathetic, always-available digital companion for students preparing for high-stakes board exams (e.g., NEET, JEE, CUET). Students interact with a web-based frontend to submit journal logs, which are sanitized and analyzed by an LLM to uncover hidden stress triggers.

## 2. Component Architecture
- **Streamlit UI (`src/ui/app.py`):** Handles A11y compliant user interactions and rendering.
- **Sanitization Layer (`src/capabilities/sanitization.py`):** Strips HTML, truncates input, and masks PII.
- **Crisis Router (`src/capabilities/crisis_router.py`):** Intercepts high-risk distress signals before LLM processing.
- **LLM Engine (`src/capabilities/llm_engine.py`):** Connects to OpenAI to generate CBT-framed advice.
- **Memoization Layer (`src/capabilities/memoization.py`):** Caches mindfulness exercises to ensure high efficiency and non-blocking threads.

## 3. Data Flow / State Management
User Input -> `sanitize_journal_input` -> `detect_crisis`
- If Crisis: Return immediate medical intervention block.
- If Safe: Forward sanitized text to `generate_wellness_response` -> Streamlit UI.

## 4. Database Schema (High Level)
*Strictly stateless architecture. No database is used.*
- State is managed strictly in memory for the duration of the request.

## 5. Technology Stack
- **Frontend/Backend:** Streamlit (Python 3.11)
- **Database:** None (Pure memory)
- **LLM Provider:** OpenAI
- **Testing:** Pytest (100% Branch Coverage on Pure Functions)
