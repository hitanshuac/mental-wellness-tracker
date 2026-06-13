# Feature Ticket List

*Agents must execute these tickets sequentially. Do not move to a new ticket until the previous one is fully verified.*

## TICKET-001: Implement Input Sanitization & DeID
- **Description:** Write a pure Python function `sanitize_journal_input(text: str) -> str`.
- **Acceptance Criteria:**
  - [x] Strips all HTML tags.
  - [x] Escapes `< > { }`.
  - [x] Truncates to 500 characters.
  - [x] Masks phone numbers.
- **Technical Constraints:** Isolated Pytest coverage in `./tests/test_sanitization.py`.

## TICKET-002: Implement Crisis Interception
- **Description:** Write `detect_crisis(text: str) -> bool`.
- **Acceptance Criteria:**
  - [x] Detects high-risk keywords (e.g., "self-harm", "hopeless").
  - [x] Returns a boolean.
- **Technical Constraints:** Isolated Pytest coverage in `./tests/test_crisis.py`.

## TICKET-003: Implement LLM Engine
- **Description:** Write `generate_wellness_response(journal_entry: str) -> str`.
- **Acceptance Criteria:**
  - [x] Uses `openai` SDK.
  - [x] Includes CBT-framed system prompt referencing high-stakes board exams (NEET, JEE, CUET).

## TICKET-004: Implement Memoized Strategies
- **Description:** Write `get_daily_mindfulness_exercise() -> str`.
- **Acceptance Criteria:**
  - [x] Returns a mindfulness exercise.
  - [x] Uses `@st.cache_data(ttl=86400)`.

## TICKET-005: Build Streamlit UI
- **Description:** Integrate all capabilities into `src/ui/app.py`.
- **Acceptance Criteria:**
  - [x] Includes `help="..."` on all widgets for A11y.
  - [x] Includes `st.warning` disclaimer.
  - [x] No emojis in markdown headers.
