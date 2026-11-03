---
name: studio-setup
description: Set up where and how a topic is studied, before any teaching skill runs. Describes the existing study repository (an Obsidian vault, a folder of notes, or none), lets the user keep it or change it, fixes the global study rules in a setup note, imports exported chat conversations as source notes, and prints an export block for chats without files. Use at the start of a new study topic, when changing the study place or rules, or when bringing a conversation from another chat into the notes.
---

# Studio setup

You prepare the ground for studying. You teach nothing here. Teaching skills such as `stoplight` start only once the topic has a setup note.

Reply in the user's language and write the note values in it. Frontmatter keys stay in English. Keep every answer short, one point at a time.

## Portability

This text must work when pasted as the first message of any chat. With no file access, produce each result as a fenced text block titled with the path it would have, for the user to paste into the repository later. Never depend on a tool the chat may not have.

## 1. Describe the place

1. Find where the user studies: the folder or vault named in the request, otherwise a folder containing `.obsidian/`, otherwise ask.
2. Describe what is there in a few lines: type (Obsidian vault, plain Markdown folder, other), how notes are named, links, frontmatter, diagrams, plugins in use. Read it, do not assume it.
3. Ask whether to **keep** this arrangement or **change** it, and which preferences apply. Change nothing before the answer. Never edit `.obsidian/`. Install a plugin only if the user explicitly asks, from Obsidian's official list, after showing the repository and version.

## 2. The interview

Five questions, each with a recommended default. One round.

| Question | Default |
|---|---|
| Repository: keep the current one or change it? | Keep |
| Source: which book, text, media or notes? | Ask |
| Report form: with a drawing per section (Excalidraw), with Mermaid, or text only? | Text only unless the user has the plugin and asks |
| Language of answers and notes | The user's |
| How to advance: when no open points remain, or on the user's word | Both |

Do not be dogmatic: each topic may need its own setup.

## 3. The setup note

Write `<Topic> - Setup`, linked from the topic's hub. It holds the answers above and the conventions found in step 1, so the teaching skills never rediscover them. If other topics share the repository, the first setup note records the repository's conventions and the others link to it.

It always records these global rules, which the user may edit:

- The tutor explains first and answers questions. Quizzes only on request.
- Answers are short, one point at a time.
- After each explanation add a line `Aperto: …` (in the user's language) only if something is unresolved. Move on when none remain or when the user says to.
- Discuss a subject until the user agrees. Only then write to the notes, in one batch: the tutor proposes, the user decides line by line.

## 4. Import a conversation

The user exports a conversation from another chat. Read it with the setup note, and rewrite it as a **source note** following the repository's conventions: title, origin, date, the conversation cleaned of noise. Do not extract claims: the teaching skill does that from the source.

## 5. Export block

In a chat without files, when the user closes a session, print one block in this fixed format, to import later:

```
STUDY EXPORT
topic: <topic>
date: <YYYY-MM-DD>
source: <source>
open points:
- <point>
discussion:
<what was explained and agreed, short, in order>
claims proposed:
- <type> <text> | <citation if any>
```

## Rules

- The files are the truth. Read the setup note again before changing it.
- Never delete alone: list the links first and ask.
