---
name: parity-check
description: Verify contracts against the files they enforce: run the template lint, run each clause's verification, find every uncontracted file and every gap in a contract, list every discrepancy, and open tickets on request. Use after contracts or code change, or to check whether a project is stable.
---

# Parity check

Finds where contracts and the files they enforce disagree. It never fixes anything and never decides alone: it lists, and opens tickets only when asked.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Names**, **Contract tree**, **Contract format** (with **Verification** and **Lint**) and **Ticket format** sections are binding.

## 1. Decide the scope

The scope is given by whoever invokes the check:
- contracts that changed
- files that changed, mapped to the contracts that enforce them
- contracts or paths the user names

Extend it with the subtrees below those contracts and the contracts they `realize`, up to the root. Check the whole tree only when asked.

## 2. Lint (mechanical, first)

Run `contract-lint.py` from the tests folder with the configured script runner (see **Lint** in the README). Every contract it reports is **off-template**: do not check it further, and do not open tickets for it. It goes to `contract-refine` (report 2 below). Continue with the contracts that pass.

## 3. Coverage (mechanical)

List every file in the scope's paths that is not excluded (`git ls-files` where possible) and every path in the `enforces` of every contract (expanding folders). Compare the two lists:
- a file enforced by no leaf contract is an **uncontracted zone**
- an enforced path that does not exist is a discrepancy

Do this by listing and comparing, not by judgement. Report the counts.

## 4. Verify each clause

For every clause of every conforming contract in scope, use the row in its **Verification** section:

| Type | What to do | Passes when |
|---|---|---|
| `unit`, `interface`, `integration`, `end-to-end`, `script`, or an extra type from the configuration | Run the file with the configured script runner. | Exit code 0. Keep its output for the report. |
| `ai-check` | Follow the check file: look where it says, test every criterion. | Every criterion is met, with path and line cited. If you cannot cite, it fails. |

A clause whose verification is missing is off-template (the lint already caught it).

## 5. Check the contracts themselves

For each conforming contract in scope:
- **Realizes**: it contradicts no clause of the contracts it `realizes`, and every parent clause is backed by a child clause or by the parent's own verification.
- **Completeness (`ai-check`)**: read the enforced files and look for anything they do, expose, accept, return or refuse that no clause covers, or that the View does not show. Name each gap. A contract made of headings and a few lines is a gap. Gaps are never code tickets: they go to `contract-refine`.
- **Size**: if it exceeds what the README calls one readable unit, propose a new level.
- **Notes**: terms used without explanation and missing from **Notes**.

## 6. Report

1. **Discrepancies**: a clause the code breaks, with contract and clause, the conflicting parts (contract text and enforced file with path and line), the verification run and its output, and a proposed direction: `code` (the files must change), `contract` or `escalate` (decided higher in the tree). Skip anything already covered by an open ticket.
2. **For `contract-refine`**, with no ticket: off-template contracts (the lint output), gaps, oversized contracts, missing notes.
3. **Uncontracted zones**, each with the contract that should cover it (existing or new).
4. A one-line summary: contracts conforming / total, files covered / total, clauses passed / checked.

Then, unless the invoker asked for a report only, ask which discrepancies to open as tickets, and whether to change any direction.

## 7. Open tickets

Only when asked, and only for the discrepancies chosen: create `tickets/T-<name>.md` following the ticket format. The name follows the **Names** rules and must not exist yet; reword it if it does. Status `open`, log line `<date> · parity-check · opened`.

If a full check finds every contract conforming, no discrepancy, no gap and no uncontracted zone, the project is **stable**.
