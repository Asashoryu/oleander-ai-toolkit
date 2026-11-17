# oleander-ai-toolkit

Skills and workflows for Claude Code. Terms are defined in [CONTEXT.md](CONTEXT.md), authoring rules in [docs/conventions.md](docs/conventions.md).

| Name | Type | Purpose |
|---|---|---|
| `contract-flow` | workflow | Keeps code and contracts in 1:1 parity. Run with `/contract-flow`. |
| `contract-init` | skill | Creates, configures and updates the contract-flow workspace. |
| `contract-reverse` | skill | Writes one detailed contract from listed sources (code, documents, contracts). |
| `recontract` | skill | Builds the contract graph from requirements, adds parents above contracts written from code, or reorganises it. |
| `contract-refine` | skill | Changes a few contracts for a task. |
| `parity-check` | skill | Runs the verifications, finds discrepancies and uncontracted files, opens tickets. |
| `contract-handoff` | skill | Records where a contract-flow session stopped, in the workspace, so it can resume. |
| `mr-wolf` | skill | Resolves a ticket or implementation document. |
| `compress` | skill | Compresses a source, or a part of it, into atoms of information with the same meaning in fewer words, automatically and completely, and lists the noise it discarded. Output: a JSON file. |
| `summarize` | skill | Tells all the atoms of a `compress` report as one narration, with the places as references, rendered as an HTML page. |
| `stoplight` | skill | Reorganises the atoms of a `compress` report into a graph of facts, interpretations and suppositions, finds the gaps of the source and proposes completions.
| `stoplight-live` | skill | Live mode of `stoplight`: the agent is concise and everything it writes carries its type F, I or S, until the user says "esci". No report. |

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
