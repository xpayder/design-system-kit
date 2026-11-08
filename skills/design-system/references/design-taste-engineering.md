# Design Taste Engineering — anti-slop rules for any UI

Metric rules that stop the default "AI-made" look, for apps and sites alike. For website pages the upstream `design-taste-frontend` skill (taste-skill 2.5.x) goes much further — art direction, section library, copy voice, photos, a browser gate. This file is the cross-platform core it shares with native apps.

## 1. Dials (set per project in `DESIGN_SYSTEM.md`)

| Dial | Range | Default | Meaning |
|---|---|---|---|
| DESIGN_VARIANCE | 1 rigid – 10 artsy | 6 | asymmetry, offset layouts, split screens |
| MOTION_INTENSITY | 1 static – 10 physics | 5 | springs, micro-motion, entrance moments |
| VISUAL_DENSITY | 1 gallery – 10 cockpit | by audience | editorial air vs data density |

## 2. Bias corrections

| Trap | Rule |
|---|---|
| Everything centered | Headlines and hero copy left-aligned (start-aligned in RTL) or a deliberate split layout. Center only for single numeric inputs, confirmations, empty-state illustrations. |
| Purple/indigo + glow + gradient text | Banned. Palette from the brand base in the token file; **one** accent, saturation under ~80%. |
| A card around everything | Group with spacing, dividers, tonal backgrounds. Elevated cards only for a hero surface, floating navigation or a primary CTA. |
| Emoji as icons | No emojis in UI or strings. One icon set, one stroke width (1.5 or 2). |
| "John Doe", "Acme", 99.99% | Realistic, locale-appropriate sample data for the real market. |
| Generic stock component look | If you hid the logo, would it still look like *this* product? If not, the tokens aren't specific enough. |
| Static UI | Every state designed: loading skeleton, empty with guidance, inline error, pressed feedback. |
| Text explaining a control | The control explains itself by its form; no captions under icons unless the owner wants them. |

## 3. Type

- One display face + one text face at most (or one variable family). Weight and size do the hierarchy, not five colors.
- A short, fixed scale (e.g. 12/14/16/20/24/32/40) from the token file; nothing off-scale.
- Line length ~60–75 characters for reading text; tighter leading on large headings.

## 4. Color

- Neutrals carry 90% of the UI; the accent marks the primary action and selection only.
- Both themes designed, not inverted; dark mode uses lifted surfaces, not pure black everywhere.
- Status colors (error/success/warning) are semantic tokens, reused, contrast-checked.

## 5. Motion

- Springs or one ease-out curve; nothing linear on things the eye follows.
- Entrances once, short (≤ ~1s total for a hero); UI responses 150–300ms.
- Animate transform/opacity only. Respect reduced motion.
- Perpetual micro-motion only on status indicators, never on body content.
- Soft, tinted shadows that match the surface hue — no muddy black drop shadows.

## 6. Layout

- One spacing scale; consistent rhythm between sections.
- Bento/asymmetric grouping for dashboards and pickers instead of a uniform list of equal cards.
- Equal edges: content never sticks to a screen edge without intent; safe areas respected.

## 7. Pre-flight

- [ ] Loading / empty / error / pressed states exist?
- [ ] Holds at smallest and largest screen and at max text size?
- [ ] Cards only where they earn it?
- [ ] Headlines start-aligned, one accent, no glow?
- [ ] Zero emojis in UI strings?
- [ ] Blur/shader work only on floating chrome?
- [ ] Looked at in light and dark as real images?
