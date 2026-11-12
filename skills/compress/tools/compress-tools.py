#!/usr/bin/env python3
"""compress-tools: deterministic checks and HTML build for a compress report.

  compress-tools.py words <file>     print the word count of a file
  compress-tools.py build <report.json>
        validate the report, write <report>.html next to it, print the
        source words, the report words and the ratio
"""
import json, re, sys, html
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
HEADER_KEYS = ["title", "date", "sources", "not_treated", "noise", "lost", "visualization", "data"]


def count(text):
    return len(re.findall(r"\S+", text))


def strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from strings(v)


def validate(rep, viz_dir):
    errs = [f"missing key: {k}" for k in HEADER_KEYS if k not in rep]
    if errs:
        return errs
    if not (viz_dir / "renderer.js").exists():
        return [f"unknown visualization: {rep['visualization']}"]
    for s in rep["sources"]:
        if not s.get("name"):
            errs.append("a source has no name")
    if rep["visualization"] == "stoplight":
        d = rep["data"]
        ids = {}
        for c in d.get("claims", []):
            if c["id"] in ids:
                errs.append(f"duplicate id {c['id']}")
            ids[c["id"]] = c
            if c["type"] not in "FIS" or not c["id"].startswith(c["type"]):
                errs.append(f"{c['id']}: id and type disagree")
            if c["type"] == "F" and not c.get("cite"):
                errs.append(f"{c['id']}: a fact needs a citation")
        for r in d.get("reasonings", []):
            for ref in r["from"] + [r["to"]]:
                if ref not in ids:
                    errs.append(f"{r['id']}: unknown claim {ref}")
    if rep["visualization"] == "sintesi":
        def walk(sec):
            title = sec.get("title")
            for p in sec.get("points", []) + sec.get("timeline", []):
                if not p.get("source"):
                    errs.append(f"entry without source in '{title}'")
            q = sec.get("quote")
            if q and not q.get("source"):
                errs.append(f"quote without source in '{title}'")
            for s in sec.get("sections", []):
                walk(s)
        for sec in rep["data"].get("sections", []):
            walk(sec)
    return errs


def build(path):
    path = Path(path)
    rep = json.loads(path.read_text(encoding="utf-8"))
    viz_dir = HERE / "visualizations" / str(rep.get("visualization"))
    errs = validate(rep, viz_dir)
    if errs:
        print("INVALID")
        for e in errs:
            print(" -", e)
        return 1
    src_words = 0
    for s in rep["sources"]:
        p = Path(s["path"]) if s.get("path") else None
        if p and not p.is_absolute():
            p = path.parent / p
        w = count(p.read_text(encoding="utf-8")) if p and p.exists() else s.get("words", 0)
        s["words"] = w
        src_words += w
    rep_words = sum(count(t) for t in strings(rep["data"]))
    ratio = src_words / rep_words if rep_words else 0
    rep["stats"] = {"source_words": src_words, "report_words": rep_words, "ratio": round(ratio, 2)}
    renderer = (viz_dir / "renderer.js").read_text(encoding="utf-8")
    base = (HERE / "tools" / "page.js").read_text(encoding="utf-8")
    css = (HERE / "tools" / "page.css").read_text(encoding="utf-8")
    style = viz_dir / "style.css"
    if style.exists():
        css += style.read_text(encoding="utf-8")
    data = json.dumps(rep, ensure_ascii=False).replace("</", "<\\/")
    out = path.with_suffix(".html")
    out.write_text(
        f"<!doctype html><html lang=it><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
        f"<title>{html.escape(rep['title'])}</title><style>{css}</style></head>"
        f"<body><div id=app></div><script id=report type=application/json>{data}</script>"
        f"<script>{renderer}</script><script>{base}</script></body></html>",
        encoding="utf-8",
    )
    print(f"written {out}")
    print(f"source words {src_words}, report words {rep_words}, ratio {ratio:.2f}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "words":
        print(count(Path(sys.argv[2]).read_text(encoding="utf-8")))
    elif len(sys.argv) == 3 and sys.argv[1] == "build":
        sys.exit(build(sys.argv[2]))
    else:
        print(__doc__)
        sys.exit(2)
