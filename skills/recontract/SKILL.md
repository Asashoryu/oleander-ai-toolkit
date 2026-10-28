---
name: recontract
description: Build or reorganise a whole contract tree. Creates all contracts at once from existing docs and code, or moves, merges, splits and re-nests contracts, after grilling the user on the proposal. Use for structural changes to contracts, not for editing a few of them.
---

# Recontract

Changes the **structure** of the contract tree: which contracts exist, how they nest and what they target. Changing the content of a few contracts is out of scope.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Contract format** section is binding. If there is no workspace, say so and stop.

## 1. Survey

Read, within the contracted domain:
- the existing contract tree, if any
- the existing documentation listed in the configuration
- the code: structure, entry points, module boundaries

## 2. Draft a proposal

Propose, without writing anything yet:
- **Tree**: the root contract (the whole system, coarse) and how it breaks down, as an indented list of contract IDs, each with a one-line purpose and its targets. Nest only where a part has responsibilities worth stating separately; branches can be as shallow or deep as the code needs.
- **Clauses**: for each contract, its main Ensures and Invariants, with the verification method you propose.
- **Verification contracts**: where clauses use `test`, the leaf contracts that will target the tests.
- **Uncontracted zones**: every path in the contracted domain that no contract would target. Propose a contract for each, or confirm it stays uncontracted.
- **Moves** (when reorganising): for each existing contract, whether it is kept, moved, merged, split or removed, and which clauses go where.

Prefer as few contracts as will do. A contract that only restates its parent is not worth having.

## 3. Grill the proposal

Invoke the `grilling` skill on the proposal. Settle the top of the tree first, then each branch downwards. Do not write until the user confirms.

## 4. Write

- Create the contract files and folders following the contract format.
- Write clauses from what the docs and code actually say. Where the two disagree, write what the user decided in the grilling and note the disagreement under **Decisions**.
- When reorganising: keep the IDs of clauses that survive, and update every `targets`, `realises` and ticket that refers to a moved or renamed contract. Set every open ticket on a removed or rewritten clause to `obsolete`, with a log line.

## 5. Hand over

List the contracts created or changed.
