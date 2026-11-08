# design-system-kit

Universal design system + visual QA plugin for Claude Code. Works for native Android, iOS and web projects. Grew out of the Kündigungs-Experte project plugin (`plugins/kuendigungs-experte`, unchanged).

## Install

From GitHub (private repo — you need collaborator access), in Claude Code:

```
/plugin marketplace add xpayder/design-system-kit
/plugin install design-system-kit@design-system-kit
```

Updates later: `/plugin marketplace update design-system-kit`.

From a folder (e.g. unzipped from an archive):

```
/plugin marketplace add /path/to/design-system-kit
/plugin install design-system-kit@design-system-kit
```

Run `/reload-plugins` (or restart) afterwards.

Requires `python3` for the locale-parity hook. Android work needs `adb`; web screenshots use the in-app browser or `npx playwright`.

`skills/design-system/references/owner-standards.md` holds the author's personal working rules (language, review habits, visual preferences). Edit it to your own before use.

## Contents

| Part | What it does |
|---|---|
| `skills/design-system` | Core skill: owner standards, project profile, principles, construction rules, routing to platform guides (`platforms/android-compose.md`, `web.md`, `ios-swiftui.md`) and references |
| `skills/liquid-glass-reference` | Apple Liquid Glass SwiftUI reference |
| `skills/stitch-skill` | `DESIGN.md` for Google Stitch |
| `skills/imagegen-frontend-mobile` | Mobile screen concepts via image generation |
| `skills/ux-researcher-designer` | Personas, journeys, usability tests (with scripts and references) |
| `/ds-init` | Writes the project's `DESIGN_SYSTEM.md` |
| `/ds-verify` | Build, tests, lint, locale parity — detects Gradle / npm / Xcode |
| `/ds-visual-audit` | Capture on device / simulator / browser and review frames as images |
| hook `locale-parity.sh` | After editing `strings.xml` or JSON message files, checks key parity across locales |

## Recommended upstream plugins (web work)

Not vendored, so they update themselves. Install once:

```
/plugin marketplace add Leonxlnx/taste-skill
/plugin install taste-skill@taste-skill
/plugin marketplace add Leonxlnx/taste-skill-classics
/plugin install taste-skill-classics@taste-skill-classics
/plugin marketplace add Leonxlnx/imagegen-skills
/plugin install imagegen-skills@imagegen-skills
```

`taste-skill` 2.5.x needs Node and Chrome for its browser checker and adds a Stop-hook gate for website builds; it does nothing in folders without a tasteskill build.

## Sources and versions (checked 2026-11-08)

| Item | Source | Version / state |
|---|---|---|
| Haze API in `platforms/android-compose.md` | github.com/chrisbanes/haze | 2.1.0 (2026-11-02) |
| `stitch-skill` | Leonxlnx/taste-skill-classics | 2026-10-19; `disable-model-invocation` removed so the router can pick it, description adjusted |
| `imagegen-frontend-mobile` | Leonxlnx/imagegen-skills | 2026-10-19, unchanged |
| `ux-researcher-designer` | alirezarezvani/claude-skills (MIT) | 2026-11-05, unchanged |
| `liquid-glass-reference` | conorluddy/LiquidGlassReference | not copied (no license) — the skill reads it from GitHub; iOS 27 changes in `glass-and-translucency.md` |
| Dropped | taste-skill v1 copy (superseded by 2.5.x upstream), `redesign-skill` (merged into taste-skill upstream), `output-skill` (retired upstream) | — |

To refresh: compare each vendored folder with its upstream repo and re-run `claude plugin validate`.
