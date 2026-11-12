---
name: parity-check
description: Verify contracts against the files they enforce: run the lint and the ticket sweep, run each clause's verification, find every uncontracted file and every gap in a contract, and open a ticket for every discrepancy. Use after contracts or code change, or to check whether a project is stable.
---

# Parity check

Finds where contracts and the files they enforce disagree. It never fixes anything: it finds, and records every discrepancy as a ticket.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Names**, **Contract graph**, **Contract format** (with **Verification** and **Lint**), **contract-tools** and **Ticket format** sections are binding.

## Quotes

When you say what a contract says, use `contract-tools quote <contract>#<clause>` and paste its output; never paraphrase it or write it from memory. Look contracts up with `contract-tools find` and `which-contracts` (exit code 3 and `UNCONTRACTED ZONE` mean no contract covers it: stop, see **No contract covers it** in the contract-flow workflow). Names are words, never codes.

## 1. Decide the scope

The scope is given by whoever invokes the check:
- contracts that changed
- files that changed, mapped to the contracts that enforce them
- contracts or paths the user names

Extend it with every descendant of those contracts (through `enforces`) and every ancestor (through `implements`: every parent, up to the roots). Check the whole graph only when asked.

## 2. Sweep and lint (mechanical, first)

Run these from the project root with the configured script runner. The tool does the counting; you do not repeat it by hand.

1. `contract-tools ticket sweep`: tickets whose clause or contract no longer exists become `obsolete`, `open` code tickets whose verification now passes become `resolved`, and `resolved` tickets whose verification fails again are reopened. Report what it changed.
2. `contract-tools lint`. Every contract it reports with `FAIL` is **off-template**: do not check it further, and do not open tickets for it. It goes to `contract-refine` (report 2 below). Continue with the contracts that pass.

## 3. Coverage (mechanical)

The lint already printed it: every `ZONE` line is a file of the contracted domain that no leaf contract enforces, an **uncontracted zone**. A `FAIL` for an enforced path that does not exist is a discrepancy. Report the counts the tool printed; do not compare lists by judgement.

## 4. Verify each clause

Run `contract-tools verify` (add `--contract <id>` for each contract in scope). It runs every scripted verification and prints one line per clause:

| Line | Meaning | What to do |
|---|---|---|
| `PASS` | the script exited 0 | nothing |
| `FAIL` | the script failed, is missing, or is a stub | a discrepancy |
| `JUDGE` | `ai-check` or `covered-by`: no script can decide | judge it yourself, as below |

| Type | How to judge | Passes when |
|---|---|---|
| `ai-check` | Follow the check file: look where it says, test every criterion. | Every criterion is met, with path and line cited. If you cannot cite, it fails. |
| `covered-by` | Read the clauses it names in the enforced contracts, in their written form, and judge whether together they satisfy the clause. Do not read the code: the leaves prove it. | The named clauses cover every part of the clause, with their text cited. |

A clause whose verification is missing is off-template (the lint already caught it).

## 5. Check the contracts themselves

For each conforming contract in scope:
- **Implements**: it contradicts no clause of any contract it `implements` (every parent), and every clause of a contract that enforces contracts is covered by clauses of those contracts.
- **Completeness (`ai-check`)**: read the enforced files and look for anything they do, expose, accept, return or refuse that no clause covers, or that the View does not show. Name each gap. A contract made of headings and a few lines is a gap. Gaps are never code tickets: they go to `contract-refine`.
- **Size**: the lint reports a contract that is too large; propose a new level.
- **Notes**: terms used without explanation and missing from **Notes**.

## 6. Report and tickets

**Every discrepancy becomes a ticket now, without asking.** For each clause that failed or was judged failing, run `contract-tools ticket new <name> <contract> <clause> --direction <d> --reason "<why>"` with `--problem`, `--conflict`, `--verification` and `--proposal` filled in plain words (the conflicting contract text as a quote, and the enforced file with path and line, the verification run and its output). The name follows the **Names** rules. If the clause already has a ticket, the tool reopens it or says it is open: never a second one. The direction is `code` (the files must change), `contract` or `escalate` (decided higher in the graph). The user may change a direction afterwards (`ticket direction`) or close a ticket as `obsolete` with a reason (`ticket status`), but a discrepancy is never left without a ticket. If the invoker asked for a report only, say so in the report and open nothing.

A gap (something the files do that no clause covers) has no clause to hang a ticket on: send it to `contract-refine`, which adds the clause with `clause add --ticket`, creating a failing stub and its ticket together.

Report:

1. **Tickets** opened or reopened, and those the sweep changed.
2. **For `contract-refine`**: off-template contracts (the lint output), gaps, oversized contracts, missing notes.
3. **Uncontracted zones**, each with the contract that should cover it (existing or new).
4. A one-line summary from the tool: contracts conforming / total, files covered / total, clauses passed / failed / judged.

The project is **stable** only if a full check finds every contract conforming, no `FAIL`, no gap, no uncontracted zone, every judged clause holding, and `contract-tools summary` shows no `open` or `rerouted` ticket.
