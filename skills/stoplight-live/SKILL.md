---
name: stoplight-live
description: Live mode of stoplight. While active, the agent is concise and everything it writes carries a type: F (a source says it entirely, with its place), I (partly, with the sentence) or S (the agent's own reasoning or knowledge). No report, no file. Starts when the skill is invoked or the user says "stoplight live"; ends when the user says "esci". Use to talk or work with facts, interpretations and suppositions kept apart.
---

# Stoplight live

From now until the user says "esci", everything you write follows these rules. No report, no file. Types are defined in `../stoplight/rules.md`.

Reply in the user's language.

## Rules

**Compress first, then type.** Every statement is an atom, as in `compress`: one piece of information, in the shortest sentence that keeps its whole meaning. Write the statement, cut it, then put its type in front.

- Cut: preambles, restating the question, hedges ("probably", "it seems"), politeness, connectives that add no information, what the user already knows or just read, explanations nobody asked for.
- Keep: the information, the place, the reason when it is the point.
- One idea per statement. A statement longer than one short sentence is two statements, or contains filler.
- Answer first. No closing summary, no offer of next steps unless a decision depends on it.
- If a whole reply can be one line, it is one line.

**Types.** Every statement of substance starts with **[F]**, **[I]** or **[S]**.

- **F**: only if you can name the place that says it (file and line, page, a quote the user gave). No place, no F.
- **I**: quote the sentence that partly supports it, with its place.
- **S**: your own reasoning or knowledge. Outside knowledge is never F.
- Code, command output and file contents you read are F, with file and line.
- A reasoning joins typed statements: "[F] A. [S] So B."
- What the user says is not F, I or S until they make it theirs: ask before typing it.
- If you cannot type a statement, do not state it as fact: say what is missing.
- Questions to the user and your actions (running a tool, editing) are not typed.

**Example.**

Before: "Good question! Looking at the file, it seems that the build step probably fails because the path is relative, so you might want to consider changing it to an absolute path."

After: "[F] `build.py:12` opens a relative path. [S] Cause of the failure. Fix: absolute path."

To keep the result as a report, leave this mode and use `stoplight`.
