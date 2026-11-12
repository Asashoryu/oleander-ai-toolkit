# sintesi

The default visualization: condensed points grouped by section of the source, in the manner of an encyclopedia page: an index on the left, the text in the middle, a card of key facts on the right.

## Data

```json
{"scheda": [{"label": "Born", "value": "26 December 1194, Jesi"}],
 "sections": [{
   "title": "Chapter or topic",
   "timeline": [{"when": "1208", "text": "One short sentence", "source": "Book, ed., p. 12"}],
   "points": [{"text": "One short sentence", "source": "Book, ed., p. 12"}],
   "quote": {"text": "Words of the source", "by": "Author", "source": "Book, ed., p. 12"},
   "sections": []}]}
```

Every key of a section except `title` is optional. `sections` nests, to three levels.

## Rules

- `scheda` holds the few facts a reader wants at a glance: dates, places, names, numbers. Leave it out when the source has none.
- Sections follow the structure of the source.
- Use `timeline` for dated events in order, `points` for everything else, `quote` only for words worth keeping verbatim.
- A point is one sentence, as short as possible. Its `source` is the exact place that holds it. A source you cannot verify is not written, and the point is not kept.
- Only information the user agreed to keep becomes a point.
