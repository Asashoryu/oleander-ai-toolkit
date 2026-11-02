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

## Learning

**Study folder**
The folder inside an Obsidian vault (or, with no vault, a folder of Obsidian-format notes) where `learn-with-obsidian` keeps its notes, chosen once. Not the contract-flow workspace.
**Hub, reference note, source note, record**
The four note types of `learn-with-obsidian`: a topic's entry point, one atomic concept, one study source, and one session's findings. A topic is never finished.

## Contracts

**Contract**
A readable document about one part of the system, written in simple language and shown mostly through diagrams and tables, plus the clauses it imposes on the files it enforces. It has a fixed header (`name`, `realizes`, `enforces`) and five sections in a fixed order: Purpose, View, Clauses, Verification, Notes (optional). Only these are rigid; the content inside is free. It leaves no grey zone: everything the parts do or expose is covered by a clause or declared out of the contract. Design decisions are part of the contract at the right abstraction level, never standalone documents. A contract made only of headings and a few lines is a defect.
_Avoid_: spec (a spec file is any skill's input; a contract is specifically documentation with obligations).
**Enforced file**
A file or folder a contract binds, listed in its `enforces` field so a person or an agent can navigate from the contract to what it governs. Enforced files never point back to their contract.
**Name**
How clauses and tickets are identified: at most 3 words joined by `_`, in the language of the project, describing what they mean. Never a number. A clause name is unique in its contract, a ticket name in the project.
**Verification**
How a clause is proven: one row per clause in the Verification section, with a type from a closed list (`unit`, `interface`, `integration`, `end-to-end`, `script`, `ai-check`; a project may add more) and a file in the tests folder chosen at setup. Every type but `ai-check` is a deterministic script that passes on exit code 0; `ai-check` is a check file judged by the model with cited evidence, used only when no script can decide. A clause with no verification is not accepted.
**Clause**
A single checkable fact a contract imposes on its enforced files, precise enough to leave no grey zone. Coarse at high levels, exact at the leaves. Referenced as `<contract id>#<clause name>`; tickets point to the clause violated.
**Contract lint**
The script `contract-lint.py` in the tests folder. It checks only the rigid parts of the template (header, sections, names, verification rows, tickets). A contract that fails it goes to contract refinement before any other check.
**Workspace**
The single folder where a workflow keeps its contracts, tickets and handoffs, together with a README explaining the flow, the formats and the configuration. Its location, and that of the tests folder, are always chosen at setup.
**Contract tree**
All contracts of a project, nested by folder: the children of `x.md` live in the folder `x/` next to it. A contract's ID is its path without `.md` (e.g. `system/auth/session`). Each contract has exactly one parent, except the root.

**Abstraction level**
How far a contract is from the code: its depth in the contract tree. Deeper contracts are more detailed and cover less. A contract too large to read in one go is split into an overview and children that take the detail. Levels are never numbered or named.
**Contracted domain**
The part of the codebase that is governed by contracts. Code outside it is ignored by parity checks.

**Uncontracted zone**
A file inside the contracted domain, not excluded, that no leaf contract enforces. Found mechanically by comparing the file list with all enforced files, announced whenever found, with a proposal to contract it.
**Notes**
The optional last section of a contract, listing each term, function or name used in it whose meaning the text does not explain.
**Reverse contracting**
Writing contracts from existing code: every file read, every responsibility documented, every file covered, every clause given a verification.
**Statement check**
While contract-flow is active, every statement the user makes about how the system works or should work is compared with the contracts and with the code they enforce. If the code agrees with the contract, the user is corrected; if it agrees with the user, the contract is outdated and gets refined; otherwise the user decides. Missing coverage is announced as an uncontracted zone.
**Parity**
The state where a contract and what it covers agree 1:1. Checked contract ↔ child contracts and, for leaf contracts, contract ↔ code. Gaps, outdated contracts and off-template contracts are not parity problems: they are solved by refinement. A higher-level contract cares only that its own statements hold, not how lower levels achieve them; verifying it may still require inspecting everything beneath it.

**Ticket**
A discrepancy found by a parity check between a contract and one of its enforced files, including a clause that nothing satisfies yet. Identified as `T-<name>` (a name, see above). Implementing new work and fixing errors are both done by resolving tickets. Each ticket has a direction, decided when it is created:
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
A project in which every contract passes the lint, every clause passes and no file is uncontracted.