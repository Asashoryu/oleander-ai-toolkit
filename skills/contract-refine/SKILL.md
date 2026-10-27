---
name: contract-refine
description: Change the content of a few contracts for a specific task (a new requirement, a contract or escalate ticket), after grilling the user on the change. Use whenever contract clauses or targets need to change during normal work.
---

# Contract refine

Changes what a few contracts say. For reorganising the tree (levels, moving or splitting contracts), use `recontract`.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Contract format** section is binding.

## 1. Understand the input

The input is one of:
- a **requirement** from the user (new, changed or removed behaviour)
- one or more **tickets** with direction `contract`, `escalate` or status `rerouted`

Find the contracts involved. For an `escalate` ticket, start from the parent of the ticket's contract and keep climbing while the problem is really decided higher up.

## 2. Grill the change

Invoke the `grilling` skill. Settle, for each contract involved:
- which clauses are added, reworded or removed
- whether children must change to keep realising their parent (list them)
- whether the change is really structural, in which case stop and suggest `recontract`

Work from the highest affected contract downwards. Do not write until the user confirms.

## 3. Write

- Edit the contracts following the contract format. Never renumber surviving clauses.
- Keep `targets` and `realises` accurate.
- For each input ticket, append a log line saying what changed, and set it to `resolved` if the contract change removes the discrepancy. Set to `obsolete` any other open ticket whose clause no longer exists.

## 4. Hand over

List the contracts changed. The next step is a scoped parity check on them.
