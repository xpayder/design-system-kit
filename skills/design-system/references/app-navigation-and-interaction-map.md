# App Navigation & Surface Interaction Map — method

**Purpose:** build a deterministic navigation blueprint of a project's destinations, modals/sheets, and test hooks, so automation and visual audits navigate by known route/element rather than blind OCR-coordinate guessing or expensive trial-and-error. This file has no routes in it on purpose — generate the project's own map once (e.g. `docs/NAVIGATION_MAP.md`) and keep it current.

## 1. Find the navigation source of truth

- Compose Navigation: a `sealed class`/enum of destinations (`*Destination.kt`, `*Routes.kt`) and the `NavHost` wiring — `grep -rl "NavHost(" app/src/main/java`.
- Web: the router — file-based routes (`app/`, `pages/`, `src/routes/`) or a route table (`createBrowserRouter`, `vue-router`, `routes.ts`).
- SwiftUI: `NavigationStack` paths, `TabView`, and `.sheet`/`.fullScreenCover` presenters.
- With Repowise installed, `search_codebase("NavHost")` / `search_codebase("router")` finds it faster.

## 2. Table 1 — top-level destinations

For each route, record: route name, screen composable, entry condition/trigger, and what back/next does. One row per destination; don't skip the ones that feel "obvious," they're exactly where an automated flow silently breaks.

| Route | Screen | Entry condition | Back / next |
|---|---|---|---|

## 3. Table 2 — modal sheets & system dialogs

Floating surfaces (bottom sheets, dialogs, pickers) that sit over a destination and must be accounted for separately, since they aren't a `NavHost` route:

| Sheet/dialog | Hosting screen / trigger | Dismissal | Key controls & states |
|---|---|---|---|

## 4. Golden-path journeys

Write out the 2-4 flows that matter most to the product (the core conversion/task flow, any multi-step wizard, any "resume where I left off" flow) as a numbered step list naming the exact route/action at each step — this is what both a human QA pass and `/ds-verify`-style automation follow instead of re-discovering the app each time.

## 5. Navigation invariants to record once found

- Where cross-screen state lives (single ViewModel? per-screen state hoisted to a shared one? SavedStateHandle?) and whether back-navigation preserves it.
- `launchSingleTop`/`popUpTo` usage for hub/entry routes, so repeated navigation doesn't pile up the back stack.
- Any "checkpoint"/resume mechanism mapping a saved state to a mid-flow route.
- Default transition (crossfade, slide, etc.) and any routes that deliberately differ from it.
