# oleander-ai-toolkit

Skills and workflows for Claude Code. Terms are defined in [CONTEXT.md](CONTEXT.md), authoring rules in [docs/conventions.md](docs/conventions.md).

| Name | Type | Purpose |
|---|---|---|
| `contract-flow` | workflow | Keeps code and contracts in 1:1 parity. Run with `/contract-flow`. |
| `contract-init` | skill | Creates the contract-flow workspace. |
| `recontract` | skill | Builds or reorganises the whole contract tree. |
| `contract-refine` | skill | Changes a few contracts for a task. |
| `parity-check` | skill | Finds contract/code discrepancies and opens tickets. |
| `mr-wolf` | skill | Resolves a ticket or implementation document. |

**Requires** Matt Pocock's `grilling` and `handoff` skills ([mattpocock/skills](https://github.com/mattpocock/skills)).

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
