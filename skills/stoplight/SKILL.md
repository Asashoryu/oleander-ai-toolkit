---
name: stoplight
description: Reorganise the atoms of a compress report into a graph of facts, interpretations and suppositions linked by reasonings, find the gaps where the source jumps or is silent, and propose interpretations and suppositions to complete them. Claims and reasonings are both typed F (the source says it entirely), I (partly) or S (it lacks it), and each I or S says whether the user or the AI made it. Use after compress, to see how the pieces of a source fit together and what the source leaves out.
---

# Stoplight

`compress` finds the atoms of information in a source and keeps them faithful. You take those atoms and reorganise them, then go further: you find what the source leaves out and help the user complete it. What you add is never mixed with what the source says: every claim and reasoning carries its type.

Reply in the user's language. JSON keys stay in English. Types, fields and writing rules are in `rules.md` next to this file: read it before writing.

## Rules

- Short answers, one point at a time. No quizzes unless asked.
- Say where the source states something and where you are adding.
- The user decides, line by line. Nothing you propose enters the report before they confirm it.
- An idea the user voices is not a claim until they make it theirs.

## The input

A `compress` report (`<source-name>_compresso.json`): `data.atoms` are the F claims. Without one, run `compress` first. Read the report's `goal`: it says what the graph must answer.

## A session

1. **Reorganise.** Turn the atoms into F claims, ordered as the goal asks. Each F claim names the atoms it holds in `atoms`; `build` fills its `cite` from their places. Link them with **F reasonings** wherever the source states the link, with its place. If the source states a reason that is not an event, add it as an F claim.
2. **Find the gaps.** A gap is an atom with no stated cause, a conclusion without premises, or a jump between two atoms. Show them in one table: where, what is missing.
3. **Propose.** For each gap, one to three completions, of two kinds: a **new claim** with the reasonings that link it, or a **reasoning alone** between two existing claims. Both are typed:
   - **I** if the source gives a partial basis: quote the sentence and place;
   - **S** if the source lacks it entirely, whether from the AI's knowledge or from reasoning: say which (`by: ai`).
   Say in one line what you add. Outside knowledge is always S or I, with its origin, never F.
4. **The user decides** each line: confirm, correct, write their own (`by: user`) or drop. A dropped gap stays a gap and is listed as open.
5. **Write** `<source-name>_compresso_stoplight.json` next to the `compress` report, leaving that report untouched.
6. **Build**: `python3 ../compress/tools/compress-tools.py build "<report>.json"` (path relative to this skill). Fix every error it prints. If it notes atoms that are in no F claim, say so to the user: it is allowed, but they should know. Tell the user the path of the `.html` file and the gaps still open.

The page draws the claims as cards and the reasonings as arrows, in the colour of their type (a supposition dashed). Passing over an arrow or a card shows the reasoning: type, origin and explanation.

## The report

```json
{"title": "", "date": "YYYY-MM-DD", "goal": "",
 "from": "<source-name>_compresso.json",
 "visualization": "stoplight",
 "data": {"claims": [], "reasonings": [], "open": ["gaps still open"]}}
```

`data.open` lists the gaps still open. Before overwriting an existing report, say so and ask.

For typing statements in conversation, with no report, use `stoplight-live`.
