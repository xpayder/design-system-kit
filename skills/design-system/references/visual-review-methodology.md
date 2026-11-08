# Visual Review Methodology (no OCR/coordinate shortcuts)

This is a concrete, repeatable procedure. Follow it literally when reviewing any screen recording or batch of screenshots — whether from the user or from the agent's own build after a code change.

## 0. Core principle

Every judgment of the form "this is wrong" / "this is fine" / "this got better" must come from the model actually looking at an image — shape, color, transparency, layering, clipping, rhythm. A script that pulls text bounding boxes via OCR and reasons only from coordinates is NOT visual analysis and does not substitute for it. Such scripts are fine as a navigation aid (e.g. finding a button's coordinates to tap it in a UI test) but never as the basis for judging design quality.

## 1. Extracting frames from video

If the input is a screen recording (`.mp4`/`.mov` — device, simulator, or browser):

1. Get duration and resolution:
   ```bash
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 input.mp4
   ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=noprint_wrappers=1 input.mp4
   ```
2. First pass, broad: it isn't necessary (or affordable) to look at every single frame individually. Build "contact sheets" — a grid of downscaled frames at regular intervals (2–3 seconds is enough for most UI; go denser wherever the recording shows an active animation/transition):
   ```bash
   ffmpeg -y -i input.mp4 -vf "fps=1/3,scale=270:585,tile=4x4" -q:v 3 sheet_%03d.jpg
   ```
   Pick `scale` so the tiled result stays around 1080×2340 for a vertical phone recording (for a 1440-wide desktop browser recording use e.g. `scale=480:-1,tile=3x3`).

   **Prefer scene-change detection over a fixed interval when available** . A fixed interval can straddle a transition entirely — a double-render defect that only exists for a fraction of a second between two samples is invisible to fixed sampling no matter how dense, short of sampling every single frame. Scene detection instead captures every visually distinct moment individually, however brief:
   ```bash
   ffmpeg -y -i input.mp4 -vf "select='gt(scene,0.12)',showinfo" -vsync vfr -qscale:v 2 frame_%04d.png 2>scenes_log.txt
   grep -oP "pts_time:\K[0-9.]+" scenes_log.txt > times.txt
   ```
   This produces one native-resolution PNG per detected visual change, with exact timestamps — every transition moment gets its own frame, so single-frame ghosting is no longer a matter of luck to catch. Use this as the primary broad pass when reviewing anything involving navigation/transitions; fall back to fixed-interval sampling only where scene detection over- or under-fires (e.g. a screen with continuous animation that never settles, which triggers on every frame).
3. **Open every contact sheet as an image and actually look at it.** Don't skip any. The goal on this pass is to find *candidates* for problems: overlaps, clipping, style mismatches, odd shadows/smears, unreadable text.
4. **A second, precise pass is mandatory for every candidate.** A contact sheet is compressed and downscaled, so it's easy to both miss a real defect and "see" one that isn't there (a JPEG artifact, downscale moiré). For every suspicious moment, pull the frame(s) around that timestamp at the recording's native resolution:
   ```bash
   ffmpeg -y -ss <time-1s> -i input.mp4 -frames:v 1 -q:v 2 -update 1 zoom_a.png
   ffmpeg -y -ss <time>    -i input.mp4 -frames:v 1 -q:v 2 -update 1 zoom_b.png
   ffmpeg -y -ss <time+1s> -i input.mp4 -frames:v 1 -q:v 2 -update 1 zoom_c.png
   ```
   Grab 2–3 frames around the suspicious moment (transitions/animations span more than one frame), open each, and look carefully. Only then decide whether it's a real defect.
5. A candidate that isn't confirmed at native resolution **does not count as a defect** and doesn't go into further work. In practice, a meaningful share of contact-sheet "findings" turn out to be compression artifacts once checked at full resolution — that's expected; don't hesitate to discard them.

## 2. What to actually look at in each frame (category checklist)

When reviewing a frame, don't just "read the text on screen" — judge the design itself:

- **Compositing/z-order.** Is more than one screen state visible at once — a "ghost" duplicate of text/buttons overlapping the current screen? This is almost always a transition bug (see the construction rules in `SKILL.md`).
- **Clipping by system chrome.** Does content run under the status bar, nav bar, gesture area, notch/safe area, or a sticky browser header?
- **Glass/blur quality.** Is the blur smooth, free of smearing/double content while scrolling behind it; do highlight, edge, radius and tint match the product's other glass surfaces (one style, not "close enough")?
- **Spacing and alignment.** Consistent rhythm between cards/sections; nothing sticking to the screen edge without clear intent.
- **Overlap of interactive elements.** A snackbar/toast/badge must never sit on top of a button; two independent floating blocks must never render in the same area simultaneously.
- **Contrast and readability.** Text over glass/photo content must stay readable in both themes.
- **RTL.** For RTL locales — highlights, chevrons, docks and progress must mirror correctly.
- **Responsive (web).** Nothing overflows horizontally at 390px; no awkward single-word lines; no layout shift as fonts/images load.
- **Don't confuse this with recording artifacts.** A small dot/cursor that moves independently of any UI element (not anchored to anything) is almost certainly the system tap-visualization indicator ("Show taps" in Android Developer Options, or a recorder's click highlight) — not an app defect. It's fine to note once that this setting should be off for the next recording, but it's not a bug to file.

## 3. Self-check after the agent's own code changes

The same procedure applies not only to a user-provided video but to every meaningful visual change the agent itself makes:

1. Build and capture the current screen:
   - Android: `adb exec-out screencap -p > after_fix.png`
   - iOS Simulator: `xcrun simctl io booted screenshot after_fix.png`
   - Web: the in-app browser's screenshot, or `npx playwright screenshot --viewport-size=390,844 <url> after_fix.png` (and 1440×900)
   Previews (Compose `@Preview`, SwiftUI previews, Storybook) are a quick first look, not the final check.
2. Open `after_fix.png` as an image and actually look at it.
3. Compare it against how that screen looked before the change (keep the "before" screenshot in view for comparison) and against the project's token/glass targets (`DESIGN_SYSTEM.md`).
4. If the result doesn't actually read as clean and consistent with the rest of the product — by eye, not by "the code exists so it must work" — refine it rather than closing the task because it compiled.
5. Only once the visual result is genuinely satisfactory, move on to the formal verification (`/ds-verify`).

## 4. Working-notes format during a review

For a long recording, keep a short running list of candidates with timestamps during the first pass, e.g.:

```
~00:38 — possible double-render on step 1 → step 2 transition, verify at native resolution
~02:41 — possible clipping under the status bar on the limits screen, verify
~02:41 — toast appears to overlap the primary button, verify across adjacent frames (more than one frame?)
```

After the second pass, mark each "confirmed" or "not confirmed — compression artifact," and only carry confirmed items into code work (`SKILL.md` §3).
