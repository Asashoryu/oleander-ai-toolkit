#!/usr/bin/env python3
"""compress-tools: deterministic checks and HTML build for the learning skills.

  compress-tools.py words <file>        print the word count of a file
  compress-tools.py check <report.json> validate a compress report, print source words, atom words and ratio
  compress-tools.py build <report.json> validate a summarize or stoplight report against the compress
                                        report it comes from, write <report>.html next to it

Two kinds of report:
  compress   (no `visualization`)  data.atoms: the compressed information, with noise, lost and outside
  derived    (`visualization` is the name of a skill folder next to compress/: summarize, stoplight)
             `from` names the compress report; the skill's renderer.js draws the page
"""
import json, re, sys, html
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../compress/tools
SKILLS = HERE.parent.parent                     # folder that holds the skills


def count(text):
    return len(re.findall(r"\S+", text))


def need(rep, keys, errs, where=""):
    errs.extend(f"{where}missing key: {k}" for k in keys if k not in rep)
    return not errs


def validate_compress(rep):
    errs = []
    if not need(rep, ["title", "date", "goal", "mode", "sources", "outside", "noise", "lost", "data"], errs):
        return errs
    if rep["mode"] not in ("lossless", "lossy"):
        errs.append("mode must be lossless or lossy")
    if rep["mode"] == "lossless" and rep["lost"]:
        errs.append("lossless report with a non-empty `lost`")
    if not rep["sources"]:
        errs.append("no source")
    for s in rep["sources"]:
        if not s.get("name"):
            errs.append("a source has no name")
        if not isinstance(s.get("primary"), bool):
            errs.append(f"source '{s.get('name')}': `primary` must be true or false")
    for n in rep["noise"]:
        if not n.get("text") or not n.get("reason"):
            errs.append("a noise entry needs text and reason")
    atoms = rep["data"].get("atoms")
    if not isinstance(atoms, list) or not atoms:
        errs.append("data.atoms must be a non-empty list")
        return errs
    seen = set()
    for a in atoms:
        i = a.get("id")
        if not i:
            errs.append("an atom has no id")
        elif i in seen:
            errs.append(f"duplicate atom id {i}")
        seen.add(i)
        if not a.get("text"):
            errs.append(f"{i}: empty text")
        if not a.get("place"):
            errs.append(f"{i}: an atom needs the place in the source")
    return errs


def source_words(path, s):
    """Words of the part compressed: the declared `words`, else the whole text file."""
    if s.get("words"):
        return s["words"]
    p = Path(s["path"]) if s.get("path") else None
    if p and not p.is_absolute():
        p = path.parent / p
    if p and p.exists():
        if p.suffix.lower() == ".pdf":
            raise ValueError(f"source '{s['name']}' is a PDF: extract the text and declare `words` for the part compressed")
        try:
            return count(p.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            pass
    raise ValueError(f"cannot count the words of source '{s['name']}': give a text `path` or `words`")


def stats_of(path, rep):
    src = sum(source_words(path, s) for s in rep["sources"])
    atoms = sum(count(a["text"]) for a in rep["data"]["atoms"])
    return {"source_words": src, "atom_words": atoms, "ratio": round(src / atoms, 2) if atoms else 0}


def load_base(path, rep):
    base_path = (path.parent / rep["from"]).resolve()
    if not base_path.exists():
        return None, [f"`from` not found: {rep['from']}"]
    base = json.loads(base_path.read_text(encoding="utf-8"))
    errs = validate_compress(base)
    return (base, base_path), [f"the compress report is invalid: {e}" for e in errs]


def validate_derived(rep, base):
    errs, notes = [], []
    atoms = {a["id"]: a for a in base["data"]["atoms"]}
    used = set()

    def use(ids, who):
        for i in ids:
            if i not in atoms:
                errs.append(f"{who}: unknown atom {i}")
            used.add(i)

    if rep["visualization"] == "summarize":
        def walk(sec):
            if not sec.get("title"):
                errs.append("a section has no title")
            for p in sec.get("paragraphs", []):
                if not p.get("atoms"):
                    errs.append(f"paragraph without atoms in '{sec.get('title')}'")
                use(p.get("atoms", []), f"'{sec.get('title')}'")
            for s in sec.get("sections", []):
                walk(s)
        for sec in rep["data"].get("sections", []):
            walk(sec)
        missing = [i for i in atoms if i not in used]
        if missing:
            errs.append("atoms not told in the summary: " + ", ".join(missing))

    elif rep["visualization"] == "stoplight":
        d = rep["data"]
        ids = {}

        def typed(x, what):
            t = x.get("type")
            if t not in ("F", "I", "S"):
                errs.append(f"{x['id']}: {what} needs a type F, I or S")
            elif t == "F" and what == "reasoning" and not x.get("cite"):
                errs.append(f"{x['id']}: an F reasoning needs a cite")
            elif t in ("I", "S"):
                if x.get("by") not in ("ai", "user"):
                    errs.append(f"{x['id']}: an {t} {what} needs by: ai or user")
                if "basis" not in x:
                    errs.append(f"{x['id']}: an {t} {what} needs a basis (or 'none')")
                elif t == "I" and x["basis"] in ("", "none"):
                    errs.append(f"{x['id']}: an I {what} needs a real basis")

        for c in d.get("claims", []):
            if c["id"] in ids:
                errs.append(f"duplicate id {c['id']}")
            ids[c["id"]] = c
            if c.get("type") not in ("F", "I", "S") or not c["id"].startswith(str(c.get("type"))):
                errs.append(f"{c['id']}: id and type disagree")
            typed(c, "claim")
            if c.get("type") == "F":
                if not c.get("atoms"):
                    errs.append(f"{c['id']}: an F claim needs `atoms`")
                else:
                    use(c["atoms"], c["id"])
                    c["cite"] = "; ".join(atoms[i]["place"] for i in c["atoms"] if i in atoms)
        for r in d.get("reasonings", []):
            typed(r, "reasoning")
            for ref in r["from"] + [r["to"]]:
                if ref not in ids:
                    errs.append(f"{r['id']}: unknown claim {ref}")
        missing = [i for i in atoms if i not in used]
        if missing:
            notes.append("atoms in no F claim: " + ", ".join(missing))
    return errs, notes


def check(path):
    rep = json.loads(Path(path).read_text(encoding="utf-8"))
    errs = validate_compress(rep)
    if not errs:
        try:
            st = stats_of(Path(path), rep)
        except ValueError as e:
            errs.append(str(e))
    if errs:
        print("INVALID")
        for e in errs:
            print(" -", e)
        return 1
    print(f"atoms {len(rep['data']['atoms'])}, noise {len(rep['noise'])}, lost {len(rep['lost'])}, outside {len(rep['outside'])}")
    print(f"source words {st['source_words']}, atom words {st['atom_words']}, ratio {st['ratio']:.2f}")
    return 0


def build(path):
    path = Path(path)
    rep = json.loads(path.read_text(encoding="utf-8"))
    errs = [f"missing key: {k}" for k in ("title", "date", "goal", "from", "visualization", "data") if k not in rep]
    if not errs:
        viz_dir = SKILLS / str(rep["visualization"])
        if not (viz_dir / "renderer.js").exists():
            errs.append(f"unknown visualization: {rep['visualization']}")
    notes = []
    if not errs:
        loaded, errs = load_base(path, rep)
    if not errs:
        base, base_path = loaded
        try:
            st = stats_of(base_path, base)
        except ValueError as e:
            errs.append(str(e))
    if not errs:
        errs, notes = validate_derived(rep, base)
    if errs:
        print("INVALID")
        for e in errs:
            print(" -", e)
        return 1
    # the page shows what the compress report says about the source
    rep["sources"] = base["sources"]
    rep["atoms"] = {a["id"]: a for a in base["data"]["atoms"]}
    rep["noise"], rep["lost"], rep["outside"] = base["noise"], base["lost"], base["outside"]
    rep["mode"], rep["stats"] = base["mode"], st
    css = (HERE / "page.css").read_text(encoding="utf-8")
    if (viz_dir / "style.css").exists():
        css += (viz_dir / "style.css").read_text(encoding="utf-8")
    renderer = (viz_dir / "renderer.js").read_text(encoding="utf-8")
    page = (HERE / "page.js").read_text(encoding="utf-8")
    data = json.dumps(rep, ensure_ascii=False).replace("</", "<\\/")
    out = path.with_suffix(".html")
    out.write_text(
        f"<!doctype html><html lang=it><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
        f"<title>{html.escape(rep['title'])}</title><style>{css}</style></head>"
        f"<body><div id=app></div><script id=report type=application/json>{data}</script>"
        f"<script>{renderer}</script><script>{page}</script></body></html>",
        encoding="utf-8",
    )
    print(f"written {out}")
    print(f"source words {st['source_words']}, atom words {st['atom_words']}, ratio {st['ratio']:.2f}")
    for n in notes:
        print("note:", n)
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "words":
        print(count(Path(sys.argv[2]).read_text(encoding="utf-8")))
    elif len(sys.argv) == 3 and sys.argv[1] == "check":
        sys.exit(check(sys.argv[2]))
    elif len(sys.argv) == 3 and sys.argv[1] == "build":
        sys.exit(build(sys.argv[2]))
    else:
        print(__doc__)
        sys.exit(2)
