---
name: compress
description: Compress a source (book, text, conversation, PDF), or a part of it the user chooses, into atoms of information with the same meaning in fewer words, automatically and completely, and list explicitly what was discarded as noise. The result is a JSON file; lossless by default, lossy on request. It adds no interpretation. The skills summarize and stoplight then read the atoms to tell them or to reason on them. Use to condense a long source, to study a text in depth, or to extract the facts a later reorganisation needs.
---

# Compress

Compression keeps the semantics of a source with less syntax. The result is pure with respect to the source: the same information (lossless) or less (lossy), never more. It adds no interpretation and no outside knowledge. Telling the atoms as a narration is `summarize`; reasoning on them and filling what the source leaves out is `stoplight`.

The work is automatic and complete: every piece of information in the chosen part ends up in the fewest sentences, and every piece of text that carries no information is listed as noise, with the reason.

Reply in the user's language. Frontmatter and JSON keys stay in English.

## Rules

- Never invent a source, a quote or a place. If you cannot verify a place, say so and leave the atom out.
- An atom is one piece of information, in the shortest sentence that keeps its whole meaning, with its place in the source.
- If two sentences of the source say the same, one atom holds both places. If the source contradicts itself, keep both versions with both places in one atom.
- Do not interpret, connect or complete. What the source leaves out is `stoplight`'s work.
- Discuss only to resolve doubt about what is information. The user reviews the result afterwards and corrects it.

## 1. Setup

Ask once, with a recommended answer for each:

| Question | Default |
|---|---|
| Which part of the source to compress? (the whole, or a range: "chapters 2 and 3", "pages 10-25") | The whole |
| Lossless or lossy | Lossless |
| What must the result serve? Goes in `goal` | Understanding the source as a whole |
| Is the source a primary one? An AI answer or a summary is not | Ask |

Lossy needs one more answer: what the user accepts to lose (a criterion, in a sentence). It decides what goes to `lost` instead of staying as an atom.

## 2. Reading

Read the chosen part to the end. A PDF: extract the text first (`pypdf`, `pdftotext`) and tell the user which tool you used; if none is available, ask. For a long source, read by chunks and add the atoms to the report as you go, so nothing depends on memory.

## 3. Sorting

Every piece of the chosen part ends in one of three places:

| Outcome | Meaning |
|---|---|
| **Atom** | Information that stays: it goes into `data.atoms`. |
| **Noise** | Text that carries no information (interface text, links, the author's afternoon wine). Listed with a one-line reason. |
| **Lost** | Information the user accepts to sacrifice. Lossy mode only. |

Whatever lies outside the chosen part goes to `outside`, in a line each.

When in doubt whether a piece is information or noise, it is information.

## 4. The report

One file `<source-name>_compresso.json` next to the source (`<source-name>` is the source's file name without its extension). Before overwriting an existing report, say so and ask. Without file access, print it as a fenced block titled with that path.

```json
{"title": "", "date": "YYYY-MM-DD", "goal": "", "mode": "lossless",
 "sources": [{"name": "", "path": "relative path, optional", "primary": true,
              "scope": "the whole, or the range chosen", "words": 0}],
 "outside": ["parts of the source not compressed"],
 "noise": [{"text": "", "reason": ""}],
 "lost": [{"text": ""}],
 "data": {"atoms": [{"id": "word-made-id", "text": "", "place": "Book, ed., p. 12"}]}}
```

- `words` is the word count of the part compressed. Leave it out when the part is the whole of a text file: `check` counts it. For a range or a PDF, extract that part to a scratch file, run `python3 tools/compress-tools.py words <file>` (path relative to this skill) and write the number.
- Atom ids are unique, in the order of the source.
- In lossless mode `lost` stays empty.

## 5. A run

1. Do the setup, or read the existing report and say what it already covers.
2. Read and sort, as above, over the whole chosen part.
3. Write the report.
4. Run `python3 tools/compress-tools.py check "<report>.json"` (path relative to this skill). It validates the report and prints the source words, the atom words and the ratio. Fix every error it prints.
5. Show the user the result for review: the ratio, the table of noise with reasons, the table of lost (if any), the list of what lies outside. Do not list the atoms unless asked.
6. The user corrects: a noise line that is information becomes an atom, a lost line may too. Apply, run `check` again, show the new ratio.
7. Offer `summarize` to read the atoms as a narration, or `stoplight` to reason on them.

A source can be any text, including a conversation exported from another chat: it is a source like the others. A ratio below 1 means the source is already shorter than its atoms: say so and propose to stop.
