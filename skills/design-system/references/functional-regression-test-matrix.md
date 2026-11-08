# Functional/Regression Test Matrix — template

This file is a **method**, not a fixed checklist: it has no project screens in it on purpose. Build the project's own matrix from it once, then keep that matrix (not this file) up to date as the app grows. Visual quality within each scenario is judged per `visual-review-methodology.md` (look at frames, don't infer from OCR/coordinates); this file is about what must hold functionally.

## 1. Build the matrix for this project

1. Walk the app's real navigation graph (`app-navigation-and-interaction-map.md` method) and list every screen/flow once.
2. For each flow, write down: entry state → user actions → exit state(s), and which fields/toggles carry state across screens.
3. Flag the flows that are business-critical (payments, paywalls/quotas, legal documents, data loss risk) — these get re-verified on every regression pass, not just when touched.
4. Save the result as e.g. `docs/REGRESSION_MATRIX.md` in the project itself; link it from this skill's routing table once it exists.

## 2. Universal scenario shapes (apps and sites)

- **Onboarding / first-run:** every step advances, text fits in the current locale, required fields block progress, optional fields don't.
- **Auth / app lock (if present):** cold-launch gate blocks all content until passed; wrong credential/PIN shows a clear failure state without unlocking; correct one transitions cleanly.
- **Multi-step forms/wizards:** back/forward never loses entered data; "continue" is disabled until the step's required input is valid; the final step's output (document, submission, saved record) matches what was entered.
- **Lists with empty/loading/error states:** each state renders correctly, not just the happy path with data already present.
- **Anything metered (free tier, quota, trial):** exhausting it shows the correct upsell/limit screen; it never silently grants more, and never blocks a user who already has the paid tier.
- **Document/export generation (PDF, share, etc.):** the generated file opens correctly in at least one real viewer, not just "no crash".
- **Theming:** light and dark theme on every screen in the matrix — an actual screenshot pass (`visual-review-methodology.md`), not "should work in theory".
- **Locale parity:** every locale this project ships renders without clipped/truncated/shifted text, especially the longest-word languages and any RTL locale (mirroring, not just text direction).
- **System accessibility settings:** reduced transparency / increased contrast / max font scale don't produce unreadable or clipped UI.

## 3. Regression discipline

Every regression pass re-verifies this project's own construction rules (see the main `SKILL.md` §3-equivalent once filled in for this project) — these exist because a specific defect class happened once. If one regresses, fix it before starting new work, and treat the recurrence as a signal to enforce it more mechanically (lint rule, shared component, checklist item) instead of hand-fixing it again next time.
