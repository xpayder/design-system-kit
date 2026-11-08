# Platform guide — Web (HTML/CSS, React, Next.js, Vue, Svelte, Astro, Tailwind)

How the universal principles in `../SKILL.md` become web code. Read the project's `DESIGN_SYSTEM.md` first.

For building or restyling **marketing / company / landing pages**, load the upstream `design-taste-frontend` skill (taste-skill plugin) — it carries the page-level art direction, section library, copy rules and a real-browser finish gate. This guide is the system layer underneath it and also covers web *apps* (dashboards, tools, forms) the taste skill doesn't target.

## 1. Tokens on the web

- Primitives and semantic roles as CSS custom properties on `:root`, dark values under `@media (prefers-color-scheme: dark)` and/or `[data-theme="dark"]`:
  ```css
  :root {
    --space-4: 1rem;  --radius-lg: 16px;
    --color-bg: #f7f8fa;  --color-fg: #0a101d;  --color-accent: #2563eb;
    --font-display: "Your Display", system-ui, sans-serif;
  }
  ```
- Tailwind 4: declare the same values in `@theme { … }` so utilities and CSS share one source; don't sprinkle arbitrary values (`p-[13px]`, `text-[#123456]`) in components.
- Type in `rem`; fluid headings with `clamp()`; body line length ~60–75ch.
- Self-host fonts (`font-display: swap`, preload the one above-the-fold face); every requested weight/italic must actually load.

## 2. Construction rules → web

1. **One transition owner:** route transitions via the framework's one mechanism (View Transitions API, the router's transition, or one wrapper component) — not ad-hoc fades in each page.
2. **Mutually exclusive overlays = one state:** one `overlay: 'none' | 'offer' | 'share'` value rendered by a single switch; toasts in one region that never sits on top of the primary CTA.
3. **Reserved space:** sticky/fixed headers and bottom bars pad content by their real height and `env(safe-area-inset-*)`; `scroll-padding-top` for anchor jumps.
4. **Shared components:** one `Button`, one `Input`, one `Card` primitive; variants via props, not copies.
5. **RTL:** logical properties (`margin-inline-start`, `padding-inline`, `inset-inline-end`, `text-align: start`), `dir="rtl"` on `<html>` for RTL locales; mirror only direction-bearing icons.
6. **Animate `transform` and `opacity` only**; no animating `width/height/top/left` in scroll or pointer paths. One ease-out curve (e.g. `cubic-bezier(0.2, 0, 0, 1)`), 150–300ms for UI.
7. **Targets:** ≥ 24×24 CSS px is the WCAG 2.2 AA minimum (2.5.8); aim for 44×44 on touch layouts.
8. **No layout shift:** reserve image/video dimensions (`width`/`height` or `aspect-ratio`), skeletons the size of the final content.

## 3. Glass on the web

Principles in `../references/glass-and-translucency.md`. Implementation:

```css
.glass {
  background: color-mix(in srgb, var(--color-bg) 72%, transparent);
  backdrop-filter: blur(20px) saturate(1.4);
  -webkit-backdrop-filter: blur(20px) saturate(1.4);
  border: 1px solid color-mix(in srgb, white 24%, transparent);
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.25), 0 8px 24px rgb(0 0 0 / 0.12);
}
@supports not (backdrop-filter: blur(1px)) { .glass { background: var(--color-bg); } }
@media (prefers-reduced-transparency: reduce) { .glass { backdrop-filter: none; background: var(--color-bg); } }
@media (prefers-contrast: more) { .glass { background: var(--color-bg); border-color: var(--color-fg); } }
```

`backdrop-filter` is expensive on large or many surfaces — keep it to bars, docks and menus; test scrolling on a mid-range phone.

## 4. Accessibility specifics (web)

- Semantic HTML first (`button`, `a`, `nav`, `main`, headings in order); ARIA only to fill gaps.
- Visible `:focus-visible` ring on every interactive element, never `outline: none` without a replacement.
- Every control keyboard-operable; modals trap focus and restore it; `Esc` closes.
- `prefers-reduced-motion: reduce` turns transitions into instant state changes.
- Text zoom to 200% without loss; no fixed-height text containers.
- Images: meaningful `alt`, decorative `alt=""`.
- axe / Lighthouse are navigation aids for finding issues; the contrast and layout verdict still comes from looking at the render.

## 5. Locales

Message files (`locales/*.json`, `messages/*.json`, `i18n/*.json`, `*.po`) share exactly the same keys as the base locale — the plugin's hook checks JSON key parity after each edit. Use `Intl` for dates, numbers, plurals; never concatenate translated fragments.

## 6. Getting the page on screen and looking at it

- Run the dev server (or the production build for the final check — dev servers lie about performance and fonts).
- Capture at **1440×900** and **390×844** at minimum (plus 768 if there's a tablet layout), light and dark, one long-word locale and RTL if shipped. Use the Claude in-app browser (`preview_start` + screenshot) or Playwright:
  ```bash
  npx playwright screenshot --viewport-size=390,844 --full-page http://localhost:3000 shot-390.png
  ```
- Record interactions (hover, menus, route transitions) and review frames per `../references/visual-review-methodology.md`.
- DOM snapshots / accessibility trees are for locating elements to click, not for judging the design.

## 7. Verify

Type check (`tsc --noEmit` or the framework's check), lint, unit tests, production build (`npm run build`), locale parity. `/ds-verify` detects `package.json` scripts and runs what exists.
