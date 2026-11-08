# Agent Memory Architecture (projectmem + Repowise)

Applies when the project uses **projectmem** (event log, MCP tools) and/or **Repowise** (code index). Without them, keep the same three layers in plain files: rules in `CLAUDE.md`/`DESIGN_SYSTEM.md`, working notes in `memory/YYYY-MM-DD.md`, decisions in `docs/adr/`.

The three-layer split below is borrowed as a *conceptual model* from [TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory). That project itself is **not installed**: it is a Docker service with a proxy in front of Claude Code and needs paid LLM API keys, so it was deliberately skipped. Do not describe it as active.

---

## 1. Memory Layering Architecture (TencentDB Model)

Following TencentDB-Agent-Memory architecture, agent context is structured in three strictly separated layers:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CORE MEMORY (Persistent / Soul & Rules)                  │
│    - SOUL.md, USER.md, AGENTS.md, skill instructions        │
│    - Non-negotiable project laws & construction constraints │
├─────────────────────────────────────────────────────────────┤
│ 2. WORKING MEMORY (Session & Operational)                   │
│    - Active conversation state, scratchpad, git diffs       │
│    - Daily notes: memory/YYYY-MM-DD.md                      │
├─────────────────────────────────────────────────────────────┤
│ 3. KNOWLEDGE BASE & LONG-TERM PERSISTENCE (projectmem / MCP)│
│    - Structured event log: .projectmem/events.jsonl         │
│    - Automated summaries: .projectmem/summary.md            │
│    - Curated wisdom: MEMORY.md                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Projectmem Session Startup (MANDATORY)

At the start of **any** session or task, if projectmem is installed for this project, call these three MCP tools in sequence before answering or modifying code:

1. **`get_instructions()`**: Loads mandatory project logging rules and event types.
2. **`get_summary()`**: Loads the current architectural state, decisions, and known active issues. Costs **~500 tokens** vs **~5,000+ tokens** to re-scan files.
3. **`get_project_map()`**: Loads structural package layout and key modules.

---

## 3. During-Work Logging Protocols

Never edit `.projectmem/summary.md` or `.projectmem/PROJECT_MAP.md` directly via filesystem writes. Always use the MCP write tools:

* **Bug Discovery:** Call `log_issue(summary, location)` when a bug is identified.
* **Fix Attempt:** Call `record_attempt(summary, outcome)` after trying a resolution.
* **Confirmed Resolution:** Call `record_fix(summary, issue_id?)` once verified via tests and visual audit.
* **Architectural Decisions:** Call `add_decision(summary)`.
  * *Superseding decisions:* When replacing an older decision, supply `supersedes="<old_event_id>"`. This keeps the log append-only while pruning obsolete guidance from `summary.md`.
* **Gotchas / Environment quirks:** Call `add_note(summary)`.
* **File Precheck:** Call `precheck_file(path)` before modifying any file to review its failure/fix history.

---

## 4. Continuity & Knowledge Hygiene

1. **Text > Brain:** Mental notes do not survive session restarts. Commit critical insights to projectmem or `memory/YYYY-MM-DD.md`.
2. **Never leak secrets or credentials:** Keep sensitive user context out of general commit logs.
3. **Audit Trails:** Keep bug descriptions focused on symptoms and root causes, avoiding vague notes.
