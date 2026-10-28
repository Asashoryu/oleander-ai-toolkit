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
A document, written to be read, processed and verified by both a person and an LLM, stating what a part of the system must achieve without prescribing how. Its form varies (a spec, a set of ADRs, a PRD…); what makes it a contract is that it points explicitly to what it covers and its statements can be checked.
Design decisions (ADRs) are part of a contract at the right abstraction level, never standalone documents outside the contract tree.
_Avoid_: spec (a spec file is any skill's input; a contract is specifically an obligation).

**Target**
Something a contract covers: a child contract, code, or any other path. Every contract must list its targets explicitly, so a person or an agent can navigate from it to what it governs. Targets never point back to their contract.

**Test**
Ordinary code with no special status. Tests exist only where a contract requires them, and are covered by their own contracts like any other code.

**Clause**
A single verifiable statement in a contract, with a stable ID and a verification method. Clauses are preconditions (`§R…`, what the part requires), postconditions (`§E…`, what it ensures) or invariants (`§I…`, what always holds). Coarse at high levels, precise at the leaves. Child contracts declare which parent clauses they realise; tickets point to the clause violated.

**Workspace**
The single folder where a workflow keeps its contracts, tickets and handoffs, together with a README explaining the flow and how to resume it. Its location is chosen at setup.

**Contract tree**
All contracts of a project, nested by folder: the children of `x.md` live in the folder `x/` next to it. A contract's ID is its path without `.md` (e.g. `system/auth/session`). Each contract has exactly one parent, except the root.

**Abstraction level**
How far a contract is from the code: its depth in the contract tree. Deeper contracts are more precise and cover less. Branches can have different depths; levels are never numbered or named.

**Contracted domain**
The part of the codebase that is governed by contracts. Code outside it is ignored by parity checks.

**Uncontracted zone**
Code or resources inside the contracted domain that no contract targets. Allowed, but announced whenever found, with a proposal to contract it.

**Verification method**
How a clause is proven: `inspection` (reading, with cited evidence; the default), `test`, `static` (a tool such as a type checker or linter), `command` (a command whose result proves it) or `review` (only a person can confirm it).

**Verification contract**
A leaf contract whose targets are the tests or checks that prove other contracts' clauses. Required whenever a clause is verified by `test`.

**Statement check**
While contract-flow is active, every statement the user makes about how the system works or should work is checked against the contracts targeting it: contradictions are pointed out, new information leads to a proposed refinement, missing coverage is announced as an uncontracted zone.

**Parity**
The state where a contract and what it covers agree 1:1. Checked contract ↔ child contracts and, for leaf contracts, contract ↔ code. A higher-level contract cares only that its own statements hold, not how lower levels achieve them; verifying it may still require inspecting everything beneath it.

**Ticket**
A discrepancy found by a parity check between a contract and one of its targets, including a clause that nothing realises yet. Implementing new work and fixing errors are both done by resolving tickets. Each ticket has a direction, decided when it is created:
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
Reorganising the contract tree as a whole: creating it from scratch out of existing docs and code, or moving, merging, splitting and re-nesting contracts. Rare and broad.

**Refinement**
Changing the content of a few contracts for a specific task. Frequent and narrow.

**Stable project**
A project in which every contract in the tree is in parity.
