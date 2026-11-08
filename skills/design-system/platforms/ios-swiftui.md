# Platform guide — iOS / SwiftUI (and UIKit)

How the universal principles in `../SKILL.md` become SwiftUI code. Read the project's `DESIGN_SYSTEM.md` first. For the full Liquid Glass API surface (modifiers, containers, morphing, button styles), load the `liquid-glass-reference` skill.

## 1. Tokens in SwiftUI

- Semantic colors in the asset catalog (Any/Dark appearances, High Contrast variants) or a `Color` extension backed by them; spacing/radius scales as `enum Space { static let s4: CGFloat = 16 }`.
- Typography via text styles (`.font(.title2)`, or custom fonts with `Font.custom(_, size:, relativeTo:)`) so Dynamic Type scales them. No fixed point sizes on body text.
- One `ButtonStyle` / `LabelStyle` family per product, reused everywhere.

## 2. Construction rules → SwiftUI

1. **One transition owner:** navigation through `NavigationStack`/one container; `.transition` + `withAnimation` from one place per state change.
2. **Mutually exclusive overlays = one state:** an `enum Overlay` driving a single `.overlay`/`.sheet(item:)`, not several `isPresented` booleans that can all be true.
3. **Safe areas:** floating bars use `.safeAreaInset(edge:)` so scroll content is padded automatically; don't hard-code bar heights.
4. **Shared components:** one style per control type; no copies with slightly different padding.
5. **RTL:** `.leading/.trailing` everywhere; SF Symbols mirror automatically where meaningful — check custom images with `.flipsForRightToLeftLayoutDirection(true)` only when direction-bearing.
6. **Animations:** springs (`.spring(duration: 0.35, bounce: 0.1)`), transform/opacity; respect `@Environment(\.accessibilityReduceMotion)`.
7. **Targets:** 44×44pt minimum (HIG). Not 48dp — that's Android.

## 3. Liquid Glass (iOS 26+, refined in iOS 27)

Principles in `../references/glass-and-translucency.md`. API essentials: `.glassEffect(_:in:)` with `.regular`/`.clear`, `.tint(...)`, `.interactive()`; group nearby glass in `GlassEffectContainer` so it blends and morphs (`glassEffectID` + namespace); standard bars, tab bars and sheets adopt glass automatically — don't re-skin them. Respect Reduce Transparency / Increase Contrast / Reduce Motion (the system adapts native glass; custom effects must check `accessibilityReduceTransparency` etc.). Deployment target below 26 → provide a `.background(.regularMaterial)` fallback behind `if #available`.

## 4. Accessibility specifics (iOS)

VoiceOver labels on icon-only buttons (`.accessibilityLabel`), decorative views `.accessibilityHidden(true)`, grouping with `.accessibilityElement(children: .combine)`, announcements for async results; test Dynamic Type up to the largest accessibility sizes; Smart Invert and Increase Contrast checked visually.

## 5. Locales

String Catalogs (`Localizable.xcstrings`) — every key translated in every shipped language, plurals via the catalog, not string concatenation. RTL: Arabic/Hebrew run with `-AppleLanguages (ar)` scheme argument.

## 6. Getting the app on screen and looking at it

Simulator: `xcrun simctl io booted screenshot shot.png`; recording: `xcrun simctl io booted recordVideo qa.mov`. Use the iOS Simulator tool when available (screenshot + accessibility-tree inspect for navigation). Review frames per `../references/visual-review-methodology.md`. SwiftUI previews are a first look, never the final verification.

## 7. Verify

`xcodebuild -scheme <Scheme> -destination 'platform=iOS Simulator,name=<Device>' build test`, SwiftLint if configured, string catalog has no stale/missing entries.
