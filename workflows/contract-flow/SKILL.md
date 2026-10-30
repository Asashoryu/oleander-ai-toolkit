---
name: contract-flow
description: Workflow: keep a project's code and its contracts in 1:1 parity, from first setup to a stable project. Contracts are readable documentation with verified constraints. Orchestrates contract-init, contract-reverse, recontract, contract-refine, parity-check and mr-wolf.
disable-model-invocation: true
---

# Contract flow

Every part of the project is documented by a **contract**: readable documentation (tables, diagrams, simple language) that targets specific files and imposes **constraints** on them, each verified by a script or a check file. Contracts are nested from the whole system down to single files, and every file is covered. This workflow loops until every constraint passes and nothing is uncontracted:

```
change contracts (grilling) → parity check → tickets → Mr. Wolf resolves code tickets
        ▲                                                         │
        └────────────── contract / escalate / rerouted tickets ◄──┘
```

## Skills used

- `contract-init`: creates the workspace and its configuration
- `contract-reverse`: writes detailed contracts from existing code
- `recontract`: builds the tree from requirements, or reorganises it
- `contract-refine`: changes a few contracts for a task
- `parity-check`: runs verifications, finds uncontracted files and thin contracts, opens tickets on request
- `mr-wolf`: resolves code tickets one at a time
- `grilling` (external, used by `recontract` and `contract-refine`)
- `handoff` (external): records where the flow stopped

Both external skills come from Matt Pocock's skills and must be installed beforehand.

## Workspace

All state lives in the workspace (contracts, tickets, handoffs, and a README with the configuration and formats) and in the configured tests folder. Every skill reads it from there. Handoffs are always written to `<workspace>/handoff/`.

## While the flow is active

These rules hold from the moment `/contract-flow` starts until the user stops it.

### Statement check

Whenever the user states how something works or should work, find the contracts that target it, read the relevant constraints and documentation, then read the code they target. Decide:

| Contract says | Code does | Then |
|---|---|---|
| same as the user | anything | Nothing to do (if the code disagrees, it is a ticket for the next parity check). |
| something else | what the contract says | **Correct the user**: quote the contract and the code (path and line). Ask whether they want to change the behaviour; only then refine. |
| something else | what the user says | The contract is outdated: propose `contract-refine` with the code as evidence. |
| something else | neither | Show all three versions and ask which is right; then refine or open a code ticket. |
| something else | not written yet | Quote the contract and ask which version holds; refine if the user's. |
| nothing | exists | Uncontracted zone: propose `contract-reverse` on it. |
| nothing | not written yet | New requirement: propose `contract-refine` (or `recontract` if it needs new contracts). |

Never silently accept a statement that contradicts a contract, and never change a contract only because the user said so without showing what the contract and the code say.

### Other rules

- **Uncontracted zones** are announced in the reply where they are found, with a proposal to contract them. They are never stored.
- **Scope tracking.** Keep a list of contracts changed and files touched during the session. It is the scope of the next parity check.

## Steps

### 0. Locate the workspace
- Look for `Contract-flow workspace: <path>` in `CLAUDE.md`/`AGENTS.md`, then for a `README.md` containing `<!-- contract-flow-workspace -->`. Show the user what you found and ask them to confirm.
- If none exists, invoke `contract-init`. Then:
  - the project has code: invoke `contract-reverse` on the whole contracted domain, then `recontract` only if the user wants to add contracts for requirements not yet in the code
  - no code yet: invoke `recontract` to build the tree from requirements
- Then go to step 3 with the whole tree as scope.
- If a skill stops because the job belongs to another one (structure vs content vs documenting code), invoke that one.

### 1. Resume
- Read the most recent file in `<workspace>/handoff/` and the open tickets. Tell the user where the flow stopped and what comes next, then ask what to do:
  - continue from there (open tickets → step 4)
  - start from a new requirement (step 2)
  - contract existing code (`contract-reverse`, then step 3)
  - reorganise the contracts (`recontract`, then step 3)
  - check a part of the project, or all of it (step 3)

### 2. Change contracts
- **Entry:** a new requirement or statement, or tickets with direction `contract` / `escalate` or status `rerouted`.
- **Invoke:** `contract-refine`. If the change is structural or a contract needs a new level, invoke `recontract`. If it is about code that has no contract, invoke `contract-reverse`.
- **Output:** changed contracts and verifications, added to the scope.

### 3. Parity check
- **Invoke:** `parity-check` with the tracked scope (or what the user named).
- It lists discrepancies, uncontracted zones and contract quality problems, and asks which to open as tickets. Offer `contract-reverse` for each uncontracted zone and `contract-refine` for each thin contract.
- If a full check finds nothing, the project is **stable**: invoke `handoff`, tell the user and stop. If a scoped check finds nothing, say so and offer a full check.

### 4. 🛑 Tickets are open
- Summarise the open tickets by direction. Ask the user:
  - resolve them, or stop here
  - for code tickets: Mr. Wolf interactive (you choose each solution), automatic (his recommendation, stopping only on alarm) or autonomous alarm (never stops)
  - sequential (default) or parallel
- If they stop, invoke `handoff` and end.

### 5. Resolve code tickets
- **Invoke:** `mr-wolf` on each `open` ticket with direction `code`, passing the ticket as its document, and tell it:
  - **mode**: the one chosen at step 4
  - **constraints**: the ticket's contract and every contract it `realises`, up to the root
  - **check**: after executing, run the ticket constraint's verification, then `parity-check` scoped to the files changed, report only, no tickets
  - **outcome**: set the ticket's `status` to `resolved`; if it ends `blocked`, set `status: rerouted` and `direction: contract` instead
- **Parallel**, only if the user asked: group tickets so that no two groups share a target or a touched file, and run one `mr-wolf` agent per group. Tickets in the same group run in sequence.
- **Output:** tickets `resolved` or `rerouted`; files touched added to the scope.

### 6. Loop
- If any tickets have direction `contract` / `escalate` or status `rerouted`, go to step 2 with them.
- Otherwise go to step 3 with the tracked scope.

Invoke `handoff` whenever the user stops the flow, writing to `<workspace>/handoff/`, so `/contract-flow` can resume it in a new session.
