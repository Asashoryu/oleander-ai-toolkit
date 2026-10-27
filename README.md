# oleander-ai-toolkit

This is my personal collection of skills and workflows for AI coding assistants. Right now everything is built for Claude Code, but I write the content so it can be adapted to other tools (like Codex) later on.

There are two kinds of things in here:

- **Skills** (`skills/`) each do one job well. A skill tells the AI what it is supposed to do and which tools it can use.
- **Workflows** (`workflows/`) are step-by-step methods. They chain several skills together to get something bigger done.

If you want to write your own, start with [docs/conventions.md](docs/conventions.md). It's short.

## What's inside

| Name | Type | What it does |
|---|---|---|
| `contract-flow` | workflow | Keeps your code and its contracts in 1:1 parity: change contracts, check parity, open tickets, resolve them, repeat until the project is stable. Run it with `/contract-flow`. |
| `contract-init` | skill | Sets up the contract-flow workspace (contracts, tickets, handoffs) and explains how the flow works. |
| `recontract` | skill | Builds the whole contract tree from existing docs and code, or reorganises it. |
| `contract-refine` | skill | Changes a few contracts for a specific task, after grilling you on the change. |
| `parity-check` | skill | Compares contracts with their child contracts and code, and opens a ticket for each discrepancy. |
| `mr-wolf` | skill | A calm, no-nonsense problem solver. Picks up a ticket (or any implementation document), lays out options with their trade-offs, then gets it done in one go. |

`contract-flow` also needs two of Matt Pocock's skills, `grilling` and `handoff`, installed from [mattpocock/skills](https://github.com/mattpocock/skills).

The vocabulary used across these skills is defined in [CONTEXT.md](CONTEXT.md).

## Installation

Ubuntu:

```bash
cd ~
git clone https://github.com/asashoryu/oleander-ai-toolkit.git
cd oleander-ai-toolkit
./setup.sh
```

Windows (PowerShell):

```powershell
cd ~
git clone https://github.com/asashoryu/oleander-ai-toolkit.git
cd oleander-ai-toolkit
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

Then open a new Claude Code session and type `/contract-flow`.

## Update

```bash
~/oleander-ai-toolkit/setup.sh --update   # Windows: powershell -ExecutionPolicy Bypass -File ~\oleander-ai-toolkit\setup.ps1 -Update
```

## Uninstall

```bash
cd ~/oleander-ai-toolkit
./setup.sh --uninstall     # Windows: powershell -ExecutionPolicy Bypass -File .\setup.ps1 -Uninstall
cd ~ && rm -rf ~/oleander-ai-toolkit   # Windows: cd ~; Remove-Item -Recurse -Force oleander-ai-toolkit
```

## Adding your own skill or workflow

1. Create a folder `skills/<name>/` or `workflows/<name>/` with a `SKILL.md` inside. For workflows, there's a ready-made template in [docs/authoring-workflows.md](docs/authoring-workflows.md).
2. Give it a unique name and use that same name for the folder and for the `name:` field at the top of the file.
3. Run the setup again.

## What's next

- Publish the toolkit on the Claude Code plugin marketplace.
- Add support for other assistants, starting with Codex.
