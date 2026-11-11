---
name: contract-handoff
description: Record where a contract-flow session stopped, as a handoff file in the workspace's handoff folder, so a new session can resume it. Use when the user stops the flow, when the project is stable, or when the user asks for a handoff of contract work.
---

# Contract handoff

Adapted from Matt Pocock's `handoff` skill, kept unchanged in [references/mattpocock-handoff.md](references/mattpocock-handoff.md). Same purpose (a fresh agent continues the work), with these changes:

| Matt Pocock's | Here |
|---|---|
| Saves to the OS temporary folder, never the workspace | Saves to `<workspace>/handoff/`, where `/contract-flow` step 1 reads it |
| Free-form summary | Fixed sections about the flow's state |
| Arguments describe the next session | Same; they tailor "Next" |

## Before starting

Find the workspace through the `Contract-flow workspace:` line in `CLAUDE.md`/`AGENTS.md`. If the line is missing, ask the user for the path. Never write the handoff anywhere else.

## Write the file

Run `contract-tools handoff --stopped-at "<step and number>" --why "<user stopped | project stable | blocked>" --decisions "<...>" --next "<...>" --skills "<...>"` from the project root. The tool writes `<workspace>/handoff/<YYYY-MM-DD-HHMM>.md` (never overwriting an earlier one: the most recent file is the one read on resume) and fills Scope from `scope.txt` and Tickets from the ticket files itself. You supply only the stopped-at, decisions, next and skills texts. The sections it writes, in order:

Sections, in this order:

1. **Stopped at**: the flow step reached (name and number), and why it stopped (user stopped, project stable, blocked).
2. **Scope**: contracts changed and files touched in the session, as paths. This is the scope of the next parity check.
3. **Tickets**: open tickets by direction (`code`, `contract`, `escalate`) and any `rerouted`, each as its path. Do not copy their content.
4. **Decisions**: choices the user made that the contracts and tickets do not record, such as the Mr. Wolf mode or sequential vs parallel.
5. **Next**: what `/contract-flow` should offer first on resume. If the user passed arguments, tailor this to them.
6. **Suggested skills**: which skills the next session should invoke with the Skill tool.

## Rules

- Do not duplicate what is already in contracts, tickets, commits or diffs. Reference them by path.
- Redact secrets, credentials and personal data.
- Report the path of the file written.
