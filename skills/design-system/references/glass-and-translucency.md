# Glass & Translucency — platform-neutral rules

Grounded in Apple's HIG (Materials), WWDC25 "Meet Liquid Glass" and the iOS 27 refinement (released 2026-09-14). Paraphrased; for exact wording see `developer.apple.com/design/human-interface-guidelines/materials`. Implementation per platform: Compose/Haze in `../platforms/android-compose.md`, CSS `backdrop-filter` in `../platforms/web.md`, SwiftUI `.glassEffect` in `../platforms/ios-swiftui.md`.

## 1. What it is

Not "blur with transparency": a material that **bends light (lensing)**, picks up color from what's behind, has specular highlights that react (to motion on iOS; at least to touch/scroll elsewhere), and materializes by modulating refraction rather than a plain alpha fade. A static, flat blurred panel is not this material — use real optics where the platform offers them.

## 2. Where it is allowed

- **Control layer only:** navigation bars, toolbars, tab bars, floating buttons, docks, menus, the chrome of sheets.
- **Never on content:** lists, data cards, tables, body text, media. Content gets solid or lightly tinted, unblurred surfaces.
- **Never glass on glass:** a glass sheet over a glass toolbar, a glass button inside a glass card. Nearby controls that belong together merge into **one** glass object (SwiftUI `GlassEffectContainer`, Haze `hazeGlassContainer`) instead of stacking.

## 3. Tint

A semantic accent for the primary action, not a decoration on everything. Primary CTA may carry a clear accent tint; secondary actions use neutral, more transparent glass.

## 4. Readability first (the iOS 27 lesson)

iOS 26's first version was criticized as too transparent. iOS 27 answered with: a **less transparent default**, **better diffusion of busy backgrounds**, a **darkened edge** around glass for separation, **brighter highlights**, and a user-adjustable Clear ↔ Tinted slider. When a glass surface looks weak or unreadable, move in that direction — not "more transparent".

- Text on glass: prefer the denser variant (Haze `GlassStyle.regular`, SwiftUI `.regular`). The clearer variant only for controls over photos/video, with a dimming layer when the content is bright.
- Check contrast against the product's **worst real backgrounds** (a photo, a white document, a dense list), not one flat color.

## 5. Concentricity

Inner and outer geometry agree: a capsule's radius and the radii of buttons inside it follow one progression (outer = inner + padding), not unrelated numbers.

## 6. System settings it must respect

1. **Reduce Transparency** → more opaque, matte.
2. **Increase Contrast** → high-contrast edge, near black/white.
3. **Reduce Motion** → no elastic/animated material behavior.

iOS applies these to native glass automatically. Android and web do not — wire them explicitly (Haze `GlassAccessibilitySettings`; CSS `prefers-reduced-transparency`, `prefers-contrast`, `prefers-reduced-motion`) and offer an in-app setting where no system signal exists.

## 7. Fallback

Every glass surface needs a fallback that stays readable when the renderer can't do blur/refraction (old Android, unsupported browsers, reduced transparency). Never make meaning depend on refraction or chromatic aberration alone.

## 8. Cost

Blur/refraction is GPU work. Keep it to a few chrome surfaces, measure first appearance and scrolling on a mid-range device, avoid glass inside long scrolling lists.
