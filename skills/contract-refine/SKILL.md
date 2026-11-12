---
name: contract-refine
description: Change the content of a few contracts for a specific task (a new requirement, a correction, a contract or escalate ticket), after grilling the user on the change, keeping the documentation complete, with no grey zone, and every clause verified. Also brings a contract back to the template when it fails the lint, and fills gaps found by a parity check. Use whenever what a contract says, enforces or covers needs to change during normal work.
---

# Contract refine

Changes what a few contracts say. Reorganising the graph (moving, merging, splitting, changing which contracts a contract implements, adding levels) is out of scope.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Names**, **Contract format** (with **Verification** and **Lint**) sections are binding.

## Quotes

When you say what a contract says, use `contract-tools quote <contract>#<clause>` and paste its output; never paraphrase it or write it from memory. Look contracts up with `contract-tools find` and `which-contracts` (exit code 3 and `UNCONTRACTED ZONE` mean no contract covers it: stop, see **No contract covers it** in the contract-flow workflow). Names are words, never codes.

## 1. Understand the input

The input is one of:
- a **requirement** or statement from the user (new, changed or removed behaviour)
- one or more **tickets** with direction `contract`, `escalate` or status `rerouted`
- an outdated contract found to disagree with code that is right
- a contract that **fails the lint (`contract-tools lint`)**, or has a **gap** (something the enforced files do or expose that no clause covers), reported by a parity check

Find the contracts involved and read them with the files they enforce. For an `escalate` ticket, start from the contracts it `implements` and keep climbing through every parent while the problem is really decided higher up.

## 2. Grill the change

Invoke the `mattpocock-skills:grilling` skill. Settle, for each contract involved:
- what changes in the documentation (**Purpose**, **View**, **Notes**), not only in the clauses; for an off-template contract, which parts are missing or misplaced and what goes there
- which clauses are added, reworded or removed, and how each is verified (type from the closed list)
- that no grey zone remains: every responsibility, input, output, error and configuration at this level has a clause or is declared out of the contract
- whether the contracts it enforces, and the ones that implement it, must change too (list them), and whether a clause shared by several contracts (security, quality) should be changed once in its own contract
- whether the contract becomes too large and needs a new level, or the change is otherwise structural: then stop and say so

Work from the highest affected contract downwards, through every parent branch. Do not write until the user confirms.

## 3. Write

- Edit the contracts following the contract format and its writing rules: update the prose, tables and diagrams so the contract still documents the files it enforces completely, mostly through diagrams and tables, in simple words. A contract that was off-template is rewritten into the template (fixed header, then Purpose, View, Clauses, Verification, Notes), proposing a name for every clause and getting it confirmed. Never rename a surviving clause without updating every reference to it.
- **Structured parts go through `contract-tools`, never by hand**: `clause add|rename|remove`, `edge`, `files`, `root`, `contract new|rename`. You write only the prose (Purpose, View, Notes). A clause added for a gap is created with `clause add ... --ticket <name>`, which makes a stub verification that fails and opens its ticket at once. Write the real verification into the stub afterwards.
- Keep the `covered-by` rows of the parents of any clause you changed correct (`clause add` on the parent, or `clause remove` and add).
- Run `contract-tools lint` (see **Lint** in the README); it rewrites the links blocks and `INDEX.md`. Do not finish while a contract you touched fails it. Add each contract you changed to the scope: `contract-tools scope add <id>`. A contract written in an older format (`realizes`, nested folders) fails the lint: bring it to the current template, and flag a move out of a subfolder to the user.
- Show the clauses you change as quotes (`contract-tools quote`) before and after the change.
- For each input ticket, use `contract-tools ticket log` to say what changed. If the contract change removes the discrepancy, `ticket status <id> resolved`; if the clause is now right and the code must follow, `ticket reopen` then `ticket direction <id> code`. `ticket sweep` closes tickets whose clause no longer exists.

## 4. Hand over

List the contracts and verifications changed.
