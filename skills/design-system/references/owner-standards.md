# Owner standards — how this owner wants every product built

Distilled from the owner's feedback across projects (Android app, web game, others). These apply to **every** project by default; a project's `DESIGN_SYSTEM.md` may override one explicitly. When the owner states a new rule, add it here (generalized) and to the project profile.

## Working together

- Reply to the owner in **Russian** (Ukrainian, then Polish as fallbacks). Code and files may stay English.
- The owner dictates long messages with many unrelated points and changes their mind mid-way. Split every message into bugs / wishes / decisions / questions, write them into the project's plan file, work from the file, re-read it and the chat after each batch so nothing is dropped. The latest statement wins.
- Say plainly what was verified on a real device/browser and what only compiled. Never call a visual result "verified" without having looked at a fresh capture.
- Don't change what wasn't asked; propose improvements, don't sneak them in.

## Interface equals function

- Interface and function are equally important. A new feature is not done until it is integrated beautifully, without overloading the screen, and matches the neighbouring UI.
- Never invent a new control or pattern when an existing one in the product fits. Extend what exists.
- Details matter: compare the changed screen with its neighbours before reporting.
- First impression counts ("встречают по обложке"): nothing shown to the owner may contain grey placeholder boxes or debug UI.

## Minimal, contextual UI

- Fix a visibility problem in the element itself (placement, size, angle, light, contrast) — don't add an extra widget, HUD element or explanation to compensate.
- No duplicated text: a title, subtitle, badge and body never repeat each other; a card's title equals the title of the screen it opens.
- Icon tools (editors, toolbars, shelves): icons **without captions** (Canva / CapCut style), all in **one row**; if they overflow, the row scrolls horizontally. Never wrap into several rows, never replace with long text pills.

## Visual system

- **One background** for the whole product, quiet and deliberate (base tone, soft light, subtle texture at most). No per-screen backgrounds. Bright colored glows and over-saturated blue/violet looks were rejected.
- **One palette source** feeding both themes. Dark: no pure black backgrounds, no pure white text. Light: must look clean and crisp, never grey or "dirty" — texture/vignette effects that work in dark are often wrong in light.
- **Always check both themes** after any color, background or surface change. Dark-only checks have hidden real defects.
- **The app's own theme setting overrides the system theme** everywhere (components read the app's theme flag, not the OS flag directly).
- **Edge-to-edge, one rule for every screen:** nothing paints a color behind the status bar; content scrolls under it and under a floating top capsule; top padding = capsule height + status-bar inset. Insets are applied exactly once (watch for frameworks that add them a second time).
- **Cards share one fill and one border recipe.** Secondary buttons are tonal (light accent fill + accent border) with the same height and radius as the primary button.
- **Fonts are bundled** (offline, no font servers/trackers) and cover every script the product ships (e.g. Cyrillic). Audit stray fonts by temporarily swapping the app font to a serif and screenshotting every screen. Numbers and codes use tabular figures.
- Long titles shrink down to a minimum size before they ever ellipsize.

## Startup and state

- No flash of a wrong screen at startup: until state is loaded, show only the background, never a guessed destination.
- When the UI and the data disagree (a toggle that doesn't stick, a list that needs a restart), verify at the data level (query the actual store after the action) before blaming the UI.

## Verification habit

- After every visible change: record the whole affected flow, review it from the very first frames (loading, first screen, transitions), with dense frame sampling around events — not occasional screenshots.
- Check every variant the change touches (each step, each level/biome, each state), not one sample.
- When the review is done, delete the recordings and extracted frames; keep the project and the machine clean.
