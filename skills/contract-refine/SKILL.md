---
name: contract-refine
description: Change the content of a few contracts for a specific task (a new requirement, a correction, a contract or escalate ticket), after grilling the user on the change, keeping the documentation complete and every constraint verified. Use whenever what a contract says, constrains or targets needs to change during normal work.
---

# Contract refine

Changes what a few contracts say. Reorganising the tree (moving, splitting, re-nesting, adding levels) is out of scope.

## Before starting

Read the workspace `README.md` (find it through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`). Its **Contract format** and **Verification** sections are binding.

## 1. Understand the input

The input is one of:
- a **requirement** or statement from the user (new, changed or removed behaviour)
- one or more **tickets** with direction `contract`, `escalate` or status `rerouted`
- an outdated contract found to disagree with code that is right

Find the contracts involved and read them with their targets. For an `escalate` ticket, start from the contract it `realises` and keep climbing while the problem is really decided higher up.

## 2. Grill the change

Invoke the `grilling` skill. Settle, for each contract involved:
- what changes in the documentation (**How it works**, **Interface**, **Notes**), not only in the constraints
- which constraints are added, reworded or removed, and how each is verified (`script` or `check`)
- whether contracts that `realise` it must change too (list them)
- whether the contract becomes too large and needs a new level, or the change is otherwise structural: then stop and say so

Work from the highest affected contract downwards. Do not write until the user confirms.

## 3. Write

- Edit the contracts following the contract format and its writing rules: update the prose, tables and diagrams so the contract still documents its targets completely. Never renumber surviving constraints.
- Create, change or delete the verification files of the constraints touched.
- Keep `targets` and `realises` accurate.
- For each input ticket, append a log line saying what changed, and set it to `resolved` if the contract change removes the discrepancy. Set to `obsolete` any other open ticket whose constraint no longer exists.

## 4. Hand over

List the contracts and verifications changed.
