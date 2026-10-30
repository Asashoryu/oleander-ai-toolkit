---
name: parity-check
description: Verify contracts against their targets by running each constraint's verification script or check file, find every uncontracted file and thin contract, list every discrepancy, and open tickets on request. Use after contracts or code change, or to check whether a project is stable.
---

# Parity check

Finds where contracts and their targets disagree. It never fixes anything and never decides alone: it lists, and opens tickets only when asked.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Contract tree**, **Contract format**, **Verification** and **Ticket format** sections are binding.

## 1. Decide the scope

The scope is given by whoever invokes the check:
- contracts that changed
- files that changed, mapped to the contracts that target them
- contracts or paths the user names

Extend it with the subtrees below those contracts and the contracts they `realise`, up to the root. Check the whole tree only when asked.

## 2. Coverage (mechanical)

List every file in the scope's paths that is not excluded (`git ls-files` where possible) and every path in the `targets` of every contract (expanding folders). Compare the two lists:
- a file targeted by no leaf contract is an **uncontracted zone**
- a target that does not exist is a discrepancy

Do this by listing and comparing, not by judgement. Report the counts.

## 3. Verify each constraint

For every constraint of every contract in scope:

| Verification | What to do | Passes when |
|---|---|---|
| `script` | Run it with the configured script runner. | Exit code 0. Keep its output for the report. |
| `check` | Follow the check file: look where it says, test every criterion. | Every criterion is met, with path and line cited. If you cannot cite, it fails. |
| missing | The constraint has no verification, or its file does not exist. | Never: it is a discrepancy. |

## 4. Check the contracts themselves

For each contract in scope:
- **Realises**: it contradicts no constraint of the contracts it `realises`, and every parent constraint is backed by a child constraint or by the parent's own verification.
- **Completeness**: compared with its targets, the documentation covers every responsibility, exposed element, error case and configuration at its level. Name what is missing. A contract made of headings and a few lines is a discrepancy (direction `contract`).
- **Size**: if it exceeds what the README calls one readable unit, propose a new level.
- **Notes**: terms and functions used without explanation and missing from **Notes**.

## 5. Report

1. **Discrepancies**, each with contract and constraint, the conflicting parts (contract text and target with path and line), the verification run and its output, and a proposed direction: `code` (the target must change), `contract` (the contract is wrong, outdated or incomplete) or `escalate` (decided higher in the tree). Skip anything already covered by an open ticket.
2. **Uncontracted zones**, each with the contract that should cover it (existing or new).
3. **Contract quality**: incomplete contracts, oversized contracts, missing notes.
4. A one-line summary: files covered / total, constraints passed / checked.

Then, unless the invoker asked for a report only, ask which discrepancies to open as tickets, and whether to change any direction.

## 6. Open tickets

Only when asked, and only for the discrepancies chosen: create `tickets/T-<nnnn>-<slug>.md` following the ticket format, numbering from the highest existing ID. Status `open`, log line `<date> · parity-check · opened`.

If a full check finds no discrepancies and no uncontracted zones, the project is **stable**.
