---
name: contract-init
description: Set up a contract-flow workspace in a project, with its contracts, tickets and handoff folders, a tests folder for verifications and the contract lint, and a README explaining the flow, the contract format and the configuration. Also updates an existing workspace to the current tool and README after the toolkit changed. Use when starting contract-flow in a new project, changing its configuration, or bringing an older workspace up to date.
---

# Contract init

Sets up the workspace that the contract-flow skills share. It configures and explains the flow; it does not write contracts.

## 1. Look for an existing workspace

Check, in order:
1. A line `Contract-flow workspace: <path>` in the project's `CLAUDE.md` or `AGENTS.md`.
2. Any `README.md` containing `<!-- contract-flow-workspace -->`.

If one exists, show its configuration and ask which of these the user wants, then do only that and stop:
- **Change the configuration**: edit only the **Configuration** section (and move folders if a location changed).
- **Update the workspace**: bring it to what the toolkit now ships, as in **Update an existing workspace** below. Offer this first when the tests folder has a `contract-lint.py`, has no `contract-tools.py`, or `contract-tools.py --version` is lower than the same command on `templates/contract-tools.py`.

## 2. Ask the setup questions

Explore the project first (folder structure, languages, build and test tools, existing docs) so every question comes with a concrete suggestion. Ask them together, numbered, each with your recommended answer. There are no defaults: every answer comes from the user.

1. **Workspace location.** Where contracts, tickets and handoffs go.
2. **Tests folder.** Where verification scripts and check files go: inside the workspace, or in the project's own test folder.
3. **Script runner.** How verification scripts are run, matching what the project already uses (e.g. `bash`, `pwsh`, `python`, `node`, `npm test --`). `contract-tools.py` is a Python script (`python3 -I`), so Python 3 is needed for it whatever the runner.
   **Extra verification types** and **hooks** (CI, pre-commit) where verifications should also run: ask, suggesting none if the project has neither.
4. **Contracted domain.** Which paths are governed by contracts, and which are excluded (generated code, vendored libraries, build output…).
5. **Existing documentation.** List what you found (specs, ADRs, PRDs, issue folders…) and ask what each contains and whether it should later be absorbed into contracts or left alone. Never move or delete it here.

## 3. Create the workspace

```
<workspace>/
├── README.md      from templates/README.md, Configuration filled in
├── contracts/     one folder, no subfolders
├── tickets/
└── handoff/
<tests folder>/    created if missing, with contract-tools.py copied from templates/
```

Copy `templates/contract-tools.py` into the tests folder. Fill the **Configuration** table exactly as the tool reads it: paths in backticks (folders end in `/`), the script runner as one command in backticks, `none` where nothing applies. Then run `python3 -I <tests folder>/contract-tools.py lint` from the project root to check the setup.

Add `Contract-flow workspace: <workspace>` to the project's `CLAUDE.md` (create it if missing; also `AGENTS.md` if the project has one) so new sessions find it.

## 4. Hand over

Tell the user the workspace is ready, where it and the tests folder are, and whether the project already has code (contracts are then best written from it) or not (contracts are written from requirements).

## Update an existing workspace

Brings a workspace made with an older toolkit to the current one. It never rewrites contracts, tickets or handoffs.

1. Read the **Configuration** table of the workspace `README.md`, and find the tests folder from it.
2. **Tool.** Copy `templates/contract-tools.py` over the tests folder's `contract-tools.py`. If the tests folder has the old `contract-lint.py`, tell the user and delete it once the new tool is in place.
3. **README.** Replace everything above and below the **Configuration** section with the current `templates/README.md`, keeping the values already in the table. Rewrite those values in the form the tool reads (paths in backticks, folders ending in `/`, the script runner as one command in backticks, `none` where nothing applies). For a setting the old table does not have, or whose value cannot be read (**Contracted domain**, **Script runner**), propose a value from the project and ask the user to confirm it, as in step 2 of the setup questions.
4. **Project files.** Check that `CLAUDE.md` (and `AGENTS.md` if it exists) still has the `Contract-flow workspace:` line.
5. **Check.** Run `python3 -I <tests folder>/contract-tools.py lint` from the project root and show the result. A contract or ticket in an older format will fail it: that is expected. Do not fix them here; list them and say that `/contract-flow` will route them to `contract-refine`, and the parity check will open the tickets.
6. **Hand over.** List what was replaced, what was kept, and the number of problems the lint found.
