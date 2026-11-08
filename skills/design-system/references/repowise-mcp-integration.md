# Repowise MCP Integration & Codebase Intelligence

This guide establishes the mandatory rules and best practices for leveraging **Repowise MCP tools** on any project where Repowise is installed.

---

## 1. Why Repowise Matters (Token Efficiency & Structural Safety)

* **Drastic Token Savings:** Calling targeted Repowise tools (`get_context`, `get_symbol`, `search_codebase`) consumes **~200–500 tokens**, whereas reading entire source files blindly costs **5,000–15,000+ tokens** per file.
* **Architectural Awareness:** Repowise indexes call graphs, symbol dependencies, hotspot risk scores, and architectural rationale across the entire project.
* **Pre-Edit Safety:** Repowise detects bug magnets, test coverage deficits, and blast radius before any code modification is attempted.

---

## 2. Tool Reference & When to Call Each

| Tool | When & Why to Use |
|------|-------------------|
| `search_codebase(query, mode?)` | Fast hybrid search for symbols, paths, or architectural concepts across Kotlin & Python modules without reading entire directory trees. |
| `get_context(targets=[...])` | Primary triage card for files, classes, or symbols. Returns docstrings, public signatures, bug fix history, and callers/callees without source bytes. |
| `get_symbol(id, depth?)` | Retrieves the exact verified body of a specific symbol/function (e.g. `AppTextFieldKt::AppTextField`) identified by a previous tool, saving full-file reads. |
| `get_change_risk(revspec?)` | Deterministic git-diff safety analysis. Returns percentile risk, impacted call chains, and testing recommendations before staging/committing. |
| `get_risk(targets=[...])` | Evaluates file-level structural blast radius and bug-magnet history for specific files — ask it for this project's own hotspots, don't assume which files they are. |
| `get_why(query, targets?)` | Queries documented architectural decisions and git rationale. Call before refactoring established patterns. |
| `get_health(targets?)` | Self-checks defect density, maintainability, and code smells on modified files. |
| `get_dead_code(safe_only?)` | Detects unused composables, dead functions, and obsolete imports during refactor/cleanup passes. |
| `get_overview()` | Returns the global architectural blueprint of the project. |

---

## 3. Mandatory Repowise Workflow Rules

1. **Query Before Blind Read:** When locating where a feature, composable, or business rule lives, start with `search_codebase` or `get_context`, not broad ripgrep searches or full-file inspections.
2. **Follow-up with `get_symbol`:** If you only need to inspect a specific composable or helper function inside a large 500+ line file (e.g. `PdfEditorSheet.kt`), call `get_symbol` rather than loading the whole file into context.
3. **Check Risk Before Modifying Hotspots:** This project has its own known "bug magnets" — find them with `get_risk`/`get_health` rather than assuming which files they are. Always run `get_risk` or `get_context` to review past fix history before making changes.
4. **Change-Risk Validation:** Before committing code to `feature/latest-updates`, check diff risk with `get_change_risk` to ensure no unintended call chains are broken.
