---
name: contract-flow
description: Workflow: keep a project's code and its contracts in 1:1 parity, from first setup to a stable project. Orchestrates contract-init, recontract, contract-refine, parity-check and mr-wolf.
disable-model-invocation: true
---

# Contract flow

Every part of the project is described by a **contract** (what it must achieve, never how), organised in abstraction levels from the whole system down to single files. This workflow loops until every contract is in parity with its targets:

```
change contracts (grilling) → parity check → tickets → Mr. Wolf resolves code tickets
        ▲                                                         │
        └────────────── contract / escalate / rerouted tickets ◄──┘
```

## Skills used

- `contract-init`: creates the workspace and its configuration
- `recontract`: builds or reorganises the contract tree
- `contract-refine`: changes a few contracts for a task
- `parity-check`: finds discrepancies and opens tickets
- `mr-wolf`: resolves code tickets one at a time
- `grilling` (external, used by the contract skills): every contract change is grilled first
- `handoff` (external): records where the flow stopped

Both external skills come from Matt Pocock's skills and must be installed beforehand.

## Workspace

All state lives in the workspace: contracts, tickets and handoffs, plus a README with the configuration and formats. Every skill reads it from there; this workflow passes nothing else.

## Steps

### 0. Locate the workspace
- **Entry:** always.
- Look for `Contract-flow workspace: <path>` in `CLAUDE.md`/`AGENTS.md`, then for a `README.md` containing `<!-- contract-flow-workspace -->`. Show the user what you found and ask them to confirm.
- If none exists, invoke `contract-init`, then `recontract`, then go to step 2.
- **Checkpoint:** confirm the workspace.

### 1. Resume
- **Entry:** a workspace exists.
- Read the most recent file in `handoff/` and the open tickets. Tell the user where the flow stopped and what comes next, then ask what to do:
  - continue from there
  - start from a new requirement (go to step 2)
  - reorganise the contracts (invoke `recontract`, then step 3)
  - full parity check (step 3, whole tree)

### 2. Change contracts
- **Entry:** a new requirement, or tickets with direction `contract` / `escalate` or status `rerouted`.
- **Invoke:** `contract-refine` with the requirement or those tickets. If it says the change is structural, invoke `recontract` instead.
- **Output:** changed contracts.
- **Checkpoint:** the grilling inside the skill; continue automatically afterwards.

### 3. Parity check
- **Entry:** contracts or code changed, or the user asked for a full check.
- **Invoke:** `parity-check`, scoped to what changed (whole tree only when asked).
- **Output:** new tickets.
- If nothing is found by a full check, the project is **stable**: invoke `handoff`, tell the user and stop. If nothing is found in a scoped check, say so and offer a full check.

### 4. 🛑 Tickets are open
- **Entry:** open tickets exist.
- Summarise them by direction. Ask the user:
  - resolve them all, or stop here
  - for code tickets: Mr. Wolf one by one (choosing each solution), or Mr. Wolf with his recommendation applied automatically
  - sequential (default) or parallel
- If they stop, invoke `handoff` and end.

### 5. Resolve code tickets
- **Entry:** the user chose to resolve.
- **Invoke:** `mr-wolf` on each `open` ticket with direction `code`, one at a time, passing the ticket as its document.
- **Parallel**, only if the user asked: group tickets so that no two groups share a target, and run one `mr-wolf` agent per group. Tickets that share targets stay in the same group and run in sequence.
- **Output:** tickets `resolved` or `rerouted`.
- **Checkpoint:** Mr. Wolf's own stops (choice of solution, end of ticket, alarm).

### 6. Loop
- If any tickets have direction `contract` / `escalate` or status `rerouted`, go to step 2 with them.
- Otherwise go to step 3, scoped to the contracts whose tickets were resolved.

Invoke `handoff` whenever the user stops the flow, so `/contract-flow` can resume it in a new session.
