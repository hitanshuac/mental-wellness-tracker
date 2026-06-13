# Hack2Skill Mental Wellness Tracker - AI Engineering Rules
**Trigger:** always_on
**Role:** Senior GenAI Engineer & Compliance Evaluator

## 🚨 1. PASS/FAIL CONSTRAINTS (DO NOT VIOLATE)
- **Repository Size:** The final repo MUST remain under 10 MB. ALWAYS ensure `.venv`, `__pycache__`, and `*.db` are strictly defined in `.gitignore`.
- **Branching:** Use ONLY the `main` branch. Never create or switch to sub-branches.
- **Database:** NEVER use heavy local databases (PostgreSQL/MySQL). Use pure local memory, local JSON, or lightweight SQLite.
- **Problem Statement Alignment:** The following keywords MUST be injected verbatim into the `README.md` and module-level docstrings:
  - `"Mental Wellness Tracker"`
  - `"high-stakes board exams"`
  - `"NEET, JEE, CUET"`
  - `"hidden stress triggers"`
  - `"empathetic, always-available digital companion"`
- **STRICT EMOJI BAN:** There is a strict rule of absolutely NO EMOJIS anywhere in the codebase. This includes frontend elements, markdown documents, headers, and metadata.

## 🏥 2. MEDICAL & SECURITY COMPLIANCE (CWE-74 & HIPAA)
- **Crisis Interception (Duty to Warn):** 
  - ALWAYS write a local `detect_crisis(text)` pure function using a keyword dictionary (e.g., "self-harm", "hopeless").
  - If a crisis is detected, bypass the LLM entirely and return a hardcoded emergency hotline response.
- **Input Sanitization (Prompt Injection / XSS):** 
  - ALL user inputs must pass through a `sanitize_input(text)` function before reaching the LLM.
  - MUST strip HTML tags, escape `< > { }` brackets, and aggressively truncate input to a maximum of 500 characters.
- **HIPAA Data De-identification:** Mask phone numbers, emails, and obvious PII using Regex before LLM API calls.
- **FDA SaMD Exemption:** The system prompt MUST state: *"You are an educational companion, not a licensed therapist. Do not diagnose."* The UI MUST display a persistent Medical Disclaimer Banner at the top.

## 🏗️ 3. ARCHITECTURE & CODE QUALITY
- **Strict Modularity:** NEVER write a monolithic `app.py`. Split capabilities into distinct modules (e.g., `src/capabilities/llm_engine.py`, `src/capabilities/sanitization.py`, `src/ui/app.py`).
- **Type Hinting:** EVERY function MUST have strict Python type hints (e.g., `def parse_log(log: str) -> dict:`).
