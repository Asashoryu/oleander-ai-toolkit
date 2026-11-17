# compress: test notes

Defects found while testing `compress` with `stoplight`, to fix in the next version. Test 1: `ottavio bianchi - Google Search.pdf` (47 pages, AI chat), era 1, 2026-11-13.

## Status (2026-11-15)

`compress` was redesigned: automatic, atoms only (`data.atoms`), outcomes atom / noise / lost / outside, `check` prints the ratio of the part chosen over the atom words only (closes 3 and 4 below). `sintesi` became the skill `summarize`; `stoplight` reads atoms by id. The ratio shows on the page only above 1, `goal` and primary/secondary are shown. Tested on an invented text in `tmp/prova` (light, dark, narrow, errors); not tested: print, a real long source, a PDF, `setup.ps1`, copy install mode, the graph hover.

## Status (2026-11-14)

Done in the rework: 1, 2 (SKILL.md and `build`), 5, 6, 8 partly, 9, 10, 11, 12, 13. The design change below is applied: `compress` keeps atoms only, `stoplight` is its own skill with F/I/S on claims and reasonings.
Still open: 3 and 4 (ratio counts all report strings, including `cite` and `basis`, and the noise text of the source); 7 (nothing records whether a batch was discussed); the arrows' `cited` flag was replaced by the reasoning type; checking that a source without file access still works.

## Open

| # | Defect | Where | Proposed fix |
|---|---|---|---|
| 1 | `build` crashes with `UnicodeDecodeError` when a source is a PDF. | `tools/compress-tools.py`, `build()`, line `p.read_text(...)` | Extract the text first, or stop with a clear message and ask for an explicit `words`. |
| 2 | The skill does not say how to read a non-text source (PDF). No extractor, and `pypdf`/`pdftotext` were not installed. | `SKILL.md` | Say how to get the text, or add the step. |
| 3 | The ratio compares the whole source with a report that covers one iteration, so it is misleading. | `build()`, `stats` | Count only the treated parts, or show the ratio per iteration. |
| 4 | The word count of the source includes interface text (timestamps, links, "AI can make mistakes"), which the report later calls noise. | `build()` | Count after removing the declared noise, or show both counts. |
| 5 | I and S claims were proposed by the assistant and accepted without the source sentence that holds them, so the assistant's own constructions looked like conclusions found in the source (I1 turned "after" into "from", S1 was a guess). | `SKILL.md` rules, `stoplight/rules.md` | The assistant proposes I and S only with the source sentence that supports them, and says in one line what it adds. Optionally store it in the claim (`basis`, `adds`). |
| 6 | When the source is an AI conversation, every `F` cites "the AI", which is not a verifiable place. The skill says a fact needs a verifiable citation. | `stoplight/rules.md` | Add a rule for sources that are not primary: cite the claim and mark the source as unverified, or use a different type. |
| 7 | The iteration asks for a discussion before the batch, but in a test it was skipped. Nothing marks that the discussion did not happen. | `SKILL.md`, iteration step 3 | Record in the report whether each batch was discussed or accepted directly. |
| 8 | The "lost" outcome was never exercised: material outside the subject stayed in `not_treated` with no way to say "keep for later" versus "discard". | `SKILL.md`, *Sorting* | Decide whether `not_treated` also needs a reason or a priority. |

Found in test 2 (whole document as a chain of events, `Catena.json`, 29 nodes, 9 causal links):

| # | Defect | Where | Proposed fix |
|---|---|---|---|
| 9 | One report per source, overwritten at every iteration, but the vault has no history: a second compression of the same source (a different goal) erases the first. I wrote `Catena.json` next to `Condensato.json` to avoid it. | `SKILL.md`, *The report* | Name the report by goal (`<Source> - <Goal>.json`), or ask before overwriting. |
| 10 | The source contradicts itself (Reja "esonerato" p.28, "dimissioni" p.30). The skill has the contradiction rule only for claims already in the report, not inside the source. | `SKILL.md`, `stoplight/rules.md` | Say how to record two versions in one node, with both citations. |
| 11 | A chain of events is a graph, but `stoplight` reasonings are meant to be the user's. To avoid inventing causes I only linked what the source states, with the page. | `stoplight/rules.md` | Allow a reasoning whose text is the source sentence (a `cited` flag), distinct from a user reasoning. |
| 12 | No inventory step: I built the list of events by hand from my own reading and the user could not check the full list of facts. | `SKILL.md` | See *Design change requested*. |
| 13 | The skill does not say what to do when the source is 47 pages: reading it all costs a lot of context. | `SKILL.md` | Read by chunks and write the inventory to a file as it goes. |

## Design change requested (2026-11-13)

Interpretations and suppositions must not be created from nothing (see #5). The flow becomes:

1. **Inventory**: the skill extracts the list of all informative facts in the source, each with its place. Nothing is interpreted.
2. **Choice**: by an automatic or a conversational step, the user decides which pieces of information to compress.
3. **Compression**: the chosen pieces are condensed by the mode of a supporting skill (`sintesi`, `stoplight`, others). Only the user adds interpretations and suppositions.

Consequences to settle: where the inventory lives (a new `inventory` key in the report, with each fact marked treated or not, replacing the free-text `not_treated`); what the automatic step is; how a mode treats facts that have no interpretation (in `stoplight`, an inventory of green facts with no yellow or red ones is valid).

## To check

- Does the HTML page show the claims, the reasonings and the colours well? (the user has to open `ottavio bianchi - Google Search - Condensato.html`)
- Does the report stay valid when the user changes visualization (`sintesi`)?
- Next iterations (eras 2 to 6): does a claim from a later era that contradicts an earlier one trigger the "stop, show both" rule?
