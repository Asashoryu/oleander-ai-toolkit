---
name: summarize
description: Tell the atoms of a compress report as one narration, grouped by section, with the place of each atom as a numbered reference, rendered as an encyclopedia-style HTML page. Every atom must be told, none is added. Use after compress, to read a compressed source as a text instead of a list of atoms.
---

# Summarize

`compress` keeps the information of a source as atoms, each with its place. You put the atoms together as a narration that a person can read in order. You tell all of them and add nothing: no interpretation, no outside knowledge. For interpretations and gaps use `stoplight`.

Reply in the user's language. JSON keys stay in English.

## Rules

- Every atom of the compress report is told in at least one paragraph. `build` fails if one is missing.
- A paragraph lists the `atoms` it tells. Its text may join, order and connect them, but says nothing the atoms do not say.
- Sections follow the structure of the source, nested up to three levels.
- The user decides the structure. Propose the outline (section titles and which atoms go where) in one table, wait for the answer, then write.
- Before overwriting an existing summary, say so and ask.

## The input

A compress report (`<source-name>_compresso.json`). Without one, run `compress` first. Read its `goal`: the narration serves it, and the order of the sections follows it.

## A session

1. Read the report. List the atoms by place.
2. Propose the outline: sections, and the atoms of each.
3. The user confirms or corrects.
4. Write `<source-name>_compresso_summarize.json` next to the compress report, leaving that report untouched:

```json
{"title": "", "date": "YYYY-MM-DD", "goal": "",
 "from": "<source-name>_compresso.json",
 "visualization": "summarize",
 "data": {"sections": [{
   "title": "Chapter or topic",
   "paragraphs": [{"text": "A few sentences that tell the atoms", "atoms": ["id", "id"]}],
   "sections": []}]}}
```

5. Run `python3 ../compress/tools/compress-tools.py build "<report>.json"` (path relative to this skill). Fix every error it prints: an unknown atom, an atom not told. Tell the user the path of the `.html` file.

The page shows an index, the narration with the places as numbered references, and the cards of the compress report (ratio, what lies outside, discards).
