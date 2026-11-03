# oleander-ai-toolkit

Skills and workflows for Claude Code. Terms are defined in [CONTEXT.md](CONTEXT.md), authoring rules in [docs/conventions.md](docs/conventions.md).

| Name | Type | Purpose |
|---|---|---|
| `contract-flow` | workflow | Keeps code and contracts in 1:1 parity. Run with `/contract-flow`. |
| `contract-init` | skill | Creates the contract-flow workspace. |
| `contract-reverse` | skill | Writes one detailed contract from listed sources (code, documents, contracts). |
| `recontract` | skill | Builds the contract graph from requirements, adds parents above contracts written from code, or reorganises it. |
| `contract-refine` | skill | Changes a few contracts for a task. |
| `parity-check` | skill | Runs the verifications, finds discrepancies and uncontracted files, opens tickets. |
| `contract-handoff` | skill | Records where a contract-flow session stopped, in the workspace, so it can resume. |
| `mr-wolf` | skill | Resolves a ticket or implementation document. |
| `studio-setup` | skill | Sets up where and how a topic is studied, fixes the study rules, imports exported chat conversations. |
| `stoplight` | skill | Study method: facts, interpretations and suppositions linked by reasonings, written in batch after discussion. |

**Requires** Matt Pocock's `mattpocock-skills:grilling` skill ([mattpocock/skills](https://github.com/mattpocock/skills)).

## Install

```bash
git clone https://github.com/asashoryu/oleander-ai-toolkit.git ~/oleander-ai-toolkit
~/oleander-ai-toolkit/setup.sh                                    # global: ~/.claude/skills
~/oleander-ai-toolkit/setup.sh --target <project>/.claude/skills  # single project
```

On Windows run `powershell -ExecutionPolicy Bypass -File ~\oleander-ai-toolkit\setup.ps1`, with `-Target`, `-Copy`, `-Update`, `-Uninstall`.

| Option | Effect |
|---|---|
| `--copy` | Copy instead of link. Use it for projects shared through git: links point to your local clone. |
| `--update` | `git pull`, then reinstall. |
| `--uninstall` | Remove only what the script installed. |

The script also lists what it installed in a marked block of the matching `CLAUDE.md` (`~/.claude/CLAUDE.md`, or `<project>/CLAUDE.md`), so Claude knows the workflows exist. The rest of the file is left untouched.

Update and uninstall need the same `--target` used to install. With links, don't move or delete the clone.
