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

**Setup note**
The note `<Topic> - Setup` written by `studio-setup`: the study place, the source, the report form and the global study rules of one topic.
**Fact, interpretation, supposition, reasoning**
The claim types of `stoplight`: green when the source strongly supports it, yellow when it is the user's rework, red when it is strong for the user and weak in the source. A reasoning derives a new claim from existing ones.

## Contracts

**Contract**
A readable document about one part of the system, written in simple language and shown mostly through diagrams and tables, plus the clauses it imposes on the files it enforces. It has a fixed header (`name`, `implements`, `enforces`, and `root: yes` on a root) and five sections in a fixed order: Purpose, View, Clauses, Verification, Notes (optional). Only these are rigid; the content inside is free. It leaves no grey zone: everything the parts do or expose is covered by a clause or declared out of the contract. Design decisions are part of the contract at the right abstraction level, never standalone documents. A contract made only of headings and a few lines is a defect.
_Avoid_: spec (a spec file is any skill's input; a contract is specifically documentation with obligations).
**Enforced file**
A file or folder a leaf contract binds, listed in its `enforces` field so a person or an agent can navigate from the contract to what it governs. Enforced files never point back to their contract.
**Name**
How clauses and tickets are identified: at most 3 words joined by `_`, in the language of the project, describing what they mean. Never a number. A clause name is unique in its contract, a ticket name in the project.
**Verification**
How a clause is proven: one row per clause in the Verification section, with a type from a closed list (`unit`, `interface`, `integration`, `end-to-end`, `script`, `ai-check`, `covered-by`; a project may add more) and a file in the tests folder chosen at setup. Scripts are deterministic and pass on exit code 0; `ai-check` is a check file judged by the model with cited evidence, used only when no script can decide; `covered-by` names the clauses of enforced contracts that satisfy a clause of a root or intermediate contract. A clause with no verification is not accepted.
**Clause**
A single checkable fact a contract imposes on its enforced files, precise enough to leave no grey zone. Coarse at high levels, exact at the leaves. Referenced as `<contract id>#<clause name>`; tickets point to the clause violated.
**Contract tools**
The one script, `contract-tools.py` in the tests folder, that does everything a script can decide: `lint`, `verify`, and the commands that write tickets, clauses, edges, scope and handoff. Agents write prose; every structured part goes through it, and each editing command ends by running the lint.
**Contract lint**
The `lint` command of contract-tools. It checks the rigid parts of the template (header, graph, sections, names, verification rows, stale verification files, size), every reference in contracts and tickets (links, paths, `contract#clause`, `file:line`), coverage of the contracted domain by leaf contracts (`ZONE`), and tickets (format, log, states). It regenerates the links block of every contract and `contracts/INDEX.md`. A contract that fails it goes to contract refinement before any other check.
**Stub**
A verification created by `clause add` that fails until it is written ("not written yet"). It makes a clause with no code or no check yet visible as a failing clause with a ticket, never a silent gap.
**Sweep**
`ticket sweep`, run at the start of every parity check: closes as `obsolete` the tickets whose clause is gone, as `resolved` the code tickets whose verification now passes, and reopens the resolved ticket whose verification fails again.
**Workspace**
The single folder where a workflow keeps its contracts, tickets and handoffs, together with a README explaining the flow, the formats and the configuration. Its location, and that of the tests folder, are always chosen at setup.
**Contract graph**
All contracts of a project, in one flat folder, linked as a directed acyclic graph by two header fields written on both sides of every edge: `implements` (the parent contracts, none on a root) and `enforces` (the child contracts, or for a leaf the files). A contract can have several parents, so a shared requirement (security, quality) is written once as its own contract. A contract's ID is its file name without `.md` (e.g. `auth_session`).
**Root**
A contract with `root: yes`: it implements nothing and enforces contracts or files. A project can have several.
**Leaf**
A contract that enforces only files of the project, never contracts. A contract enforces files or contracts, never both. Coverage is measured on leaves.
**Intermediate contract**
A contract that implements parents and enforces only contracts.
**Orphan**
A contract with no parent that is not a root. The lint rejects it; it exists only while building bottom-up, until a parent is added.

**Abstraction level**
How far a contract is from the roots: computed by the lint as the longest chain of `implements` upwards, never written or named, and shown in `contracts/INDEX.md`. Deeper contracts are more detailed and cover less. Because a contract may have several parents, the level is a property of the graph, not of a folder. A contract too large to read in one go is split into an overview and contracts that take the detail.
**Contracted domain**
The part of the codebase that is governed by contracts. Code outside it is ignored by parity checks.

**Uncontracted zone**
A file inside the contracted domain, not excluded, that no leaf contract enforces. Found mechanically by comparing the file list with all enforced files, announced whenever found, with a proposal to contract it.
**Notes**
The optional last section of a contract, listing each term, function or name used in it whose meaning the text does not explain.
**Reverse contracting**
Writing one contract from listed sources (code, documents, contracts): every source read, every responsibility documented, every clause given a verification. Repeated for each part of a repository, then grouped under parents by `recontract`.
**Statement check**
While contract-flow is active, every statement the user makes about how the system works or should work is compared with the contracts and with the code they enforce. If the code agrees with the contract, the user is corrected; if it agrees with the user, the contract is outdated and gets refined; otherwise the user decides. Missing coverage is announced as an uncontracted zone. Any difference found, accepted or postponed, becomes a ticket at once.
**Parity**
The state where a contract and what it covers agree 1:1. Checked contract ↔ the contracts it enforces (their written clauses cover its clauses) and, for leaf contracts, contract ↔ code. Gaps, outdated contracts and off-template contracts are not parity problems: they are solved by refinement. A higher-level contract cares only that its own statements hold, not how lower levels achieve them; verifying it may still require inspecting everything beneath it.

**Ticket**
A discrepancy between a contract and the code, recorded the moment any skill or the statement check finds it, without asking. Identified as `T-<name>` (a name, see above). There is **one ticket per clause** for the whole life of the project: it is reopened, never duplicated. A ticket is written only with `contract-tools ticket`, which keeps a log of timestamped events (`opened`, `direction_changed`, `status_changed`, `reopened`, `note`) that the lint checks against the header. Implementing new work and fixing errors are both done by resolving tickets. Each ticket has a direction, decided when it is created:
- **code**: the code must change to honour the contract.
- **contract**: the contract itself must change.
- **escalate**: a higher abstraction level must be re-examined first.

A ticket's status is one of:
- **open**: created when the discrepancy was found, not yet resolved. Can be reopened from any other status.
- **resolved**: the discrepancy is gone; the ticket's log says how.
- **rerouted**: could not be resolved without changing a contract; its direction changed and it went back to contract refinement.
- **obsolete**: a contract changed and the discrepancy no longer exists (set by the sweep, or by the user with a reason).

_Avoid_: issue, bug (those may exist in the project's own docs with other meanings).

**Scoped parity check**
A parity check limited to the contracts whose responsibility is affected by a change: the changed contract, all its descendants (through `enforces`) and all its ancestors (through `implements`, every parent). The change is known from the flow itself (contracts refined, files touched while resolving tickets) or stated by the user. Full checks of the whole graph are rare, because high-level contracts are coarse.

**Alarm**
The moment, while resolving a ticket, when the chosen solution turns out to cost substantially more (or differently) than estimated. By default work stops and a new set of weighed alternatives is proposed to the user; in autonomous mode the lowest-cost alternative is applied and logged instead.

**Recontracting**
Changing the structure of the contract graph: building it from requirements when there is no code yet, adding parents above contracts written from code, or merging, splitting, re-linking contracts and adding levels. Rare and broad.
**Refinement**
Changing the content of a few contracts for a specific task. Frequent and narrow.

**Stable project**
A project in which every contract passes the lint, every clause passes and no file is uncontracted.