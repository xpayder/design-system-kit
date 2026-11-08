# Platform guide — Android / Kotlin / Jetpack Compose

How the universal principles in `../SKILL.md` become Compose code. Read the project's `DESIGN_SYSTEM.md` first; its token and component names win over the examples here.

## 1. Tokens in Compose

- Primitives in one file (`object SpaceScale`, `object RadiusScale`, raw colors), semantic roles in another (`SemanticColors` exposed through a `CompositionLocal`, e.g. `AppDesign.colors`), type roles in a `Typography`/`AppTypography` object. Screens read only semantic/component tokens.
- Text sizes in `sp` always, spacing/shapes in `dp`. No `Color(0xFF…)`, `16.dp`, `20.sp` inline in a screen once tokens exist.
- Bundle fonts in `res/font` (works offline, no Play Services font provider) unless the profile says otherwise.
- Theme check: the project's own dark-theme flag, else `isSystemInDarkTheme()`. Verify both themes on every changed screen.

## 2. Construction rules → Compose

1. **One transition owner:** a single `AnimatedContent(targetState = screen) { … }` with `fadeIn() togetherWith fadeOut()` (or an explicit slide) per navigation level, or the Navigation component's own transitions — never two layers each fading their own content.
2. **Mutually exclusive floating UI = one state:** `enum class Overlay { None, Offer, Share }` and an exhaustive `when` inside one `Column`/slot — not independent `if (a) Box {…}`, `if (b) Box {…}`.
3. **Reserved space:** `SnackbarHost` and lists get `contentPadding`/`windowInsets` equal to the measured dock height plus `WindowInsets.navigationBars`; top bars float over content padded by `WindowInsets.statusBars` + bar height.
4. **Shared components:** one `AppTextField`, one button family (`PrimaryButton`, `SecondaryButton`), one top bar — reuse, don't fork per screen.
5. **RTL:** `padding(start=, end=)`, `Alignment.CenterStart/End`, `AutoMirrored` icons for direction-bearing glyphs; never `left/right` or raw `Offset(x, …)` for anything that must mirror. Check with `LayoutDirection.Rtl` previews and a real RTL locale.
6. **Animate only `graphicsLayer`** (`translationX/Y`, `scaleX/Y`, `alpha`) in scroll/gesture paths; no animated `width`/`height` dp.
7. **Springs:** `spring(dampingRatio = Spring.DampingRatioNoBouncy…LowBouncy, stiffness = Spring.StiffnessMedium)`; pressed feedback `scale ≈ 0.98f`.
8. **Touch targets:** 48×48dp minimum (`Modifier.minimumInteractiveComponentSize()` or explicit size), measured on the tappable area, not the icon.

## 3. Glass and blur with Haze (`dev.chrisbanes.haze`) — current: 2.1.0 (2026-11-02)

Principles (control layer only, no glass on glass, fallback must stay readable) are in `../references/glass-and-translucency.md`. API below is Haze **2.1.0**; check `https://github.com/chrisbanes/haze/releases` before upgrading — 2.x moves fast.

```kotlin
// build.gradle.kts — keep all Haze artifacts on one version
implementation("dev.chrisbanes.haze:haze:2.1.0")
implementation("dev.chrisbanes.haze:haze-blur:2.1.0")        // blur effect
implementation("dev.chrisbanes.haze:haze-glass:2.1.0")       // glass effect (stable since 2.1.0)
implementation("dev.chrisbanes.haze:haze-glass-material3:2.1.0") // optional: theme surface colors
```

Source and effect:

```kotlin
val hazeState = rememberHazeState()
Box {
  LazyColumn(Modifier.hazeSource(hazeState)) { /* content layer — no glass here */ }
  TopBar(Modifier.hazeGlass(input = HazeInput.Sources(hazeState)))   // control layer
}
```

- `HazeInput.Sources(state)` samples registered `hazeSource`s; `HazeInput.Backdrop(state)` samples what's behind the surface. Plain blur is `Modifier.hazeBlur(input = …)`.
- Styles: `GlassStyle.regular` (default; use when text sits on the glass) and `GlassStyle.clear` (keeps more background — controls over photos/video; add your own dimming for contrast). Material colors via `GlassStyle.regular.material3()`.
- **Remember styles** — `GlassStyle`/`HazeBlurStyle { }` compare by identity since 2.1.0: `val style = remember { GlassStyle.regular.then { shape(RoundedCornerShape(20.dp)) } }`. Hoist shared styles into the token layer (one `GlassTokens` object) instead of building them per call site.
- Optics: start from `GlassOptics.regular.copy(refractionStrength = …, refractionFoldStrength = …)` or `optics { copy(...) }` inside a style. Removed in 2.1.0: `GlassDefaults.optics`, the parameter-based `optics(...)` overload, `GlassStyle.Material3()` (use `material3()`); destructuring `GlassOptics`/`GlassAccessibilitySettings` no longer compiles; `GlassDefaults.positionAnimationSpec` → `GlassDefaults.interactionPositionAnimationSpec`.
- Useful knobs: `tint`, `specularIntensity`, `edgeShadow` (the darkened rim iOS 27 added — keep it, it separates glass from busy backgrounds), `ambientResponse`, `edgeSoftness`, `shape`, `surfaceProfile`, `lightPosition` (use logical `Alignment.CenterStart/End` so it mirrors in RTL), `chromaticAberrationStrength` (keep 0.1–0.25 at most).
- **Containers (new in 2.1.0):** `Modifier.hazeGlassContainer(mergeDistance = 16.dp)` around a row of glass controls makes them read as one object (toolbar, segmented control) and animates members joining/leaving. Costly in dense scrolling lists — measure.
- **Interaction:** visual only; pass the same `MutableInteractionSource` to `clickable`/`focusable` and `hazeGlass(interactionSource = …)`, define `pressed { scale(0.98f) }` etc. in the style, and set `interactionReducedMotionPolicy = GlassReducedMotionPolicy.System`.
- **Accessibility:** Haze does not read system settings. Provide `LocalGlassAccessibilitySettings provides GlassAccessibilitySettings(reduceTransparency = …, increaseContrast = …, showBorders = …)` at theme level, fed from the app's own setting and `AccessibilityManager`/high-text-contrast where available.
- **Fallbacks:** one style for every renderer; fallback drops refraction, chromatic aberration and progressive optics. Never carry meaning in refraction alone. Older Android (12/12L) uses fallback paths — check one real low-end device.
- **Performance:** `HazePerformanceMode.Default` first; measure first appearance and interaction separately; `HazeInputSharing` is experimental (less repeated work, more GPU memory).
- Upcoming (main branch, unreleased at 2.1.0): `ContinuousRoundedCornerShape`, `rimHighlight(...)`, `edgeOutline(...)`, scale up to 1.2f. Don't use until released.

## 4. Accessibility specifics (Android)

- Contrast computed from final ARGB, including glass alpha over the app's worst real backgrounds (`../references/accessibility.md`).
- TalkBack: `contentDescription` on icon-only buttons, localized in every locale; decorative layers `contentDescription = null` / `semantics { invisibleToUser() }`; traversal order matches visual order (floating capsules often break it — check with `isTraversalGroup`/`traversalIndex`); toasts/errors `liveRegion = LiveRegionMode.Polite`; dialogs move focus inside and back to the trigger.
- Reduced motion: honour animator duration scale 0 (`Settings.Global.ANIMATOR_DURATION_SCALE`) — transitions become instant, not just faster.
- Font scale: test 130% and 200%; text may wrap, never clip or overlap.
- External keyboard / D-pad: modals trap focus.

## 5. Locales

`res/values/strings.xml` is the base; every `values-*/strings.xml` has exactly the same keys (the plugin's hook checks this after each edit). `values-ar`, `values-iw`, `values-fa`, `values-ur` are RTL. Placeholders (`%1$s`) must match across locales.

## 6. Getting the app on screen and looking at it

- Devices: `adb devices -l`. If more than one, ask which to use.
- Build/install: `./gradlew installDebug` (or the project's own task from the profile).
- Stills: `adb -s <serial> exec-out screencap -p > shot.png` — native resolution; open it as an image.
- Recording: `adb -s <serial> shell screenrecord --time-limit 180 /sdcard/qa.mp4 && adb -s <serial> pull /sdcard/qa.mp4`, then contact sheets per `../references/visual-review-methodology.md`. Turn "Show taps" off first.
- **Navigation without pixel guessing:** `python3 <plugin>/skills/design-system/scripts/ui_nav.py` reads `uiautomator dump` and taps elements by text / content-desc / resource-id:
  ```bash
  ui_nav.py find "=OK" --serial S            # list matches first when a label may be ambiguous
  ui_nav.py tap "Continue" --serial S
  ui_nav.py scroll-to "Settings" --serial S --tap
  ui_nav.py wait-idle --serial S             # wait out a transition instead of sleeping
  ui_nav.py screenshot shot.png --serial S
  ```
  `--role desc` reaches icon-only buttons. Standard library + `adb` only.
- Compose previews (`@Preview` with `uiMode` night and `locale = "ar"`) are a fast first look, never the final verification.

## 7. Verify

`./gradlew compileDebugKotlin`, `./gradlew testDebugUnitTest`, lint if configured (`./gradlew lintDebug`), plus locale parity. Redirect output to a file and grep for `e: |error:|FAILED` instead of printing it. `/ds-verify` does this automatically.
