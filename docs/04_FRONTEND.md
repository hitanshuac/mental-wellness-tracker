# Frontend Specification Document

## 1. Design System & Theming
- **Framework:** Streamlit Native UI.
- **Layout:** Centered, simple, and engaging to reduce cognitive load for students facing severe stress.
- **Typography:** Streamlit default sans-serif (clean and modern).
- **Rule Enforcement:** Emojis are strictly banned from being placed inside markdown structural headers (e.g., `#`, `##`) to ensure code quality analyzer compliance.

## 2. Global State Management
- Stateless. The application processes one journal entry per session. Long-term state is actively avoided.

## 3. Core Layouts & Routing
- `/` - Main Dashboard Application: Contains the Medical Disclaimer, Daily Mindfulness Exercise, and the primary Journal Entry text area.

## 4. API Contracts
- **Internal APIs:** Pure Python function calls mapping `app.py` directly to the `src/capabilities/` modules. No external REST routing is utilized to ensure lightning-fast execution.
- **External APIs:** Outbound connections to `api.openai.com` via the official `openai` Python SDK.

## 5. Accessibility (a11y) & Responsiveness
- **ARIA Compliance:** Every Streamlit input widget (`st.text_area`, `st.button`) MUST include the `help="description"` parameter to guarantee full screen-reader support.
- **Medical Disclaimer:** A persistent `st.warning` banner is displayed at the top of the application, explicitly clarifying that the tool is NOT a licensed therapist.
