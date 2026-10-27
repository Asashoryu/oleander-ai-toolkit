<!-- contract-flow-workspace -->
# Contract-flow workspace

This folder holds the **contracts** that describe what this project must do, the **tickets** that track where the code does not match them yet, and the **handoffs** that let a new session pick up where the last one stopped.

## How the flow works

1. **Contracts** say *what* each part of the system must achieve, never *how*. They are organised in levels, from a coarse description of the whole system down to single files.
2. A **parity check** compares a contract with its targets (child contracts or code) and lists every discrepancy.
3. Each discrepancy becomes a **ticket**, with a direction: `code`, `contract` or `escalate`.
4. Code tickets are resolved by **Mr. Wolf**, one at a time. Contract and escalate tickets go back to **refinement**, which always starts with a grilling session.
5. The project is **stable** when every contract at every level is in parity with its targets.

To start or resume, run `/contract-flow`.

## Folders

| Folder | Contents |
|---|---|
| `contracts/` | One subfolder per abstraction level, named `<n>-<name>/` (0 is the most abstract). |
| `tickets/` | One file per ticket, `T-<nnnn>-<slug>.md`. Closed tickets stay here with their status. |
| `handoff/` | Session handoffs. The most recent one says what to do next. |

## Configuration

<!-- Filled in by contract-init. Edit by hand or rerun /contract-init. -->

- **Contracted domain:** {{paths of code governed by contracts}}
- **Excluded:** {{paths explicitly out of scope, or "none"}}
- **Existing documentation:** {{folders/files that already exist and what they contain, e.g. "docs/specs/: feature specs (absorbed into level 2 contracts)"}}
- **Levels:**
  {{- `0-system`: whole system, architecture only}}
- **Mr. Wolf alarm mode:** stop  <!-- stop | autonomous -->

## Contract format

A contract is a Markdown file in `contracts/<level>/`. Its body can take any form (spec, PRD, design decisions…) as long as every verifiable statement is a **clause** with a stable ID.

```markdown
---
id: services/auth                    # stable; used by tickets and children
level: 1-services
parent: system                       # omitted only for the root contract
targets:                             # required: everything this contract governs
  - contracts/2-modules/auth-session.md
  - src/auth/
realises: [system§2, system§3.1]     # parent clauses this contract fulfils
---

# Authentication service

<free-form context: purpose, decisions and their reasons, constraints>

## Clauses

- **§1** Every request to a protected endpoint is rejected unless it carries a valid session.
- **§2** Sessions expire after 30 minutes of inactivity.
  - **§2.1** When a session expires, the user is asked to log in again and the original request is not lost.
```

Rules:
- Clause IDs never change once published. Removing a clause leaves a gap; new clauses get new numbers.
- High-level clauses can be coarse ("the system is client-server"). Leaf clauses must be precise enough to check mechanically, e.g. EARS ("When <trigger>, the <component> shall <response>") or Given/When/Then.
- Tests are ordinary code. They exist only where a contract requires them.
- Targets never reference their contract back.

## Ticket format

```markdown
---
id: T-0007
status: open            # open | resolved | rerouted | obsolete
direction: code         # code | contract | escalate
contract: services/auth
clause: §2.1
target: src/auth/session.py
---

# Expired session drops the original request

## Discrepancy
<what the clause requires vs what the target does>

## Evidence
<quotes from the contract and the relevant code or child contract, with paths and line numbers>

## Log
<!-- appended by whoever works on the ticket, newest last -->
- 2026-10-27 · parity-check · opened
```
