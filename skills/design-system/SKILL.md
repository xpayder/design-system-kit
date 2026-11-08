---
name: design-system
description: Universal design-system and visual-QA standard for any product UI — native Android (Kotlin/Jetpack Compose), iOS (SwiftUI), or web (HTML/CSS, React, Next.js, Vue, Svelte, Tailwind). Use for ANY work on how an app or site looks, feels or behaves on screen: building or restyling screens and components, design tokens, typography/color/spacing, glass/blur, motion, accessibility, localization, visual review of screenshots or recordings, and pre-release UI regression. Routes to the right platform guide and specialist skill.
---

# Design System — universal standard

One set of principles for every product, with a thin platform layer underneath. The principles never change between projects; what changes is the **project profile** (§0) and the **platform guide** (§2).

## Routing — read only what the task needs

| Task involves... | Read |
|---|---|
| **Always, before any UI work** | `references/owner-standards.md` — the owner's rules for every product |
| First time in this project, or no `DESIGN_SYSTEM.md` yet | §0 below, then run `/ds-init` |
| Kotlin / Jetpack Compose / Android | `platforms/android-compose.md` |
| HTML/CSS, React, Next.js, Vue, Svelte, Astro, Tailwind | `platforms/web.md` |
| SwiftUI / UIKit / iOS | `platforms/ios-swiftui.md` |
| Looking at screenshots / recordings, judging a change | `references/visual-review-methodology.md` |
| Anti-slop rules, type, color, motion baselines | `references/design-taste-engineering.md` |
| Tokens (Primitive → Semantic → Component) | `references/design-tokens-architecture.md` |
| Glass / blur / translucency on any platform | `references/glass-and-translucency.md` |
| Accessibility: contrast, targets, screen readers, motion, RTL | `references/accessibility.md` |
| Specifying a component and all its states | `references/component-spec-template.md` |
| Self-review before calling a UI task done | `references/design-review-rubric.md` |
| Building this project's regression matrix | `references/functional-regression-test-matrix.md` |
| Mapping this project's navigation / routes | `references/app-navigation-and-interaction-map.md` |
| Repowise / projectmem, if installed | `references/repowise-mcp-integration.md`, `references/agent-memory-architecture.md` |

Commands: `/ds-init` (write the project profile), `/ds-verify` (build, tests, locale parity — auto-detects the stack), `/ds-visual-audit` (capture and review frames — device or browser).

## Skill catalog — pick one specialist, load only it

Bundled in this plugin (`design-system-kit:<name>`):

| Situation | Skill |
|---|---|
| Apple Liquid Glass / SwiftUI glass API lookup | `liquid-glass-reference` |
| A `DESIGN.md` design-system document for Google Stitch | `stitch-skill` |
| Mobile screen concepts / multi-screen flows as generated images | `imagegen-frontend-mobile` |
| Personas, journey maps, usability test plans | `ux-researcher-designer` |

Upstream, installed separately so they stay current (see the plugin README for the one-time commands). Use them **only for web work** — they are written for the browser and check pages in headless Chrome:

| Situation | Skill (plugin) |
|---|---|
| Build, redesign or review a website / landing page; it "looks AI-made" | `design-taste-frontend` (`taste-skill`) |
| A specific named style: soft, minimalist, brutalist, gpt-taste | `soft-skill` / `minimalist-skill` / `brutalist-skill` / `gpt-tasteskill` (`taste-skill-classics`, run by name only) |
| Website comps, brand kits, image → code | `imagegen-frontend-web` / `brandkit` / `image-to-code` (`imagegen-skills`) |

For native apps (Compose, SwiftUI) the taste rules live in `references/design-taste-engineering.md`; don't run the web taste skill's browser gate against a native app.

## 0. Project profile — fill in once per project

Every project gets a short `DESIGN_SYSTEM.md` at its root (create it with `/ds-init`). Read it before any UI work; if it's missing, create it before writing screens. It records what this skill must not guess:

1. **Platform(s) and stack** — e.g. "Android, Compose, Material 3, Haze 2.1" or "Next.js 15, Tailwind 4".
2. **Brand brief** — tone in three words, the one accent color, light/dark/both, density (airy ↔ dense), motion intensity. These set the dials in `design-taste-engineering.md` §1.
3. **Token source** — the file(s)/objects that hold primitives, semantic roles, component tokens. If none exist, propose a minimal set first (`design-tokens-architecture.md` §2).
4. **Shared components** — the button, text field, card, top bar the whole product must reuse.
5. **Locales** — which ones ship, which are RTL, where the files are.
6. **Hotspots** — files with repeated UI bugs (from `get_risk`/`get_health` if Repowise is installed, else `git log` churn).
7. **Verify commands** — build, unit tests, lint, and how to get the app on screen.
8. **Business invariants** — what must never regress (a free tier that stays free, fixed legal wording, a quota). Written down explicitly, never invented.
9. **Overrides** — where this project deliberately departs from `references/owner-standards.md`, and any project-only rules the owner states. A new rule that would apply to every product goes into `owner-standards.md` too.

## 0a. Intake protocol (any multi-part request)

1. Split the message into tasks and record them somewhere durable (a plan file, issues, projectmem) — not only in chat memory.
2. Work from that record; mark an item done only with its evidence type (fresh screenshot, passing test, or honestly "compiled only").
3. A later statement overrides an earlier one; update the record.
4. Never change what wasn't asked (no moving text while fixing a card). If an improvement looks worthwhile, ask first.
5. New features must blend into the existing UI — same components, same patterns, no invented ones.
6. End each turn with: done, not verified, next — from the record.

The owner-specific version of this protocol (language, dictated messages, honesty about verification) is in `references/owner-standards.md`.

## 1. The core rule: design judgment only from real vision

Never judge UI quality, find visual defects, or say a change "looks right" from OCR text, DOM dumps, element coordinates or a passing test alone. Those are blind to blur, transparency, layering, contrast, clipping, stray shadows, rhythm and consistency.

1. Open every relevant screenshot or frame **as an image** and look at it.
2. After every meaningful visual or functional change, capture a **fresh** frame and look at it before calling the task done.
3. Audit flows as a continuous recording (contact sheets + native-resolution zoom on transitions), not piecemeal stills.
4. Scripts that read the accessibility tree / DOM are **navigation aids** (finding what to tap or click), never evaluators.
5. Compile/test green is the floor, not the finish. Final confirmation is visual, on a real device, emulator or browser.

Procedure: `references/visual-review-methodology.md`.

## 2. Principles (platform-neutral)

Details and code per platform are in `platforms/*.md`; these hold everywhere.

1. **One token source.** No raw colors, sizes or durations in screen code once tokens exist.
2. **Hierarchy before decoration.** One thing reads first on every screen; one primary action per view.
3. **Anti-slop defaults.** Left-aligned headlines, one accent color, no AI glow/gradient text, no card-for-everything, no emojis as icons, realistic sample data. (`design-taste-engineering.md`)
4. **Every state exists.** Default, pressed/hover, focused, disabled, loading (skeleton, not a lone spinner), empty, error, selected — plus how the component coexists with other floating UI. (`component-spec-template.md`)
5. **Glass only on the control layer.** Bars, docks, capsules, sheets' chrome — never content, never glass on glass, always a readable fallback. (`glass-and-translucency.md`)
6. **Motion has one owner and one curve.** Animate transform/opacity only; spring or one ease-out; respect reduced motion.
7. **Accessibility is measured, not assumed.** Contrast ratios computed, platform target sizes, screen-reader order, max text size, RTL. (`accessibility.md`)
8. **Localization parity.** Every user-facing string exists in every shipped locale; long-word and RTL locales checked visually.
9. **Consistency over novelty.** The same kind of element looks and behaves the same everywhere.

## 3. Construction rules that make defect classes impossible

1. **Screen transitions have one owner** — two screens are never both visible at alpha > 0.
2. **Mutually exclusive floating content is one state** — an exhaustive switch over one enum, not independent overlays.
3. **Floating chrome reserves its space** — snackbars/toasts sit above docks; scroll content is padded by the real chrome height plus system insets/safe areas.
4. **Shared components are actually shared** — one text field, one button family.
5. **RTL is verified, not assumed** — logical start/end everywhere; directional icons mirror, others don't.
6. **Accent is sparing and semantic** — strong tint only on the primary action.
7. **Layout never animates in hot paths** — transforms and opacity only.

Platform guides translate each rule into concrete code.

## 4. Done means

- [ ] Owner standards and project profile read and respected.
- [ ] Platform guide followed; tokens and shared components used.
- [ ] All states implemented; floating-content concurrency decided.
- [ ] `/ds-verify` green.
- [ ] Fresh capture reviewed as images in light and dark, a long locale, RTL if shipped, max text size.
- [ ] Rubric pass written (`design-review-rubric.md`), honest about what was not verified.
- [ ] Recordings and extracted frames deleted after review.
