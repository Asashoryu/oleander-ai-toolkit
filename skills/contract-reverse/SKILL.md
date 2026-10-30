---
name: contract-reverse
description: Write detailed contracts from existing code. Reads a part of the repository (or all of it) file by file and produces readable, complete contracts with tables and diagrams, every file covered, and a verification script or check file for every constraint. Use to contract existing code, an uncontracted zone, or a whole project that has code but no contracts.
---

# Contract reverse

Turns existing code into contracts. The code is the source of truth here: the contracts describe what it does today, in full, so that a person can understand the part without opening it.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Contract tree**, **Contract format** and **Verification** sections are binding. If there is no workspace, say so and stop.

The input is a scope: paths given by the invoker or the user, or the whole contracted domain.

## 1. Read everything in scope

List every file in scope that is not excluded (`git ls-files` where possible). Read each one. For each, note:
- what it is responsible for
- what it exposes (functions, classes, endpoints, commands, config keys, files written)
- what it depends on and what depends on it
- inputs, outputs, error cases, side effects, configuration
- rules it enforces (validations, limits, formats, invariants)

Also read existing contracts that already target files in scope, and the existing documentation listed in the configuration.

Do not summarise early. A file you skimmed is a file you will under-document.

## 2. Propose the tree

Group the files into contracts, from the coarsest part in scope down to leaves that a reader can study in one sitting. Show the user, without writing yet:

- the tree as an indented list of contract IDs, each with a one-line purpose and its targets
- where each new contract attaches to the existing tree (`realises`)
- a **coverage table**: every file in scope and the leaf contract that targets it. No file is left out; a file nobody should contract is proposed for **Excluded** in the configuration, with the reason.
- for each contract, its constraints (one line each) and the kind of verification proposed (`script` or `check`)

Prefer the split a reader would want: by responsibility, not by folder. Split a contract whenever it would exceed what the README calls one readable unit.

Ask the user to confirm or correct the tree. Do not grill on content: the code already answers that. Ask only about what the code cannot tell (intent, a behaviour that looks like a bug, what is meant to be public).

## 3. Write the contracts

For each contract, following the contract format:
- **Purpose** and **How it works** document everything collected in step 1 at this contract's level: every responsibility, flow, state, input, output, error and configuration. Use tables for fields, parameters, states and options; `mermaid` diagrams for flows, sequences and dependencies; trees for layouts.
- **Interface** lists everything exposed, as a table.
- **Constraints**: every rule the code actually enforces and every guarantee a caller relies on, each with its verification.
- **Notes**: every term, function or name used and not explained.

Where the code looks wrong (a likely bug, dead code, an inconsistency), write what it does, then list it for the user at the end. Never silently "fix" the contract to describe what it should do.

## 4. Write the verifications

For each constraint, create its file in the tests folder (`<contract id>/<constraint>.<ext>`):
- a `script` when a deterministic check is possible: a test against the code, a grep, a command, a static rule. It exits 0 on success and prints why on failure. Use the configured script runner.
- a `check` file otherwise, with what to look at, numbered criteria and when it fails.

Run every script once. Report the ones that fail: either the script is wrong (fix it) or the code breaks its own constraint (list it as a likely bug).

## 5. Hand over

List:
- contracts created, with the files each targets
- verifications created, and their result
- files proposed for exclusion
- likely bugs and open questions found in the code
