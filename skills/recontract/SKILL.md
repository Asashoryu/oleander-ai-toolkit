---
name: recontract
description: Build or reorganise a whole contract tree. Creates all contracts at once from existing docs and code, or moves, merges and splits contracts and changes abstraction levels, after grilling the user on the proposal. Use for structural changes to contracts, not for editing a few of them.
---

# Recontract

Changes the **structure** of the contract tree: which levels exist, which contracts exist, where they sit and what they target. For changing the content of a few contracts during normal work, use `contract-refine`.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Contract format** section is binding. If there is no workspace, tell the user to run `contract-init` and stop.

## 1. Survey

Read, within the contracted domain:
- the existing contract tree, if any
- the existing documentation listed in the configuration
- the code: structure, entry points, module boundaries

## 2. Draft a proposal

Propose, without writing anything yet:
- **Levels**: number and names, from the coarsest (`0-…`, one root contract describing the whole system) down to the finest that is still useful. Choose them from the project's natural boundaries, not from a fixed scheme.
- **Contracts per level**: id, one-line purpose, parent, targets.
- **Coverage**: every path in the contracted domain must be a target of some leaf contract. List anything left uncovered.
- **Moves** (when reorganising): for each existing contract, whether it is kept, moved, merged, split or removed, and which clauses go where.

Prefer as few levels and contracts as will do. A contract that only restates its parent is not worth having.

## 3. Grill the proposal

Invoke the `grilling` skill on the proposal. Settle levels first, then the contracts within each level top-down. Do not write until the user confirms the structure.

## 4. Write

- Create the level folders and contract files following the contract format.
- Write clauses from what the docs and code actually say. Where the two disagree, write what the user decided in the grilling and note the disagreement in the contract's context, so the parity check will raise it as a ticket.
- When reorganising: keep the IDs of clauses that survive, update every `parent`, `targets` and `realises` that pointed to a moved contract, and set every open ticket on a removed or rewritten clause to `obsolete` with a log line.
- Add the levels to the workspace README's **Configuration**.

## 5. Hand over

List the contracts created or changed. The next step is a parity check on each changed subtree.
