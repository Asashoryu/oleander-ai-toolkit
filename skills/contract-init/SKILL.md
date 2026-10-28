---
name: contract-init
description: Set up a contract-flow workspace in a project, with its contracts, tickets and handoff folders and a README explaining the flow and its configuration. Use when starting contract-flow in a new project or changing its configuration.
---

# Contract init

Sets up the workspace that the contract-flow skills share. It configures and explains the flow; it does not write contracts.

## 1. Look for an existing workspace

Check, in order:
1. A line `Contract-flow workspace: <path>` in the project's `CLAUDE.md` or `AGENTS.md`.
2. Any `README.md` containing `<!-- contract-flow-workspace -->`.

If one exists, show its configuration and ask whether to change it. Edit only the **Configuration** section, then stop.

## 2. Ask the setup questions

Explore the project first (folder structure, languages, existing docs) so every question comes with a concrete suggestion. Ask them together, numbered, each with your recommended answer:

1. **Workspace location.** Default: `docs/contract-flow/`.
2. **Contracted domain.** Which paths are governed by contracts, and which are explicitly excluded (generated code, vendored libraries…).
3. **Existing documentation.** List what you found (specs, ADRs, PRDs, issue or ticket folders…) and ask what each contains and whether it should later be absorbed into contracts or left alone. Never move or delete it here.

## 3. Create the workspace

```
<workspace>/
├── README.md      from templates/README.md, Configuration filled in
├── contracts/
├── tickets/
└── handoff/
```

Add `Contract-flow workspace: <workspace>` to the project's `CLAUDE.md` (create it if missing; also `AGENTS.md` if the project has one) so new sessions find it.

## 4. Hand over

Tell the user the workspace is ready and where it is.
