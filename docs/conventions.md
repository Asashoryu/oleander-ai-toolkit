# Conventions

## Skills vs workflows

- **Skill** (`skills/<name>/SKILL.md`): one capability — what the AI does and which tools it uses.
- **Workflow** (`workflows/<name>/SKILL.md`): a step-by-step method that orchestrates several skills toward a larger goal. Same file format as a skill. See [authoring-workflows.md](authoring-workflows.md).

Both are installed into the same skills directory, so **names must be unique across `skills/` and `workflows/`**. The folder name must equal the `name` in frontmatter.

## Spec file contract

Skills never hardcode where they read or write state. They attach to a **spec file**:

1. **Invoked by a workflow** — the workflow step names the spec file (e.g. "invoke `mr-wolf` with spec `docs/specs/auth.md`").
2. **Invoked standalone** — use the file the user referenced (`@file`). If none, ask once: "Which spec file should I attach to?" and suggest `SPECS.md` in the project root. Never create one silently.

## Tool neutrality

Write skill content without Claude-only assumptions where possible, so it can later be adapted for other agents (e.g. Codex). Tool-specific packaging goes in its own folder, not in skill content.
