---
description: Create or refresh this project's DESIGN_SYSTEM.md profile (stack, brand dials, tokens, components, locales, hotspots, verify commands, invariants)
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---
Load the `design-system` skill, then build the project profile described in its §0.

1. If `DESIGN_SYSTEM.md` exists at the repo root, read it and only fill gaps or fix what is out of date; never drop the owner's recorded decisions.
2. Detect, don't guess:
   - **Stack:** `build.gradle(.kts)` / `libs.versions.toml` (Android: Compose, Material 3, Haze version), `package.json` (framework, Tailwind, i18n library), `*.xcodeproj` / `Package.swift` (iOS).
   - **Token source:** search for `*Tokens*`, `Theme.kt`, `Type.kt`, `tokens.json`, `@theme`, `:root {` with custom properties, asset catalogs.
   - **Shared components:** the button, text field, card, top bar, dialog/sheet primitives that screens already reuse.
   - **Locales:** `res/values-*/strings.xml`, `locales|messages|i18n/*.json`, `*.xcstrings`; mark RTL ones.
   - **Hotspots:** Repowise `get_risk`/`get_health` if available, else `git log --since=90.days --name-only` churn on UI files.
   - **Verify commands:** real Gradle tasks / npm scripts / xcodebuild scheme.
3. Ask the owner only for what can't be detected: the brand brief (three words, accent, themes, density, motion intensity) and business invariants. Offer sensible defaults from `references/design-taste-engineering.md` §1.
4. Write `DESIGN_SYSTEM.md` with sections 1–9 from the skill's §0, each short and factual, plus a "Last refreshed" date. If the project has Haze older than the version in `platforms/android-compose.md`, note the available upgrade — don't upgrade without being asked.
5. Report in Russian what was detected, what was assumed, and what still needs the owner's answer.
