---
name: contract-reverse
description: Write one detailed contract from sources you list (code files, existing documents, other contracts). Reads every source, then produces a readable, complete contract in the fixed template, shown with diagrams and tables, with a verification for every clause. Repeat it for each part of a repository, then group the results with recontract. Use to contract existing code, an uncontracted zone, or documentation that should become a contract.
---

# Contract reverse

Turns a list of **sources** into **one** contract. The sources are the source of truth here: the contract describes what they say or do today, in full, so that a person can understand the part without opening them. To cover a larger part of a repository, the flow calls this skill once per part, and then `recontract` groups the resulting contracts under parents.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Names**, **Contract graph**, **Contract format** (with **Verification** and **Lint**) sections are binding. If there is no workspace, say so and stop.

The input is a list of sources given by the invoker or the user: code files or folders, documents (existing documentation can be copied or adapted as the base), or other contracts. If the list is empty, ask for it. If it is too large for one readable contract, propose how to split it into several and run once per part.

## 1. Read every source

Read each one. For code, note:
- what it is responsible for
- what it exposes (functions, classes, endpoints, commands, config keys, files written)
- what it depends on and what depends on it
- inputs, outputs, error cases, side effects, configuration
- rules it enforces (validations, limits, formats, invariants)

For documents, note the requirements and decisions they state, and check them against the code they describe. Also read contracts that already enforce the same files, and the existing documentation listed in the configuration.

Do not summarise early. A source you skimmed is a source you will under-document.

## 2. Propose the contract

Show the user, without writing yet:
- the contract's ID, name, one-line purpose, and the contracts it should `implement` (existing ones; if none fits yet it stays an orphan until `recontract` adds a parent)
- the files it will enforce (a leaf enforces only files). A file nobody should contract is proposed for **Excluded** in the configuration, with the reason.
- its clauses (name and one line each) and the verification type proposed for each (`unit`, `interface`, `integration`, `end-to-end`, `script` or `ai-check`)

Do not grill on content: the sources already answer that. Ask only about what they cannot tell (intent, a behaviour that looks like a bug, what is meant to be public).

## 3. Write the contract

Following the contract format (fixed header with `implements` and `enforces`, then Purpose, View, Clauses, Verification, Notes):
- Create the skeleton with `contract-tools contract new <id> --name <name> --implements <parents> --enforces <files>`; it writes both sides of every edge. Write the prose; add each clause with `clause add` (no `--ticket`: the code already exists).
- First list, from step 1, every responsibility, entry point, input, output, error case and configuration at this contract's level. This list is the grey-zone check: each item gets a clause, or is declared out of the contract with the reason.
- **Purpose**: 2-4 lines.
- **View**: document everything collected at this level, shown rather than told: `mermaid` diagrams for flows, sequences, states and dependencies; tables for fields, parameters, options and interface; trees for layouts. Simple words. Few entries, each useful.
- **Clauses**: one named clause (at most 3 words, in the language of the project) for every rule the sources actually enforce and every guarantee a caller relies on.
- **Verification**: one row per clause, with its type, what it proves and its file.
- **Notes**: only if a term, function or name is used and not explained.
- If it implements existing parents, add this contract to the `enforces` of each of them, and cover any of their clauses it satisfies (`covered-by`), so both sides of the edge are written.

Where the code looks wrong (a likely bug, dead code, an inconsistency), write what it does, then open a ticket for it at once (`contract-tools ticket new`), so it cannot be forgotten, and list the tickets for the user at the end. Never silently "fix" the contract to describe what it should do.

## 4. Write the verifications

For each clause, create its file in the tests folder (`<contract id>/<clause name>.<ext>`), of the type declared in the contract:
- `unit`, `interface`, `integration`, `end-to-end` or `script` when a deterministic check is possible. It exits 0 on success and prints why on failure. Use the configured script runner.
- `ai-check` only when no script can decide: a check file with what to look at, numbered criteria and when it fails.

Run every script once. Report the ones that fail: either the script is wrong (fix it) or the code breaks its own clause (list it as a likely bug).

Then run `contract-tools lint` (see **Lint** in the README). Do not hand over while it reports a problem other than an orphan. Add the contract to the scope: `contract-tools scope add <id>`.

## 5. Hand over

List:
- the contract created, with the files it enforces and the parents it implements (or that it is an orphan)
- verifications created, and their result
- files proposed for exclusion
- likely bugs and open questions found in the code
