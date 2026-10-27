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

It takes about five minutes, even if you're starting from scratch.

### 1. What you need

- **Claude Code.** If you don't have it yet, follow the [official guide](https://docs.claude.com/en/docs/claude-code).
- **Git**, to download the repository:
  - on Ubuntu: `sudo apt update && sudo apt install -y git`
  - on Windows: `winget install --id Git.Git -e` (open a new terminal afterwards so it shows up)

That's it. The repository is public, so you don't need a GitHub account.

### 2. Download the repository

Put it somewhere you'll keep it. The setup links your skills to this folder, so if you move or delete it later, the skills stop working.

On Ubuntu:

```bash
mkdir -p ~/src && cd ~/src
git clone https://github.com/asashoryu/oleander-ai-toolkit.git
cd oleander-ai-toolkit
```

On Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force "$HOME\src" | Out-Null; Set-Location "$HOME\src"
git clone https://github.com/asashoryu/oleander-ai-toolkit.git
Set-Location oleander-ai-toolkit
```

### 3. Run the setup

The setup script puts every skill and workflow where Claude Code looks for them (`~/.claude/skills`). It won't touch anything you already had there.

On Ubuntu:

```bash
chmod +x setup.sh   # only needed the first time
./setup.sh
```

On Windows (PowerShell):

```powershell
.\setup.ps1
```

If Windows complains that "running scripts is disabled on this system", run it like this instead:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

By default the script creates **links**, so any change in the repository shows up in Claude right away. If you'd rather have a frozen copy, use `./setup.sh --copy` (or `.\setup.ps1 -Copy` on Windows).

Only want one skill? Copy its folder (for example `skills/mr-wolf`) into `~/.claude/skills/` and you're done.

### 4. Make sure it works

Start a new Claude Code session and type `/mr-wolf`. If Mr. Wolf answers, you're all set.

## Staying up to date

```bash
cd ~/src/oleander-ai-toolkit   # Windows: Set-Location "$HOME\src\oleander-ai-toolkit"
git pull
./setup.sh                     # Windows: .\setup.ps1
```

If you installed with links, `git pull` already updates the skills you have. Run the setup again only to pick up new ones. If you installed with `--copy`, run the setup every time.

## Removing it

Run `./setup.sh --uninstall` (on Windows: `.\setup.ps1 -Uninstall`). This removes only what the toolkit installed. After that you can delete the folder.

## Adding your own skill or workflow

1. Create a folder `skills/<name>/` or `workflows/<name>/` with a `SKILL.md` inside. For workflows, there's a ready-made template in [docs/authoring-workflows.md](docs/authoring-workflows.md).
2. Give it a unique name and use that same name for the folder and for the `name:` field at the top of the file.
3. Run the setup again.

## What's next

- Rework `mr-wolf` so it attaches to a spec file, as described in the conventions.
- Publish the toolkit on the Claude Code plugin marketplace.
- Add support for other assistants, starting with Codex.
