# stoplight

Claims sorted by how far the source supports them, linked by reasonings: a directed graph with three node types.

## Data

```json
{"claims": [{"id": "F1", "type": "F", "text": "One sentence", "cite": "Edition, page"}],
 "reasonings": [{"id": "R1", "from": ["F1", "F2"], "to": "I1", "text": "How the premises lead to the conclusion"}]}
```

## Claim types

| Type | Colour | Meaning |
|---|---|---|
| **F** fact | green | The source strongly supports it. Carries a `cite` with the exact place. |
| **I** interpretation | yellow | The user's reworking of a fact. |
| **S** supposition | red | Strong for the user, weak in the source. Includes missing links the source does not state. |

The type belongs to the claim: any type can derive from any type. A fact stays a fact while it has its citation. Never invent a source or a quote: what you cannot verify is not a fact.

## Rules

- Ids are numbered once for the whole report: F1, F2…, I1…, S1…, R1….
- A reasoning joins one or more premises to a new claim of any type. A claim may have no premises.
- An objection from the user is not a claim until the user makes it theirs.
- A new claim that contradicts an existing one: stop, show both, ask how to resolve.
