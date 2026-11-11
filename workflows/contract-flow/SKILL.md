---
name: contract-flow
description: Workflow: keep a project's code and its contracts in 1:1 parity, from first setup to a stable project. Contracts are readable documentation with verified clauses. Orchestrates contract-init, contract-reverse, recontract, contract-refine, parity-check and mr-wolf.
---

# Contract flow

Every part of the project is documented by a **contract**: readable documentation (tables, diagrams, simple language) that enforces specific files through named **clauses**, each with a declared verification (unit, interface, integration, end-to-end, script or ai-check). Contracts follow one fixed template, checked by the lint (`contract-tools lint`), and leave no grey zone. They form a graph, from roots that document the whole system down to leaves that enforce files, where a contract can have several parents so shared requirements (security, quality) are written once. Every file is covered by a leaf. This workflow loops until every contract conforms, every clause passes and nothing is uncontracted:

```
change contracts (grilling) → parity check → tickets → Mr. Wolf resolves code tickets
        ▲                                                         │
        └────────────── contract / escalate / rerouted tickets ◄──┘
```

## Skills used

- `contract-init`: creates the workspace and its configuration
- `contract-reverse`: writes one detailed contract from listed sources (code, documents, contracts)
- `recontract`: builds the graph from requirements, adds parents above contracts written from code, or reorganises it
- `contract-refine`: changes a few contracts for a task, and brings off-template, outdated or incomplete contracts back to standard
- `parity-check`: sweeps tickets, runs the lint and the verifications, finds uncontracted files and gaps, and opens a ticket for every discrepancy
- `mr-wolf`: resolves code tickets one at a time
- `mattpocock-skills:grilling` (external, used by `recontract` and `contract-refine`)
- `contract-handoff`: records where the flow stopped
- `contract-tools.py` (in the tests folder): the script that lints, verifies, writes every ticket and every structured part of a contract, keeps the scope and writes the handoff. Skills call it; they do not edit those parts by hand.

The external skill comes from Matt Pocock's skills and must be installed beforehand.

## Workspace

All state lives in the workspace (contracts in one flat folder with a generated `INDEX.md`, tickets, handoffs, and a README with the configuration and formats) and in the configured tests folder. Every skill reads it from there. Handoffs are always written to `<workspace>/handoff/`.

## While the flow is active

These rules hold from the moment `/contract-flow` starts until the user stops it.

### Statement check

Whenever the user states how something works or should work, find the contracts that enforce it, read the relevant clauses and documentation, then read the code they enforce. Decide:

| Contract says | Code does | Then |
|---|---|---|
| same as the user | anything | Nothing to change in the contract. If the code disagrees, open a code ticket now (`contract-tools ticket new`). |
| something else | what the contract says | **Correct the user**: quote the contract and the code (path and line). Ask whether they want to change the behaviour; only then refine. |
| something else | what the user says | The contract is outdated: propose `contract-refine` with the code as evidence. |
| something else | neither | Show all three versions and ask which is right; then refine or open a code ticket. |
| something else | not written yet | Quote the contract and ask which version holds; refine if the user's. |
| nothing | exists | Uncontracted zone: propose `contract-reverse` on it. |
| nothing | not written yet | New requirement: propose `contract-refine` (or `recontract` if it needs new contracts). |

Never silently accept a statement that contradicts a contract, and never change a contract only because the user said so without showing what the contract and the code say. If the user declines or postpones any proposal, open the ticket anyway (direction `contract` or `code`): nothing found is left only in the conversation.

### Rigidity

The flow is strict because it contracts other workflows, which may be as flexible inside as they like. These rules do not bend:

- **No discrepancy is forgotten.** Every difference between a contract and the code, found by any skill or by the statement check, becomes a ticket the moment it is found, without asking. The user may change its direction or close it as `obsolete` with a reason; they cannot have it not opened. The project is not stable while a ticket is `open` or `rerouted`.
- **Governed code is never edited directly.** A request to change code inside the contracted domain becomes a requirement first (`contract-refine`), then a code ticket, then `mr-wolf` at step 5. Requests outside the domain are done normally. The only way out is the user stopping the flow, which writes a handoff.
- **Structure goes through the tool.** Tickets, clauses, edges, scope and handoff are written only with `contract-tools`; you write prose. The lint catches anything left inconsistent by a hand edit.
- **Keep your place.** Run `contract-tools summary` when the flow starts and after every step, and read its state instead of rereading all tickets. The scope is kept in `scope.txt` (`contract-tools scope add`), not in your memory.

### Other rules

- **Uncontracted zones** are announced in the reply where they are found, with a proposal to contract them. They are not stored: the lint recomputes them on every run (`ZONE`).
- **Scope tracking.** Add every contract changed and file touched to the scope with `contract-tools scope add`. It is the scope of the next parity check.

## Steps

### 0. Locate the workspace
- Look for `Contract-flow workspace: <path>` in `CLAUDE.md`/`AGENTS.md`, then for a `README.md` containing `<!-- contract-flow-workspace -->`. Show the user what you found and ask them to confirm.
- If none exists, invoke `contract-init`. Then:
  - the project has code: split the contracted domain into parts a reader can study in one go (with the user), invoke `contract-reverse` on each part, then `recontract` to add the parents above them (and contracts for requirements not yet in the code)
  - no code yet: invoke `recontract` to build the graph from requirements (or write leaves first and add parents later)
- Then go to step 3 with the whole graph as scope.
- If a skill stops because the job belongs to another one (structure vs content vs documenting code), invoke that one.

### 1. Resume
- Run `contract-tools summary`, and read the most recent file in `<workspace>/handoff/`. Tell the user where the flow stopped and what comes next, then ask what to do:
  - continue from there (open tickets → step 4)
  - start from a new requirement (step 2)
  - contract existing code (`contract-reverse`, then step 3)
  - reorganise the contracts (`recontract`, then step 3)
  - check a part of the project, or all of it (step 3)

### 2. Change contracts
- **Entry:** a new requirement or statement, tickets with direction `contract` / `escalate` or status `rerouted`, or a contract that failed the lint (`contract-tools lint`), is outdated or has a gap (found by the parity check).
- **Invoke:** `contract-refine`. If the change is structural or a contract needs a new level, invoke `recontract`. If it is about code that has no contract, invoke `contract-reverse`.
- **Output:** changed contracts and verifications, added to the scope.

### 3. Parity check
- **Invoke:** `parity-check` with the tracked scope (or what the user named).
- It first sweeps the tickets and runs the lint: a contract that fails goes to `contract-refine` (step 2) before anything else is checked on it. Then it opens a ticket for every discrepancy, without asking, and lists uncontracted zones and contract gaps. Offer `contract-reverse` for each uncontracted zone and `contract-refine` for each gap or off-template contract (a gap gets its clause, a failing stub and its ticket together).
- If a full check finds nothing and `contract-tools summary` shows no open or rerouted ticket, the project is **stable**: invoke `contract-handoff`, tell the user and stop. If a scoped check finds nothing, say so and offer a full check.

### 4. 🛑 Tickets are open
- Show `contract-tools summary`. Ask the user:
  - resolve them, or stop here
  - for code tickets: Mr. Wolf interactive (you choose each solution), automatic (his recommendation, stopping only on alarm) or autonomous alarm (never stops)
  - sequential (default) or parallel
- If they stop, invoke `contract-handoff` and end.

### 5. Resolve code tickets
- **Invoke:** `mr-wolf` on each `open` ticket with direction `code`, passing the ticket as its document, and tell it:
  - **mode**: the one chosen at step 4
  - **clauses**: the ticket's contract and every contract it `implements`, through every parent, up to the roots
  - **check**: after executing, run the ticket clause's verification (`contract-tools verify --contract <id>`), then `parity-check` scoped to the files changed; any new discrepancy becomes a ticket, as always
  - **outcome**: `contract-tools ticket status <id> resolved --reason "..."`; if it ends `blocked`, `ticket status <id> rerouted --reason "..."` and `ticket direction <id> contract --reason "..."` instead. Add the files touched with `contract-tools scope add`.
- **Parallel**, only if the user asked: group tickets so that no two groups share an enforced file or a touched file, and run one `mr-wolf` agent per group. Tickets in the same group run in sequence.
- **Output:** tickets `resolved` or `rerouted`; files touched added to the scope.

### 6. Loop
- Run `contract-tools summary`. If any tickets have direction `contract` / `escalate` or status `rerouted`, go to step 2 with them.
- Otherwise go to step 3 with the tracked scope (`contract-tools scope list`).

Invoke `contract-handoff` whenever the user stops the flow (it runs `contract-tools handoff`, writing to `<workspace>/handoff/`), so `/contract-flow` can resume it in a new session.
