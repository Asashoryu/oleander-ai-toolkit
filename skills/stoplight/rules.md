# stoplight: data and writing rules

A directed graph of claims and reasonings. Both are typed by how far the source supports them.

## Types, for claims and for reasonings

| Type | Colour | Meaning |
|---|---|---|
| **F** fact | green | The source says it entirely: a summary of what the text states. |
| **I** interpretation | yellow | It comes partly from the source: the text gives a basis, not the whole. |
| **S** supposition | red, dashed for a reasoning | The source lacks it: a reinterpretation by the user or the AI. |

A claim and the reasoning that leads to it can have different types. A fact stays a fact while it has its citation.

## Data

```json
{"claims": [
   {"id": "F1", "type": "F", "text": "One sentence", "atoms": ["atom-id"]},
   {"id": "I1", "type": "I", "text": "One sentence", "basis": "Source sentence and place", "by": "ai"},
   {"id": "S1", "type": "S", "text": "One sentence", "basis": "none", "by": "user"}],
 "reasonings": [
   {"id": "R1", "type": "F", "from": ["F1"], "to": "F2", "text": "How the source links them", "cite": "Source, page"},
   {"id": "R2", "type": "I", "from": ["F2"], "to": "I1", "text": "How the premise leads to it", "basis": "Source sentence and place", "by": "ai"}]}
```

- `atoms`: required on an F claim: the ids of the `compress` atoms it holds. `build` writes its `cite` from their places.
- `cite`: required on an F reasoning: the exact place where the source states the link.
- `basis`: required on an I claim or reasoning (the sentence that partly supports it). On an S, write `none` or the weak hint.
- `by`: `ai` or `user`, required on every I and S, claim or reasoning.

## Rules

- Ids are numbered once for the whole report: F1…, I1…, S1…, R1….
- A reasoning joins one or more premises to a claim. A claim may have none. A completion may be a new claim with its reasonings or a reasoning alone between two existing claims.
- An F claim is made of atoms from the `compress` report and says no more than they do. Never invent a source or a quote.
- An idea the user voices is not a claim until the user makes it theirs.
- If the source contradicts itself, one node holds both versions with both places.
- A cause the source states and that is not an event (a stated reason) becomes an F claim.
- New claim that contradicts an existing one: stop, show both, ask how to resolve.
