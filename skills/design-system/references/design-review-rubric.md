# Design Review Rubric (before calling any visual task done)

A formal self-check the agent runs after any meaningful visual change — it complements, not replaces, the verification protocol in `SKILL.md` (section 0) and the visual review procedure in `visual-review-methodology.md`. The point: don't rely on "looks about right" — go through specific axes and decide, with a reason, on each.

## The core rule

**Never claim "this looks good" or "this is done" without capturing a fresh screenshot/recording and actually looking at it** (see `SKILL.md`, section 1). The rubric below is a structure for *what* to look at — it does not replace actually looking. A rating on any axis without a real look at the current render doesn't count.

## Six axes

For the changed screen/component, go through each axis and mark it OK / has notes / critical, with a short reason:

1. **Visual hierarchy** — the most important thing on screen reads first; a title/CTA doesn't compete in weight with secondary text; see `design-tokens-architecture.md` for the shared type scale.
2. **Consistency** — the same kind of element (screen title, CTA button, list card) looks and behaves the same everywhere it appears; no place where the style is "almost the same, but slightly different."
3. **Usability** — interactive elements read as obviously interactive, states (pressed/disabled/loading) are unambiguous, the primary action is reachable in the expected number of taps.
4. **Accessibility** — see `accessibility.md`: at minimum contrast, target size, screen-reader order for the changed screen.
5. **Adaptivity** — doesn't break at max text size, at the smallest and largest screen/viewport, in RTL (if shipped), or in either theme — actually run, not assumed (`visual-review-methodology.md` §3).
6. **Smoothness/performance** — entering/leaving never produces a double render (construction rule 1), scrolling doesn't stutter, static parts aren't re-rendered needlessly, no layout shift.

## Nielsen's heuristics that matter most

From the classic 10 usability heuristics, the ones most relevant here:

- **Visibility of system status** — long operations show clear progress, never a control that silently looks stuck.
- **Match between system and the real world** — the domain's own terms, as users know them; no invented jargon, no casual paraphrase of legal/technical terms.
- **User control and freedom** — clear back/cancel at every step; going back and changing a choice doesn't lose the rest of the state.
- **Consistency and standards** — see axis 2 above.
- **Error prevention** — the "Next" button is disabled until a valid state exists, rather than enabled and then showing an error after tapping.
- **Recognition rather than recall** — status (drafts, limits, progress) is visible where it matters, not something to remember.
- **Aesthetic and minimalist design** — see the anti-slop section below.

## Severity levels (used consistently across the project)

Use the same scale for any self-run design review, so project history stays consistent:

| Level | Criterion | Action |
|---|---|---|
| **Critical** | Blocks use, makes content unreadable/inaccessible (double render, overlap, clipping) | Fix immediately, before any new feature work |
| **High** | Noticeably breaks the experience on a specific screen, but doesn't fully block it | Fix in the current iteration |
| **Medium** | Noticeable on a careful look, reduces perceived quality | Fix at the next planned polish pass |
| **Low** | Polish/taste within the already-agreed style | Backlog |

## Anti-slop — don't drift into the library's default look

Components drift toward the UI library's default look (Material `Surface`, shadcn defaults, stock UIKit) when tokens aren't deliberate. Questions to ask before considering a light/dark variant of a component finished:
- If you removed the logo/brand color, could you still tell this is *this* product from its look alone? If not, the tokens aren't expressive enough.
- Are shadow/border/highlight tuned for the product's actual backgrounds in each theme, not an average value that looks weak in both?
- Are spacing and radius from the shared scale, not "looked fine" numbers found nowhere else?

## Self-report format (before committing)

```
Screen: Checkout — summary block
1. Hierarchy: OK
2. Consistency: OK (uses button.primary tokens)
3. Usability: OK
4. Accessibility: note — the icon-only "edit" button has no label, add one
5. Adaptivity: OK, verified in RTL, at max text size, 390px and 1440px
6. Smoothness: OK, no double render on entry/exit (checked 5 times in a row)
Result: 1 Medium note — content description — fixed in this same commit
```

A short, honest record broken down by axis, not a blanket "looks great" declaration.
