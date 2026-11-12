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

- `contract-init`: creates the workspace and its configuration, and updates an older workspace to the current tool and README
- `contract-reverse`: writes one detailed contract from listed sources (code, documents, contracts)
- `recontract`: builds the graph from requirements, adds parents above contracts written from code, or reorganises it
- `contract-refine`: changes a few contracts for a task, and brings off-template, outdated or incomplete contracts back to standard
- `parity-check`: sweeps tickets, runs the lint and the verifications, finds uncontracted files and gaps, and opens a ticket for every discrepancy
- `mr-wolf`: resolves code tickets one at a time
- `mattpocock-skills:grilling` (external, used by `recontract` and `contract-refine`)
- `contract-handoff`: records where the flow stopped
- `contract-tools.py` (in the tests folder): the script that lints, verifies, writes every ticket and every structured part of a contract, keeps the scope and the position of the flow, prints quotes and the position header, searches contracts, and writes the handoff. Skills call it; they do not edit those parts by hand.

The external skill comes from Matt Pocock's skills and must be installed beforehand.

## Workspace

All state lives in the workspace (contracts in one flat folder with a generated `INDEX.md`, tickets, handoffs, and a README with the configuration and formats) and in the configured tests folder. Every skill reads it from there. Handoffs are always written to `<workspace>/handoff/`.

## While the flow is active

These rules hold from the moment `/contract-flow` starts until the user stops it.

### Position and citations

You and the user must never lose where you are, and every word of yours about the system rests on a contract's words.

- **Position header.** Every reply that talks about the system or touches a file starts with the block printed by `contract-tools header --file <path[:lines]> --why "<note>"` (one `--file` and `--why` per file treated, with the lines the words refer to). Paste it as printed; never write or edit it. It shows flow, step, contract and clause with their `path:line`, ticket, scope, and each file with its lines and why. The tool reads the flow state you keep with `contract-tools flow start <name>` when the flow starts, `flow step <n> <title> --of <total>` at every step, `flow set --contract <c>#<k> --ticket <T-name>` when the focus changes, and `flow stop` when the user stops. Without a block printed by the tool, give no answer on the merits and make no change to the code. If `header` ends with `UNCONTRACTED ZONE`, follow **No contract covers it**.
- **Quotes.** What a contract says is shown only as a **quote**, printed by `contract-tools quote <contract>#<clause>` (or `quote --all <contract>`), never written from memory and never paraphrased as if it were one:

  ```
  quote — auth_session#session_expires (contracts/auth_session.md:42)
  > The token expires after 15 minutes.
  ```

  The text must be the clause's exact text; it may be cut with `…` only if what is kept is identical. In tickets, handoffs and contracts the lint (`check-quotes`) rejects a quote that differs from its contract. In chat nothing checks it for you, so use the tool's output.
- **Names are words.** Contracts, clauses and tickets are named with words (`auth_session#session_expires`, `T-timeout_too_long`); never refer to them by number or code.

### Statement check

This procedure runs before answering any question or request about the system while the flow is active. Do the steps in this order:

1. **Search by quote.** Run `contract-tools find <the words of the request>` and `contract-tools which-contracts <each file named or touched>`.
2. **No contract covers it** (`UNCONTRACTED ZONE`, exit code 3): follow **No contract covers it**. Do not answer on the merits.
3. **Compare.** Put the request against the quotes found and read the code they enforce. Write one line with exactly one of these outcomes:
   - `compatible`: the contracts allow it. If the code disagrees with a quote, open a code ticket now (`contract-tools ticket new`).
   - `contradicts`: show the quote that contradicts it and the code (path and line), then ask whether to change the contract (`contract-refine`) or drop the request. Do not carry the request out.
   - `undecidable`: the quotes neither allow nor forbid it; show them and ask the user, then refine or open a ticket.
4. **Differences between contract and code.** When the user is right and the contract is outdated, propose `contract-refine` with the code as evidence; when the contract and the code disagree with each other, open the ticket. Never accept a statement that contradicts a quote, and never change a contract because the user said so without showing the quote and the code. If the user declines or postpones a proposal, open the ticket anyway (direction `contract` or `code`): nothing found stays only in the conversation.
5. **Show the work.** The reply starts with the position header, then the outcome line and the quotes it rests on.

### No contract covers it

When `find` or `which-contracts` finds nothing, or `header` ends with `UNCONTRACTED ZONE`, say `uncontracted zone`, name the file or the words, and stop: no answer on the merits and no change to the code. Offer only these ways forward:
- code that exists: `contract-reverse` on it;
- a new requirement: `contract-refine` (or `recontract` if it needs new contracts), whose `clause add --ticket` writes the clause, a failing stub and its ticket together.

Code outside the contracted domain (`OUTSIDE DOMAIN`) is not governed by the flow and is handled normally.

### Rigidity

The flow is strict because it contracts other workflows, which may be as flexible inside as they like. These rules do not bend:

- **No discrepancy is forgotten.** Every difference between a contract and the code, found by any skill or by the statement check, becomes a ticket the moment it is found, without asking. The user may change its direction or close it as `obsolete` with a reason; they cannot have it not opened. The project is not stable while a ticket is `open` or `rerouted`.
- **Governed code is never edited directly.** A request to change code inside the contracted domain becomes a requirement first (`contract-refine`), then a code ticket, then `mr-wolf` at step 5. Requests outside the domain are done normally. The only way out is the user stopping the flow, which writes a handoff.
- **Structure goes through the tool.** Tickets, clauses, edges, scope and handoff are written only with `contract-tools`; you write prose. The lint catches anything left inconsistent by a hand edit.
- **Keep your place.** Run `contract-tools summary` when the flow starts and after every step, and read its state instead of rereading all tickets. The scope is kept in `scope.txt` (`contract-tools scope add`) and the position in `flow.json` (`contract-tools flow`), not in your memory.

### Other rules

- **Uncontracted zones** are announced in the reply where they are found, with a proposal to contract them (see **No contract covers it**). They are not stored: the lint recomputes them on every run (`ZONE`).
- **Scope tracking.** Add every contract changed and file touched to the scope with `contract-tools scope add`. It is the scope of the next parity check.

## Steps

### 0. Locate the workspace
- Once the workspace is found, run `contract-tools flow start contract-flow`; at every step below, `flow step <n> <title> --of 6`, and `flow set --name <skill>` whenever you invoke a skill, so the header names the skill at work. `contract-handoff` ends the flow with `flow stop`.
- Look for `Contract-flow workspace: <path>` in `CLAUDE.md`/`AGENTS.md`, then for a `README.md` containing `<!-- contract-flow-workspace -->`. Show the user what you found and ask them to confirm.
- **Tool version.** Run `python3 -I <tests folder>/contract-tools.py --version` and the same on the copy shipped in the `templates/` folder of the `contract-init` skill. If the project has no `contract-tools.py` (an old `contract-lint.py`), the command fails, or the number is lower, say that the workspace is out of date and offer `contract-init` in update mode before anything else. If the user declines, continue, and say that the checks may not match this workflow.
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
