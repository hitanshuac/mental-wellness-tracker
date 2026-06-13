# Product Requirements Document (PRD)

**Project Name:** Mental Wellness Tracker
**Date:** 2026-06-13
**Status:** In Review

## 1. Objective
Build an empathetic, always-available digital companion to help students monitor and improve their mental well-being. The Generative AI-powered solution analyzes open-ended daily journaling and mood logs to uncover hidden stress triggers that standard trackers miss. This directly aligns with the Hack2Skill competition requirements.

## 2. Target Audience / Personas
- **Persona 1 (Students):** Students preparing for high-stakes board exams and competitive entrance tests (e.g., NEET, JEE, CUET, CAT, GATE, UPSC) who face severe stress, burnout, and self-doubt.

## 3. Core Features (MVP)
*Must-have features for the first release.*
1. **Sanitization:** Strict data de-identification and input scrubbing to prevent Prompt Injection (CWE-74) and ensure privacy.
2. **Crisis Interception:** Real-time semantic and regex checks to detect high-risk distress (e.g., "self-harm") and route to emergency intervention BEFORE LLM processing.
3. **Memoized Mindfulness:** Cached daily coping strategies to maximize efficiency and avoid synchronous thread blocking.
4. **CBT-Framed Analysis:** LLM integration providing actionable advice based on Cognitive Behavioral Therapy principles.
5. **A11y Compliant UI:** Accessible Streamlit interface with ARIA-compliant tooltips and medical disclaimers.

## 4. Out of Scope (Non-Goals)
*Explicitly list what the AI/Agents should NOT attempt to build in this phase.*
- Database persistence (no heavy databases, strictly pure local JSON or memory).
- Medical diagnosis (the tool is NOT a licensed therapist).

## 5. Success Metrics
*How will we know this product is successful?*
- 100/100 score against automated SAST and AI Code Analyzers (Hack2Skill Evaluator Rules).
- 100% Pytest branch coverage on pure isolated functions in `./tests/`.
