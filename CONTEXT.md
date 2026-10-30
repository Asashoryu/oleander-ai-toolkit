# Context

Glossary of the oleander-ai-toolkit domain.

## Toolkit

**Skill**
A single, reusable capability: what the AI does and which tools it uses. Not tied to any one workflow.

**Workflow**
A step-by-step method that orchestrates several skills toward a larger goal. Owns only the orchestration, not the capabilities.

**Spec file**
The document a skill attaches to for its input and state. Chosen by the workflow that invokes the skill, or by the user when the skill runs standalone.

**External skill**
A skill a workflow relies on that is not part of this toolkit. Listed as a prerequisite and must be installed beforehand.

**Handoff**
A document that captures where a workflow stopped, so a fresh session can resume it.

## Contracts

**Contract**
A readable document about one part of the system: what it is for, how it works and what it exposes, written in simple language with tables and diagrams, plus the constraints it imposes on its targets. It names the contracts it respects (`realises`) and the files it constrains (`targets`). Design decisions are part of the contract at the right abstraction level, never standalone documents. A contract made only of headings and a few lines is a defect.
_Avoid_: spec (a spec file is any skill's input; a contract is specifically documentation with obligations).
**Target**
A file or folder a contract constrains. Every contract lists its targets explicitly, so a person or an agent can navigate from it to what it governs. Targets never point back to their contract.
**Verification**
How a constraint is proven, stored in the tests folder chosen at setup. Either a **script** (deterministic, passes on exit code 0) or a **check file** (criteria judged by the model, with cited evidence). A constraint with no verification is not accepted.
**Constraint**
A single checkable fact a contract imposes on its targets, with a stable ID (`C1`, `C2`…), a verification and an enforcement (when the verification runs). Coarse at high levels, precise at the leaves. Referenced as `<contract id>#C<n>`; tickets point to the constraint violated.
**Workspace**
The single folder where a workflow keeps its contracts, tickets and handoffs, together with a README explaining the flow, the formats and the configuration. Its location, and that of the tests folder, are always chosen at setup.
**Contract tree**
All contracts of a project, nested by folder: the children of `x.md` live in the folder `x/` next to it. A contract's ID is its path without `.md` (e.g. `system/auth/session`). Each contract has exactly one parent, except the root.

**Abstraction level**
How far a contract is from the code: its depth in the contract tree. Deeper contracts are more detailed and cover less. A contract too large to read in one go is split into an overview and children that take the detail. Levels are never numbered or named.
**Contracted domain**
The part of the codebase that is governed by contracts. Code outside it is ignored by parity checks.

**Uncontracted zone**
A file inside the contracted domain, not excluded, that no leaf contract targets. Found mechanically by comparing the file list with all targets, announced whenever found, with a proposal to contract it.
**Notes**
The final section of every contract, listing each term, function or name used in it whose meaning the text does not explain.
**Reverse contracting**
Writing contracts from existing code: every file read, every responsibility documented, every file covered, every constraint given a verification.
**Statement check**
While contract-flow is active, every statement the user makes about how the system works or should work is compared with the contracts and with the code they target. If the code agrees with the contract, the user is corrected; if it agrees with the user, the contract is outdated and gets refined; otherwise the user decides. Missing coverage is announced as an uncontracted zone.
**Parity**
The state where a contract and what it covers agree 1:1. Checked contract ↔ child contracts and, for leaf contracts, contract ↔ code. A higher-level contract cares only that its own statements hold, not how lower levels achieve them; verifying it may still require inspecting everything beneath it.

**Ticket**
A discrepancy found by a parity check between a contract and one of its targets, including a constraint that nothing satisfies yet. Implementing new work and fixing errors are both done by resolving tickets. Each ticket has a direction, decided when it is created:
- **code**: the code must change to honour the contract.
- **contract**: the contract itself must change.
- **escalate**: a higher abstraction level must be re-examined first.

A ticket's status is one of:
- **open**: created by a parity check, not yet resolved.
- **resolved**: the discrepancy is gone; the ticket's log says how.
- **rerouted**: could not be resolved without changing a contract; its direction changed and it went back to contract refinement.
- **obsolete**: a contract changed and the discrepancy no longer exists.

_Avoid_: issue, bug (those may exist in the project's own docs with other meanings).

**Scoped parity check**
A parity check limited to the contracts whose responsibility is affected by a change: the changed contract, its subtree and its ancestors. The change is known from the flow itself (contracts refined, files touched while resolving tickets) or stated by the user. Full checks of the whole tree are rare, because high-level contracts are coarse.

**Alarm**
The moment, while resolving a ticket, when the chosen solution turns out to cost substantially more (or differently) than estimated. By default work stops and a new set of weighed alternatives is proposed to the user; in autonomous mode the lowest-cost alternative is applied and logged instead.

**Recontracting**
Changing the structure of the contract tree: building it from requirements when there is no code yet, or moving, merging, splitting, re-nesting contracts and adding levels. Rare and broad.
**Refinement**
Changing the content of a few contracts for a specific task. Frequent and narrow.

**Stable project**
A project in which every constraint passes and no file is uncontracted.