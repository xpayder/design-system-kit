---
description: Capture the changed screens/flow (device, simulator or browser) and review the frames as images — the Visual-First Law
allowed-tools: Bash, Read
argument-hint: [flow or screen to audit] [duration-seconds]
---
Load the `design-system` skill and follow `references/visual-review-methodology.md`. Audit: $ARGUMENTS

1. **Capture**, by platform:
   - Android: pick the device (`adb devices -l`; ask if several), use the project's recording script if the profile names one, else `adb shell screenrecord --time-limit <secs> /sdcard/qa.mp4` + `adb pull`. Navigate with `skills/design-system/scripts/ui_nav.py`, never guessed coordinates.
   - iOS Simulator: `xcrun simctl io booted recordVideo qa.mov` / `screenshot`.
   - Web: production build or dev server; screenshots at 1440×900 and 390×844 (plus 768 if there's a tablet layout) through the in-app browser or Playwright; record interactions for transitions and menus.
   - Cover light and dark theme, one long-word locale, RTL if shipped, max text size for the changed screens.
2. **Review**: contact sheets / scene-change frames first, then native-resolution frames around every candidate. Open each as an image and judge compositing, clipping, glass quality, spacing, overlap, contrast, RTL, responsive layout. Never judge from OCR, DOM or accessibility-tree output.
3. **Report** confirmed defects with timestamps/frame names and severity (`references/design-review-rubric.md`), separately list what was not checked.
4. **Clean up**: delete recordings and extracted frames when the review is done.
