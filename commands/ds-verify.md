---
description: Run this project's verification gate — build, tests, lint, locale parity — auto-detecting Android, web or iOS
allowed-tools: Bash, Read
---
Run from the repo root whatever applies, reporting only failures (first error lines, never full logs — redirect to a file and grep, or use `repowise distill <cmd>` if installed). Use the commands recorded in `DESIGN_SYSTEM.md` when present; otherwise detect:

**Android** (a `gradlew` exists, at root or in a subfolder):
1. `./gradlew compileDebugKotlin` — 0 errors (`e: |error:`).
2. `./gradlew testDebugUnitTest` — all green (`FAILED`).
3. `./gradlew lintDebug` only if the profile says lint is part of the gate.

**Web** (`package.json`):
1. Type check: the `typecheck`/`check` script, else `npx tsc --noEmit` when a `tsconfig.json` exists.
2. `lint` script if present.
3. `test` script if present (non-watch mode, e.g. `CI=1`).
4. `build` script — the production build must succeed.

**iOS** (`*.xcodeproj`/`*.xcworkspace`): `xcodebuild -scheme <scheme from profile> -destination 'platform=iOS Simulator,name=<device>' build test`.

**Locale parity (all stacks):** `scripts/validate_strings.py` if the project has one; otherwise run `${CLAUDE_PLUGIN_ROOT}/hooks/locale-parity.sh --all` which compares every locale file against its base.

Finish with a short table: check → pass/fail → first error. Green is not "done": any UI change still needs `/ds-visual-audit`.
