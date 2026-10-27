# oleander-ai-toolkit

This is my personal collection of skills and workflows for AI coding assistants. Right now everything is built for Claude Code, but I write the content so it can be adapted to other tools (like Codex) later on.

There are two kinds of things in here:

- **Skills** (`skills/`) each do one job well. A skill tells the AI what it is supposed to do and which tools it can use.
- **Workflows** (`workflows/`) are step-by-step methods. They chain several skills together to get something bigger done.

If you want to write your own, start with [docs/conventions.md](docs/conventions.md). It's short.

## What's inside

| Name | Type | What it does |
|---|---|---|
| `mr-wolf` | skill | A calm, no-nonsense problem solver. It lays out your options with their trade-offs, waits for you to pick one, then gets it done in one go. |

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

Then open a new Claude Code session and type `/mr-wolf`.

## Update

```bash
cd ~/oleander-ai-toolkit
git pull
./setup.sh                 # Windows: powershell -ExecutionPolicy Bypass -File .\setup.ps1
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

- Rework `mr-wolf` so it attaches to a spec file, as described in the conventions.
- Publish the toolkit on the Claude Code plugin marketplace.
- Add support for other assistants, starting with Codex.
