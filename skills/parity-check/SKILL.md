---
name: parity-check
description: Compare contracts with their targets (child contracts and code), report every discrepancy and, once the user confirms, open a ticket for each. Use after contracts or code change, or to check whether a project is stable.
---

# Parity check

Finds where contracts and their targets disagree. It never fixes anything: it reports, and opens tickets.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Contract format** and **Ticket format** sections are binding.

## 1. Decide the scope

Check only what a change can have affected:
- the contracts that changed (or that the user names)
- their subtrees, down to the code
- their ancestors, up to the root, to confirm the change still honours every parent

Check the whole tree only when the user asks for it, or to confirm the project is stable. Never re-check a contract outside the scope just because it exists.

## 2. Check each contract against its targets

For each contract in scope, and each clause:

- **Child contracts**: every clause of the parent must be realised by at least one child (`realises`), and no child clause may contradict a parent clause.
- **Code** (leaf contracts): find the code that realises the clause and check it does what the clause says. Read the code; run it or its tests only if they exist and the clause is about behaviour that reading cannot settle.
- **Coverage**: every target path must exist, and every path in the contracted domain within scope must be targeted by some leaf contract.

A higher-level clause cares only about what it states. Do not raise lower-level imperfections against it unless they break that statement.

## 3. Report

Present the discrepancies as a list, each with:
- contract and clause
- target
- what the clause requires vs what the target does, with evidence (paths, lines, quotes)
- a proposed direction: `code` (the target must change), `contract` (the clause is wrong or outdated) or `escalate` (the problem is decided at a higher level)

Skip anything already covered by an open ticket.

🛑 Ask the user to confirm the list and the directions. They can drop, merge or redirect items.

## 4. Open tickets

For each confirmed item, create `tickets/T-<nnnn>-<slug>.md` following the ticket format, numbering from the highest existing ID. Status `open`, log line `<date> · parity-check · opened`.

If nothing is found in scope, say so. If the check was a full one and found nothing, the project is **stable**.
