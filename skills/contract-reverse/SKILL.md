---
name: contract-reverse
description: Write detailed contracts from existing code. Reads a part of the repository (or all of it) file by file and produces readable, complete contracts in the fixed template, shown with diagrams and tables, every file covered, and a verification for every clause. Use to contract existing code, an uncontracted zone, or a whole project that has code but no contracts.
---

# Contract reverse

Turns existing code into contracts. The code is the source of truth here: the contracts describe what it does today, in full, so that a person can understand the part without opening it.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Names**, **Contract tree**, **Contract format** (with **Verification** and **Lint**) sections are binding. If there is no workspace, say so and stop.

The input is a scope: paths given by the invoker or the user, or the whole contracted domain.

## 1. Read everything in scope

List every file in scope that is not excluded (`git ls-files` where possible). Read each one. For each, note:
- what it is responsible for
- what it exposes (functions, classes, endpoints, commands, config keys, files written)
- what it depends on and what depends on it
- inputs, outputs, error cases, side effects, configuration
- rules it enforces (validations, limits, formats, invariants)

Also read existing contracts that already enforce files in scope, and the existing documentation listed in the configuration.

Do not summarise early. A file you skimmed is a file you will under-document.

## 2. Propose the tree

Group the files into contracts, from the coarsest part in scope down to leaves that a reader can study in one sitting. Show the user, without writing yet:

- the tree as an indented list of contract IDs, each with a one-line purpose and its enforced files
- where each new contract attaches to the existing tree (`realizes`)
- a **coverage table**: every file in scope and the leaf contract that enforces it. No file is left out; a file nobody should contract is proposed for **Excluded** in the configuration, with the reason.
- for each contract, its clauses (name and one line each) and the verification type proposed for each (`unit`, `interface`, `integration`, `end-to-end`, `script` or `ai-check`)

Prefer the split a reader would want: by responsibility, not by folder. Split a contract whenever it would exceed what the README calls one readable unit.

Ask the user to confirm or correct the tree. Do not grill on content: the code already answers that. Ask only about what the code cannot tell (intent, a behaviour that looks like a bug, what is meant to be public).

## 3. Write the contracts

For each contract, following the contract format (fixed header, then Purpose, View, Clauses, Verification, Notes):
- First list, from step 1, every responsibility, entry point, input, output, error case and configuration at this contract's level. This list is the grey-zone check: each item gets a clause, or is declared out of the contract with the reason.
- **Purpose**: 2-4 lines.
- **View**: document everything collected at this level, shown rather than told: `mermaid` diagrams for flows, sequences, states and dependencies; tables for fields, parameters, options and interface; trees for layouts. Simple words. Few entries, each useful.
- **Clauses**: one named clause (at most 3 words, in the language of the project) for every rule the code actually enforces and every guarantee a caller relies on.
- **Verification**: one row per clause, with its type, what it proves and its file.
- **Notes**: only if a term, function or name is used and not explained.

Where the code looks wrong (a likely bug, dead code, an inconsistency), write what it does, then list it for the user at the end. Never silently "fix" the contract to describe what it should do.

## 4. Write the verifications

For each clause, create its file in the tests folder (`<contract id>/<clause name>.<ext>`), of the type declared in the contract:
- `unit`, `interface`, `integration`, `end-to-end` or `script` when a deterministic check is possible. It exits 0 on success and prints why on failure. Use the configured script runner.
- `ai-check` only when no script can decide: a check file with what to look at, numbered criteria and when it fails.

Run every script once. Report the ones that fail: either the script is wrong (fix it) or the code breaks its own clause (list it as a likely bug).

Then run `contract-lint.py` (see **Lint** in the README). Do not hand over while it reports a problem.

## 5. Hand over

List:
- contracts created, with the files each enforces
- verifications created, and their result
- files proposed for exclusion
- likely bugs and open questions found in the code
