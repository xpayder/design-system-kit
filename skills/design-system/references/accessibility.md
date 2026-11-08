# Accessibility — universal checklist

The principles are the same everywhere; the mechanisms and units differ. Platform specifics: `../platforms/*.md` §4.

## 1. Numbers per platform

| Check | Android | iOS | Web |
|---|---|---|---|
| Min touch target | 48×48 dp | 44×44 pt | 24×24 CSS px (WCAG 2.2 AA), 44×44 recommended on touch |
| Text unit | `sp` | Dynamic Type text styles | `rem` |
| Max text size to test | 200% font scale | largest accessibility size | 200% zoom |
| Screen reader | TalkBack | VoiceOver | NVDA / VoiceOver / TalkBack in browser |
| Reduced motion signal | animator duration scale 0 | `accessibilityReduceMotion` | `prefers-reduced-motion` |
| Reduced transparency | none from system — app setting | `accessibilityReduceTransparency` | `prefers-reduced-transparency` |
| Increased contrast | high-text-contrast flag (partial) | `colorSchemeContrast == .increased` | `prefers-contrast: more` |

Never carry a number across platforms unchanged (48dp ≠ 44pt ≠ 44px).

## 2. Contrast (WCAG 2.2 AA, applies to all platforms)

- Text 4.5:1; large text (≥ 18pt regular / ≥ 14pt bold equivalent) 3:1; non-text UI (borders, icons that convey state) 3:1.
- Compute from final colors, including the real alpha of a translucent surface over the actual content behind it. Check the worst real background, both themes.

## 3. Screen readers

- Every icon-only control has a localized label in every shipped locale.
- Decorative layers (highlights, ornaments) are hidden from the reader.
- Reading order matches visual order — floating bars/docks/overlays often break it; test by listening with the screen off.
- State changes and async results are announced (live region / announcement), toasts included.
- Dialogs move focus in on open and back to the trigger on close; background is not reachable while open.

## 4. Keyboard and focus

Visible focus on every interactive element; logical tab order; modals trap focus; `Esc`/back closes. Relevant on web always, on Android/iOS for hardware keyboards, foldables, tablets.

## 5. Motion

With reduced motion on, transitions become instant state changes (not just faster), parallax and perpetual loops stop, essential feedback stays.

## 6. Text size

At the maximum size text may wrap; it must never clip, truncate essential content, or overlap. No fixed-height text containers.

## 7. RTL

Logical start/end everywhere; mirror direction-bearing icons (back, chevrons, progress) but not neutral ones (star, check, camera); progress indicators read right-to-left; glass highlights and docks positioned logically.

## 8. Sign-off pass (before calling a screen accessible)

1. Screen reader on, go through the flow listening only.
2. Maximum text size.
3. Reduced motion on.
4. RTL locale, if shipped.
5. Light and dark, increased contrast.
Only after all five is the screen's accessibility verified.
