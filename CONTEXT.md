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
A single verifiable statement in a contract, with a stable ID (e.g. `§1.2`). Free-form at high levels, increasingly precise (EARS, Given/When/Then) towards the leaves. Child contracts declare which parent clauses they realise; tickets point to the clause violated.

**Workspace**
The single folder where a workflow keeps its contracts, tickets and handoffs, together with a README explaining the flow and how to resume it. Its location is chosen at setup.

**Contract tree**
All contracts of a project, kept in one contracts folder with one subfolder per abstraction level. Each contract has exactly one parent, except the root.

**Abstraction level**
How far a contract is from the code. Higher levels are vaguer and cover more; lower levels are precise and cover less. The number and names of levels are chosen per project and can change.

**Contracted domain**
The part of the codebase that is governed by contracts. Code outside it is ignored by parity checks.

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

**Scoped parity check**
A parity check limited to the contracts whose responsibility is affected by a change: the changed contract, its subtree and its ancestors. Full checks of the whole tree are rare, because high-level contracts are coarse.
_Avoid_: issue, bug (those may exist in the project's own docs with other meanings).

**Alarm**
The moment, while resolving a ticket, when the chosen solution turns out to cost substantially more (or differently) than estimated. By default work stops and a new set of weighed alternatives is proposed to the user; in autonomous mode the lowest-cost alternative is applied and logged instead.

**Recontracting**
Reorganising the contract tree as a whole: creating it from scratch out of existing docs and code, or moving, merging, splitting contracts and changing levels. Rare and broad.

**Refinement**
Changing the content of a few contracts for a specific task. Frequent and narrow.

**Stable project**
A project in which every contract at every level is in parity.
