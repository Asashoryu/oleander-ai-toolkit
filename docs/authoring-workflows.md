# Authoring workflows

A workflow is a `SKILL.md` in `workflows/<name>/` that drives several skills in order. Copy this template:

```markdown
---
name: <workflow-name>
description: Workflow: <what larger goal it achieves>. Use when <trigger>.
---

# <Workflow title>

## Skills used
- `<skill-a>` — <why>
- `<skill-b>` — <why>

## Spec file
<Where this workflow keeps its spec/state file, and how it passes it to each skill.>

## Steps

### 1. <Step name>
- **Entry:** <condition to start this step>
- **Invoke:** `<skill-a>` with spec `<path>`
- **Output:** <what this step produces>
- **Checkpoint:** stop and ask the user | continue automatically

### 2. <Step name>
...
```
