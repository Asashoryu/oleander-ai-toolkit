---
name: recontract
description: Build or reorganise a contract tree. Creates the tree from requirements and existing documents when there is no code yet, or moves, merges, splits and re-nests contracts and adds abstraction levels, after grilling the user on the proposal. Use for structural changes to contracts; to contract existing code, use contract-reverse.
---

# Recontract

Changes the **structure** of the contract tree: which contracts exist, how they nest and what they target. Changing the content of a few contracts is out of scope; documenting existing code is the job of reverse contracting.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Contract tree**, **Contract format** and **Verification** sections are binding. If there is no workspace, say so and stop.

If the request is to document code that exists but has no contracts, say that this is reverse contracting and stop.

## 1. Survey

Read:
- the existing contract tree, if any
- the existing documentation listed in the configuration
- the requirements the user gives
- the code structure, if any (to place targets, not to document it)

## 2. Draft a proposal

Propose, without writing anything yet:
- **Tree**: the contracts as an indented list of IDs, each with a one-line purpose and its targets (planned files for code that does not exist yet). Nest where a reader would want to study a part separately.
- **New levels**: for every contract that has grown too large (see the README), the overview it keeps and the children that take the detail.
- **Constraints**: for each contract, its main constraints, each with the kind of verification (`script` or `check`). A constraint that cannot be verified is reworded or dropped.
- **Moves** (when reorganising): for each existing contract, whether it is kept, moved, merged, split or removed, and where each constraint goes.
- **Coverage**: every existing file in the contracted domain and the contract that will target it.

A contract that only restates its parent is not worth having; a contract too long to read in one go is not either.

## 3. Grill the proposal

Invoke the `grilling` skill on the proposal. Settle the top of the tree first, then each branch downwards. For a new project, grill until every contract has enough to be written in full: purpose, how it should work, interface, errors, configuration. Do not write until the user confirms.

## 4. Write

- Create or move the contract files following the contract format and its writing rules. Write each contract in full, with tables and diagrams, not as a list of headings: a thin contract is a defect.
- Create the verification file for every new constraint in the tests folder. Scripts for code that does not exist yet will fail; that is expected and becomes a ticket.
- When reorganising: keep the IDs of surviving constraints, move their verification files with them, and update every `targets`, `realises` and ticket that refers to a moved or renamed contract. Set every open ticket on a removed constraint to `obsolete`, with a log line.

## 5. Hand over

List the contracts and verifications created, moved or removed.
