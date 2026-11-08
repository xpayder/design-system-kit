# Component Spec Template (anatomy + every state + a11y)

A short, mandatory structure for specifying any reusable component (`PrimaryButton`, `ScreenHeader`, list card, chip, text field, radio item, etc.) — both new components and refactors of existing ones.

## Why this matters here specifically

Defects where two floating elements end up overlapping, or a toast covers a button, are ultimately cases where a component's *concurrency* with other elements was never explicitly decided — only its default look was designed. A formal spec forces that decision at design time instead of discovering it on a recording later.

## Required sections

For each component, a short spec (a code comment or a short doc) covering:

### 1. Anatomy
What parts it's made of: icon, title, subtitle, trailing element (chevron/switch/arrow), container. What's required vs. optional.

### 2. Variants
E.g. for a list card: `default` (trailing chevron), `withBadge` (a counter), `disabled` (a feature unavailable on the current plan).

### 3. States — the minimum required set
Never describe a component as "it just looks like this" — go through each state explicitly:

| State | Required for | Example |
|---|---|---|
| `default` | everything | normal appearance |
| `pressed`/`hover` (hover only if mouse/stylus input is possible) | interactive elements | tapping a card/button |
| `focused` | interactive elements (screen reader / keyboard) | a visible focus ring |
| `disabled` | wherever applicable | "Next" before a required choice is made |
| `loading` | any async operation | generating a file, a network request |
| `error` | anything with validation | a required field left empty |
| `selected` | anything that's part of a choice | the chosen radio item or chip |
| **concurrency with another element on screen** | any component that can appear near/over another floating element (snackbar/toast, bottom sheet, promo card) | **the state most often skipped — see below** |

### 4. Concurrency — the state most often skipped
Explicitly document what happens when this component needs to appear while another floating/overlay element is already showing. Required pairs to document for every floating/overlay component:
- Snackbar/toast + any floating bottom dock/CTA → the toast always sits above it with margin, never covers it (`SKILL.md` construction rule 3).
- Two floating cards that can be triggered by the same flow (e.g. an offer card and a share card) → mutually exclusive, one visible at a time, modeled as one state (rule 2).
- Any screen entering/leaving composition (navigation) → see `SKILL.md` construction rule 1; this check is required at the screen-container level too, not only for individual components.

### 5. Token mapping
Which component tokens it uses (see `design-tokens-architecture.md`) — no "magic" value that didn't come from a token.

### 6. Accessibility spec
See `accessibility.md` — at minimum: screen-reader label, platform minimum target size, reading order, what gets announced on a state change.

## Mini example: `PrimaryButton` spec

```
Anatomy: [optional leading icon] + label (1 line) + full-width container
Variants: filled (primary), outlined (secondary action)
States: default, pressed (scale 0.98 spring), focused (visible ring), disabled (reduced
        opacity, no press reaction), loading (spinner replaces label, keeps its exact size — never jumps)
Concurrency: primary + secondary on one screen sit in one vertical stack with fixed spacing, never
        overlapping; a promo card that appears is inserted INTO that stack, never overlaid on it
Tokens: button.primary.* (see design-tokens-architecture.md)
A11y: label is the text itself; height >= platform minimum (48dp / 44pt / 44px touch);
        disabled state announced by role
```

## When to write the full spec vs. skip it

Write the full spec for reusable components (used on 2+ screens) and for any component that has already caused a visual defect once. For one-off layout on a single screen that won't be reused elsewhere, it's enough to explicitly check items 3 (states) and 4 (concurrency) in substance, without a separate spec file.
