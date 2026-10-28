<!-- contract-flow-workspace -->
# Contract-flow workspace

This folder holds the **contracts** that describe what this project must do, the **tickets** that track where the project does not match them yet, and the **handoffs** that let a new session pick up where the last one stopped.

## How the flow works

1. **Contracts** say *what* each part of the system must achieve, never *how*. They are nested: the root contract describes the whole system, its children describe its parts, down to single files.
2. A **parity check** verifies each clause of a contract against its targets (child contracts, code, other resources) and lists every discrepancy.
3. On request, discrepancies become **tickets**, with a direction: `code`, `contract` or `escalate`.
4. Code tickets are resolved by **Mr. Wolf**, one at a time. Contract and escalate tickets go back to **refinement**, which always starts with a grilling session.
5. The project is **stable** when every contract in the tree is in parity with its targets.

To start or resume, run `/contract-flow`.

## Folders

| Folder | Contents |
|---|---|
| `contracts/` | The contract tree. The children of `x.md` live in the folder `x/` next to it. |
| `tickets/` | One file per ticket, `T-<nnnn>-<slug>.md`. Closed tickets stay here with their status. |
| `handoff/` | Session handoffs. The most recent one says what to do next. |

## Configuration

<!-- Filled in by contract-init. Edit by hand or rerun /contract-init. -->

- **Contracted domain:** {{paths governed by contracts}}
- **Excluded:** {{paths explicitly out of scope, never reported as uncontracted, or "none"}}
- **Existing documentation:** {{folders/files that already exist and what they contain}}

## Contract format

```
contracts/
├── system.md              id: system (the root)
└── system/
    ├── auth.md            id: system/auth
    ├── auth/
    │   └── session.md     id: system/auth/session
    └── billing.md         id: system/billing
```

A contract's **ID is its path** inside `contracts/` without `.md`. Its parent is the contract with the name of the folder it sits in. A contract with no children is a single file; the folder is created when its first child is.

Every contract has the same sections. Leave a section empty (write "None") rather than removing it.

```markdown
---
targets:                          # required: everything this contract governs
  - src/auth/                     # code, folders, any resource
  - contracts/system/auth/        # child contracts (implied for a contract with a folder)
realises: [system§E2, system§I1]  # parent clauses this contract fulfils (not on the root)
---

# Authentication

## Purpose
<why this part exists, 2-3 lines>

## Interface
<what it exposes to the outside: API, commands, files produced… or None>

## Requires
- **§R1** A user store is reachable. `verify: inspection`

## Ensures
- **§E1** A request to a protected endpoint without a valid session is rejected with 401. `verify: test`
- **§E2** Sessions expire after 30 minutes of inactivity. `verify: inspection`

## Invariants
- **§I1** Passwords are never stored or logged in clear text. `verify: static`

## Decisions
- <choice made and why, e.g. "Sessions are server-side because tokens must be revocable.">
```

### Clauses

- **Requires** (`§R`) are preconditions: what must be true for this part to work. **Ensures** (`§E`) are postconditions: what it guarantees. **Invariants** (`§I`) always hold.
- Clause IDs never change once written. A removed clause leaves a gap; new clauses get new numbers. Elsewhere a clause is referenced as `<contract id>§<clause>`, e.g. `system/auth§E2`.
- High in the tree clauses are coarse ("client and server communicate only over HTTP"); at the leaves they are precise enough to check mechanically.
- A parent may require a minimum verification method of its descendants (e.g. "every Ensures below this contract is verified by `test`").

### Verification methods

| `verify:` | Proven by |
|---|---|
| `inspection` | Reading the targets, with the evidence cited (path and line). Default; the weakest. |
| `test` | A test that demonstrates it. Requires a **verification contract**: a leaf contract targeting the test files, whose clauses state which clauses each test covers. |
| `static` | A tool: type checker, linter, architecture rule. Name the tool and the rule. |
| `command` | A command whose result proves it. Write the command and the expected result. |
| `review` | Only a person can confirm it. Parity checks report it, never judge it. |

Tests are ordinary code: they exist only where a contract requires them.

## Ticket format

```markdown
---
id: T-0007
status: open            # open | resolved | rerouted | obsolete
direction: code         # code | contract | escalate
contract: system/auth
clause: §E2
---

# Sessions expire after one hour instead of 30 minutes

## Problem
<in plain words: what is wrong and why it matters>

## Conflict
- contracts/system/auth.md §E2: "Sessions expire after 30 minutes of inactivity."
- src/auth/session.py:42: `SESSION_TIMEOUT = 3600`

## Verification
<method used and what it showed>

## Proposed direction
code: the contract reflects the agreed requirement; the constant is wrong.

## Log
<!-- appended by whoever works on the ticket, newest last -->
- 2026-10-28 · parity-check · opened
```
