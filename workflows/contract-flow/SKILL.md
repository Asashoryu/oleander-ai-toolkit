---
name: contract-flow
description: Workflow: keep a project's code and its contracts in 1:1 parity, from first setup to a stable project. Orchestrates contract-init, recontract, contract-refine, parity-check and mr-wolf.
disable-model-invocation: true
---

# Contract flow

Every part of the project is described by a **contract** (what it must achieve, never how). Contracts are nested from the whole system down to single files. This workflow loops until every contract is in parity with its targets:

```
change contracts (grilling) → parity check → tickets → Mr. Wolf resolves code tickets
        ▲                                                         │
        └────────────── contract / escalate / rerouted tickets ◄──┘
```

## Skills used

- `contract-init`: creates the workspace and its configuration
- `recontract`: builds or reorganises the contract tree
- `contract-refine`: changes a few contracts for a task
- `parity-check`: verifies clauses, lists discrepancies and uncontracted zones, opens tickets on request
- `mr-wolf`: resolves code tickets one at a time
- `grilling` (external, used by `recontract` and `contract-refine`)
- `handoff` (external): records where the flow stopped

Both external skills come from Matt Pocock's skills and must be installed beforehand.

## Workspace

All state lives in the workspace: contracts, tickets and handoffs, plus a README with the configuration and formats. Every skill reads it from there. Handoffs are always written to `<workspace>/handoff/`.

## While the flow is active

These rules hold from the moment `/contract-flow` starts until the user stops it:

- **Statement check.** Whenever the user states how something works or should work, find the contracts that target it and compare:
  - contradiction → point it out, quoting the clause, and ask which is right
  - new information → propose `contract-refine`
  - no contract covers it → announce it as an uncontracted zone and propose to contract it
- **Uncontracted zones** are always announced in the reply where they are found, with a proposal to contract them. They are never stored.
- **Scope tracking.** Keep a list of contracts changed and files touched during the session. It is the scope of the next parity check.

## Steps

### 0. Locate the workspace
- Look for `Contract-flow workspace: <path>` in `CLAUDE.md`/`AGENTS.md`, then for a `README.md` containing `<!-- contract-flow-workspace -->`. Show the user what you found and ask them to confirm.
- If none exists, invoke `contract-init`, then `recontract`, then go to step 3 with the whole tree as scope.
- If `recontract` or `contract-refine` stops because the change is the other's job (structural vs content), invoke the other one.

### 1. Resume
- Read the most recent file in `<workspace>/handoff/` and the open tickets. Tell the user where the flow stopped and what comes next, then ask what to do:
  - continue from there (open tickets → step 4)
  - start from a new requirement (step 2)
  - reorganise the contracts (`recontract`, then step 3)
  - check a part of the project, or all of it (step 3)

### 2. Change contracts
- **Entry:** a new requirement or statement, an uncontracted zone to contract, or tickets with direction `contract` / `escalate` or status `rerouted`.
- **Invoke:** `contract-refine`. If it says the change is structural, invoke `recontract` instead.
- **Output:** changed contracts, added to the scope.

### 3. Parity check
- **Invoke:** `parity-check` with the tracked scope (or what the user named).
- It lists discrepancies and uncontracted zones and asks which to open as tickets. Offer to contract each uncontracted zone through step 2.
- If nothing is found by a full check, the project is **stable**: invoke `handoff`, tell the user and stop. If a scoped check finds nothing, say so and offer a full check.

### 4. 🛑 Tickets are open
- Summarise the open tickets by direction. Ask the user:
  - resolve them, or stop here
  - for code tickets: Mr. Wolf interactive (you choose each solution), automatic (his recommendation, stopping only on alarm) or autonomous alarm (never stops)
  - sequential (default) or parallel
- If they stop, invoke `handoff` and end.

### 5. Resolve code tickets
- **Invoke:** `mr-wolf` on each `open` ticket with direction `code`, passing the ticket as its document, and tell it:
  - **mode**: the one chosen at step 4 (interactive, automatic, autonomous alarm)
  - **constraints**: the ticket's contract and all its ancestors
  - **check**: after executing, run `parity-check` scoped to the files changed, report only, no tickets
  - **outcome**: set the ticket's `status` to `resolved`; if it ends `blocked`, set `status: rerouted` and `direction: contract` instead
- **Parallel**, only if the user asked: group tickets so that no two groups share a target or a touched file, and run one `mr-wolf` agent per group. Tickets in the same group run in sequence.
- **Output:** tickets `resolved` or `rerouted`; files touched added to the scope.

### 6. Loop
- If any tickets have direction `contract` / `escalate` or status `rerouted`, go to step 2 with them.
- Otherwise go to step 3 with the tracked scope.

Invoke `handoff` whenever the user stops the flow, writing to `<workspace>/handoff/`, so `/contract-flow` can resume it in a new session.
