# Security & Access Document

## 1. Authentication Strategy
No authentication is required for the MVP. The platform acts as an immediately accessible, empathetic digital companion for any student.

## 2. Role-Based Access Control (RBAC)
- **User:** Anonymous users have full access to submit journal entries and receive CBT-framed advice. No administrative roles are necessary.

## 3. Secret Management
- Secrets (e.g., `OPENAI_API_KEY`) are managed strictly via local `.env` files and environment variables.
- The `.gitignore` is strictly configured to exclude `.env`, `.secrets/`, and any potential credential leakage.

## 4. Data Privacy & Compliance
- **Data Masking:** `sanitize_journal_input` aggressively strips PII (e.g., Phone Numbers) using Regex matching to satisfy data privacy heuristics.
- **Data Persistence:** To eliminate data liability, the application is strictly stateless and writes zero patient/student data to disk.

## 5. Network Security
- **Prompt Injection Defense:** `sanitize_journal_input` strips HTML and escapes malicious characters (`<`, `>`, `{`, `}`) to prevent CWE-74 vulnerabilities. Input is strictly truncated to 500 characters to prevent buffer and token exhaustion attacks.
