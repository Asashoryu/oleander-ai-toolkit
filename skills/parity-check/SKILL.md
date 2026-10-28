---
name: parity-check
description: Verify contract clauses against their targets (child contracts, code, other resources) using each clause's verification method, list every discrepancy and uncontracted zone, and open tickets on request. Use after contracts or code change, or to check whether a project is stable.
---

# Parity check

Finds where contracts and their targets disagree. It never fixes anything and never decides alone: it lists, and opens tickets only when asked.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Contract format** and **Ticket format** sections are binding.

## 1. Decide the scope

The scope is given by whoever invokes the check:
- contracts that changed
- files that changed, mapped to the contracts that target them
- contracts or paths the user names

Extend it with the subtrees below those contracts and their ancestors up to the root. Check the whole tree only when the user asks for it. Never check a contract outside the scope just because it exists.

## 2. Verify each clause

For every clause of every contract in scope, apply its `verify:` method:

| Method | What to do | Passes when |
|---|---|---|
| `inspection` | Read the targets that realise the clause. | You can cite the path and lines that make it true. If you cannot point to them, it fails. |
| `test` | Find the verification contract covering this clause, then run its tests. | A verification contract names a test for this clause and the test passes. A missing verification contract or test is a discrepancy. |
| `static` | Run the named tool and rule. | The tool reports no violation. |
| `command` | Run the command. | The result matches the one written in the clause. |
| `review` | Nothing to run. | Never judged: list it as "needs review". |

Also check, for each contract in scope:
- **Parent ↔ child**: every parent clause is realised by at least one child (`realises`), no child clause contradicts a parent clause, and every minimum verification method the parent imposes is respected.
- **Targets**: every target path exists.
- **Uncontracted zones**: every path in the contracted domain within scope is targeted by some contract. Excluded paths are not reported.

A clause cares only about what it states. Do not raise lower-level imperfections against a coarse clause unless they break that statement.

## 3. Report

Answer with:

1. **Discrepancies**, each with contract and clause, the conflicting parts (contract text and the target with path and line), the method used and its result, and a proposed direction: `code` (the target must change), `contract` (the clause is wrong or outdated) or `escalate` (the problem is decided higher in the tree). Skip anything already covered by an open ticket.
2. **Uncontracted zones** found, each with a proposal for which contract should cover it (an existing one or a new one).
3. **Needs review**: `review` clauses in scope.
4. A one-line summary: clauses checked, passed, failed.

Then, unless the invoker asked for a report only, ask which discrepancies to open as tickets, and whether to change any direction.

## 4. Open tickets

Only when asked, and only for the discrepancies chosen: create `tickets/T-<nnnn>-<slug>.md` following the ticket format, numbering from the highest existing ID. Status `open`, log line `<date> · parity-check · opened`.

If a full check finds no discrepancies, the project is **stable**.
