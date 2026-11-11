---
name: recontract
description: Build or reorganise the contract graph. Creates it from requirements and existing documents when there is no code yet, adds parents above contracts written from code (bottom-up), or merges, splits and re-links contracts and adds abstraction levels, after grilling the user on the proposal. Use for structural changes to contracts; to contract existing code, use contract-reverse.
---

# Recontract

Changes the **structure** of the contract graph: which contracts exist, which contracts each one `implements` and `enforces`, and which files the leaves enforce. Contracts live in one flat folder; relations are written only in the headers. Changing the content of a few contracts is out of scope; documenting existing code is the job of reverse contracting.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Names**, **Contract graph**, **Contract format** (with **Verification** and **Lint**) sections are binding. If there is no workspace, say so and stop.

If the request is to document code that exists but has no contracts, say that this is reverse contracting and stop.

## 1. Survey

Read:
- the existing contract graph (and `contracts/INDEX.md`), if any
- the existing documentation listed in the configuration
- the requirements the user gives
- the code structure, if any (to place enforced files, not to document it)

## 2. Draft a proposal

Propose, without writing anything yet:
- **Graph**: the contracts as a list of IDs (names as in **Names**), each with its kind (root, intermediate, leaf), a one-line purpose, the contracts it `implements` and what it `enforces`: contracts for roots and intermediates, files for leaves (planned files for code that does not exist yet). Draw it as a `mermaid` diagram. Give a contract several parents where one set of requirements (security, quality) applies to many; write it once as its own contract. Group where a reader would want to study a part separately.
- **New levels**: for every contract that has grown too large (see the README), the overview it keeps and the contracts that take the detail. When working bottom-up, the parents to add above existing leaves, to resolve orphans.
- **Clauses**: for each contract, its main clauses (name and one line), each with the verification type from the closed list: `covered-by` (naming the covering clauses) for roots and intermediates, the other types for leaves. A clause that cannot be verified is reworded or dropped.
- **Moves** (when reorganising): for each existing contract, whether it is kept, moved, merged, split or removed, and where each clause goes.
- **Coverage**: every existing file in the contracted domain and the leaf contract that will enforce it.

A contract that only restates its parent is not worth having; a contract too long to read in one go is not either. The lint rejects cycles and one-sided edges.

## 3. Grill the proposal

Invoke the `mattpocock-skills:grilling` skill on the proposal. Settle the roots first, then each branch downwards (or, bottom-up, the leaves first, then the parents above them). For a new project, grill until every contract has enough to be written in full: purpose, how it should work (what the View will show), interface, errors, configuration, with no grey zone. Do not write until the user confirms.

## 4. Write

- Create contracts with `contract-tools contract new`, and change the graph only with `contract-tools edge|files|root|contract rename|clause`, never by editing headers or tables by hand. Write each contract's prose following the contract format and its writing rules. Write each contract in full in the fixed template (header with `implements` and `enforces` on both sides of every edge, Purpose, View, Clauses, Verification, Notes), shown with tables and diagrams, in simple words, not as a list of headings: a thin contract is a defect.
- Add every new clause with `contract-tools clause add`; for code that does not exist yet use `--ticket <name>`, which creates the failing stub verification and opens its ticket at once. Write the real verification into the stub.
- When reorganising: keep the names of surviving clauses, move their verification files with them, and the tool updates every reference (`<contract id>#<clause>`), ticket and verification path on `contract rename` and `clause rename`. `clause remove` makes an open ticket on the clause `obsolete`. Add every contract touched to the scope.
- Run `contract-tools lint` (see **Lint** in the README); it rewrites the links blocks and `INDEX.md`. Do not finish while it reports a problem (orphans are expected only while building bottom-up, and are listed in the hand-over).

## 5. Hand over

List the contracts and verifications created, moved or removed.
