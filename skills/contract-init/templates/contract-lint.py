#!/usr/bin/env python3
"""Check that contracts and tickets follow the contract-flow template.

Usage: python3 -I contract-lint.py <workspace> <tests folder> [--root DIR] [--types a,b]

Checks only the rigid parts (header, sections, names, verification rows, tickets).
Exit code 0 when everything conforms, 1 otherwise. Standard library only.
"""
import argparse
import re
import sys
from pathlib import Path

TYPES = {"unit", "interface", "integration", "end-to-end", "script", "ai-check"}
SECTIONS = ["Purpose", "View", "Clauses", "Verification", "Notes"]
NAME = re.compile(r"^[a-z0-9]+(_[a-z0-9]+){0,2}$")


def front_matter(text):
    """Return (dict, body). Handles `key: value`, inline lists and `- item` lists."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, text
    data, key = {}, None
    for line in m.group(1).splitlines():
        line = re.sub(r"\s+#.*$", "", line).rstrip()
        if not line.strip():
            continue
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key:
            data.setdefault(key, []).append(item.group(1).strip())
            continue
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                data[key] = [v.strip() for v in val[1:-1].split(",") if v.strip()]
            elif val:
                data[key] = val
            else:
                data[key] = []
    return data, m.group(2)


def sections(body):
    """Return the list of (title, content) for top-level `## ` headings, ignoring code blocks."""
    out, cur, in_code = [], None, False
    for line in body.splitlines():
        if line.startswith("```") or line.startswith("~~~"):
            in_code = not in_code
        if not in_code and line.startswith("## "):
            cur = [line[3:].strip(), []]
            out.append(cur)
        elif cur is not None:
            cur[1].append(line)
    return [(t, "\n".join(c)) for t, c in out]


def table_rows(content):
    rows = []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", line):
            rows.append([c.strip().strip("`") for c in line.strip("|").split("|")])
    return rows[1:] if rows else []  # drop header


def lint_contract(path, cid, root, tests, types, errors):
    def err(msg):
        errors.append(f"{cid}: {msg}")

    fm, body = front_matter(path.read_text(encoding="utf-8"))
    if fm is None:
        return err("no front matter")
    name = fm.get("name", "")
    if not isinstance(name, str) or not name or len(name.split()) > 3:
        err("`name` is missing or longer than 3 words")
    if "realizes" not in fm:
        err("`realizes` is missing (use `[]` on the root only)")
    elif not fm["realizes"] and "/" in cid:
        err("`realizes` is empty on a contract that is not the root")
    enforces = fm.get("enforces") or []
    if not enforces:
        err("`enforces` is empty")
    for p in enforces:
        if not (root / p).exists():
            err(f"enforced path does not exist: {p}")

    secs = sections(body)
    titles = [t for t, _ in secs]
    required = SECTIONS[:4]
    present = [t for t in titles if t in SECTIONS]
    expected = required + (["Notes"] if "Notes" in titles else [])
    if present != expected or any(t not in titles for t in required):
        return err(f"sections must be {', '.join(SECTIONS[:4])} (then optional Notes) in this order; found: {', '.join(titles) or 'none'}")
    content = dict(secs)

    view = content["View"]
    if not ("```" in view or re.search(r"^\s*\|\s*[-:]+", view, re.M)):
        err("View has no diagram, table or tree")

    clauses = []
    for row in table_rows(content["Clauses"]):
        n = row[0]
        if not NAME.match(n):
            err(f"clause name `{n}` must be 1-3 words of a-z, 0-9, joined by `_`")
        if n in clauses:
            err(f"duplicate clause name `{n}`")
        clauses.append(n)
    if not clauses:
        err("Clauses has no rows")

    seen = {}
    for row in table_rows(content["Verification"]):
        if len(row) < 4:
            err("Verification rows need Name, Type, Proves, File")
            continue
        n, typ, _, file = row[:4]
        seen[n] = seen.get(n, 0) + 1
        if n not in clauses:
            err(f"verification row for unknown clause `{n}`")
        if typ not in types:
            err(f"`{n}`: type `{typ}` is not in {sorted(types)}")
        if not (tests / file).exists():
            err(f"`{n}`: verification file missing: {file}")
    for n in clauses:
        if seen.get(n, 0) != 1:
            err(f"clause `{n}` needs exactly one verification row (found {seen.get(n, 0)})")


def lint_tickets(folder, errors):
    names = set()
    for f in sorted(folder.glob("*.md")):
        stem = f.stem
        m = re.match(r"^T-(.+)$", stem)
        if not m or not NAME.match(m.group(1)):
            errors.append(f"ticket {f.name}: must be T-<1-3 words of a-z, 0-9 joined by _>")
            continue
        if stem in names:
            errors.append(f"ticket {stem}: duplicate")
        names.add(stem)
        fm, _ = front_matter(f.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"ticket {stem}: no front matter")
            continue
        if fm.get("id") != stem:
            errors.append(f"ticket {stem}: `id` differs from file name")
        for k in ("status", "direction", "contract", "clause"):
            if not fm.get(k):
                errors.append(f"ticket {stem}: `{k}` missing")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("tests")
    ap.add_argument("--root", default=".")
    ap.add_argument("--types", default="")
    a = ap.parse_args()
    ws, tests, root = Path(a.workspace), Path(a.tests), Path(a.root)
    types = TYPES | {t for t in a.types.split(",") if t}
    errors = []
    base = ws / "contracts"
    files = sorted(base.rglob("*.md"))
    for f in files:
        cid = f.relative_to(base).with_suffix("").as_posix()
        lint_contract(f, cid, root, tests, types, errors)
    if (ws / "tickets").is_dir():
        lint_tickets(ws / "tickets", errors)
    for e in errors:
        print("FAIL", e)
    print(f"{len(files)} contracts checked, {len(errors)} problems")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
