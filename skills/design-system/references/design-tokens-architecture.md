# Design Token Architecture (Primitive → Semantic → Component)

One three-tier hierarchy for every platform.

## 1. Tiers

```
PRIMITIVES                SEMANTIC ROLES                 COMPONENT TOKENS
raw scales                intent                         bound to a component
──────────────            ─────────────────              ─────────────────────
blue-600 #2563EB   ──►    color.accent.primary    ──►    button.primary.container
space-16 16        ──►    layout.gap.default      ──►    card.padding
radius-lg 16       ──►    shape.container         ──►    textField.shape
font display       ──►    type.screenTitle        ──►    topBar.title
duration-200       ──►    motion.fast             ──►    chip.pressDuration
```

Screens reference semantic or component tokens only — never raw literals.

## 2. Find before you invent

1. Look for the project's token source first (profile in `DESIGN_SYSTEM.md`, else search for `*Tokens*`, `theme`, `tokens.json`, `@theme`, `:root {`, asset catalogs).
2. If one exists, use it exclusively. Never add a second parallel system.
3. If none exists, propose a minimal set (space scale, radius scale, type scale, semantic color roles incl. both themes, motion durations/curves) and agree it before building screens.
4. Optional single source: a W3C Design Tokens (DTCG) `tokens.json` generated into each platform (Style Dictionary or similar) when a product ships on several platforms.

## 3. Where tokens live per platform

| Tier | Compose | SwiftUI | Web |
|---|---|---|---|
| Primitives | `object SpaceScale`, `RadiusScale`, raw `Color`s | `enum Space`, asset-catalog colors | CSS custom properties / Tailwind `@theme` |
| Semantic | `SemanticColors` via `CompositionLocal` (`AppDesign.colors`), `AppTypography` | `Color` extensions, text styles | `--color-*`, `--type-*` roles |
| Component | `ButtonTokens`, `GlassTokens` objects | `ButtonStyle`s | component CSS variables / variant props |

## 4. Rules

1. Both themes defined at the semantic tier; components never branch on theme themselves.
2. Glass/blur parameters are tokens too (one `GlassTokens` / `.glass` class), not per-call-site values.
3. Adding a value: add it to the scale first, then use it. An off-scale number in a screen is a review finding.
4. Rename tokens, not screens: a design change should be a token edit.
