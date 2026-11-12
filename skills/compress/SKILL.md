---
name: compress
description: Condense what a user understands from a source into a standard report, by discussion. The user asks, the skill answers and proposes condensations, sorting each piece into kept, noise or lost; the report shrinks by iterations and records what is still untreated. The report is a JSON file rendered as one HTML page by a visualization (sintesi by default, stoplight for facts, interpretations and suppositions). Use to study a book, text or conversation in depth, or to condense a long Markdown source.
---

# Compress

The goal is the user's understanding. Compression follows it: what has been discussed is condensed, what has not stays aside.

Reply in the user's language. Frontmatter and JSON keys stay in English.

## Rules

- Explain first and answer questions. Quizzes only on request.
- Answers are short, one point at a time. Point out where the source says something and where you are reconstructing.
- After an explanation add `Aperto: …` only if something is unresolved.
- Discuss until the user agrees. Only then write, in one batch: you propose, the user decides line by line.
- An objection from the user is not information until the user makes it theirs.

## Sorting

Every piece of the source ends in one of three places:

| Outcome | Meaning |
|---|---|
| **Kept** | Information that stays in the report. |
| **Noise** | Does not carry information (the author's afternoon wine). Discarded with a one-line reason. |
| **Lost** | Information the user accepts to sacrifice. Lossy mode only. |

The default is lossless: `lost` stays empty. The user decides what is noise and what is information.

## The report

One file `<Source> - Condensato.json` next to the source, overwritten at every iteration (the repository holds the history). Without file access, print it as a fenced block titled with that path.

```json
{"title": "", "date": "YYYY-MM-DD",
 "sources": [{"name": "", "path": "relative path, optional"}],
 "not_treated": ["parts of the source not yet discussed"],
 "noise": [{"text": "", "reason": ""}],
 "lost": [{"text": ""}],
 "visualization": "sintesi",
 "data": {}}
```

`data` follows the schema of the chosen visualization, found in `visualizations/<name>/rules.md`: its keys, nesting and writing rules live there only. Read that file before writing. Available: `sintesi` (default: sections, timelines, key facts in a `scheda`, quotes) and `stoplight` (claims and reasonings). The user may change visualization between iterations: reorganise the kept information into the new schema, nothing else changes.

The `build` step also writes the page the user reads: an index, the text, a card with ratio, untreated parts and discards. Tell the user the path of the `.html` file when you show the ratio.

## An iteration

1. Read the existing report, or start one: list every part of the source in `not_treated`.
2. Say in one line which subject the iteration covers.
3. Explain and discuss, as in the rules, until no `Aperto` remains or the user says to go on.
4. Propose the batch: the new kept points, the noise with reasons, the lost with the user's consent. The user confirms, corrects or discards line by line.
5. Condense: write the kept information into `data`, in the shape the visualization asks (for `sintesi`: dated events into `timeline`, facts to know at a glance into `scheda`), shorten the points already there where the discussion allows, move the treated part out of `not_treated`.
6. Run `python3 tools/compress-tools.py build "<report>.json"` (path relative to this skill). It validates the report, writes the HTML next to it and prints source words, report words and ratio. Fix every error it prints, then show the ratio. Without a shell, count by hand and say it is an estimate.
7. Stop when the user says so, or when no more words can go without touching kept information: say so and propose to stop.

Nothing enters the report before the user has agreed on the subject.

A source can be any text, including a conversation exported from another chat: it is a source like the others.
