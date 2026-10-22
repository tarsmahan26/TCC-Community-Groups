#!/usr/bin/env python3
"""Rebuild index.html from data/catalog.json, data/books.json and src/template.html.

Usage:  python3 build.py

Checks every entry first (reference exists, topics and kind are known) and stops with a list of
problems instead of writing a broken page. Needs only the Python 3 standard library.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS = json.load(open(os.path.join(HERE, "data", "books.json"), encoding="utf-8"))
CATALOG = json.load(open(os.path.join(HERE, "data", "catalog.json"), encoding="utf-8"))
TEMPLATE = open(os.path.join(HERE, "src", "template.html"), encoding="utf-8").read()

ORDER = [b["abbr"] for b in BOOKS["books"]]
NAME = {b["abbr"]: b["name"] for b in BOOKS["books"]}
CHAPTERS = {b["abbr"]: b["chapters"] for b in BOOKS["books"]}
SINGLE = {abbr for abbr, chs in CHAPTERS.items() if len(chs) == 1}
PROV = "Prov"

THEMES = {
    "oa.love", "oa.friendship", "oa.humility", "oa.serve", "oa.encourage", "oa.generosity", "oa.unity",
    "oa.patience", "oa.speech", "oa.accountability", "oa.prayer", "oa.impartiality", "oa.leaders", "oa.household",
    "cf.forgiveness", "cf.confront", "cf.restore", "cf.anger", "cf.quarrels", "cf.judging", "cf.division",
    "cf.revenge", "cf.peacemaking", "cf.disputes", "cf.divisive",
    "un.witness", "un.conduct", "un.answer", "un.enemies", "un.persecution", "un.authorities", "un.good",
    "un.engaging", "un.family", "un.rejection", "un.boundaries",
}
TYPE_CODE = {"teaching": "t", "example": "e", "parable": "p", "proverb": "v"}
XREL = {"Quoted in", "Echoed in", "Compare", "Quotes", "Echoes"}
FIELDS = {"ref", "context", "title", "summary", "themes", "type", "jesus", "key", "cautionary", "parallels", "note", "xref"}
REF_RE = re.compile(r"^(\w+) (\d+):(\d+)(?:-(?:(\d+):)?(\d+))?$")

# Every verse gets a running number so the page can count distinct verses quickly.
GIDX, total = {}, 0
for abbr in ORDER:
    for ch, count in enumerate(CHAPTERS[abbr], 1):
        for v in range(1, count + 1):
            GIDX[(abbr, ch, v)] = total
            total += 1
OMITTED = set()
for ref in BOOKS["omitted"]:
    book, cv = ref.split()
    ch, v = cv.split(":")
    OMITTED.add(GIDX[(book, int(ch), int(v))])


def parse_ref(ref):
    """'Matt 18:15-17' -> ('Matt', [(18, 15), (18, 16), (18, 17)]). Raises ValueError if invalid."""
    m = REF_RE.match(ref.strip())
    if not m:
        raise ValueError(f"bad reference format '{ref}' (use e.g. 'Rom 12:9-13' or '2Cor 6:14-7:1')")
    book, c1, v1, c2, v2 = m.groups()
    if book not in CHAPTERS:
        raise ValueError(f"unknown book '{book}' in '{ref}' (use one of: {', '.join(ORDER)})")
    c1, v1 = int(c1), int(v1)
    c2, v2 = (c1, v1) if v2 is None else (int(c2) if c2 else c1, int(v2))
    chs = CHAPTERS[book]
    for c, v in ((c1, v1), (c2, v2)):
        if c < 1 or c > len(chs) or v < 1 or v > chs[c - 1]:
            raise ValueError(f"'{ref}': {book} {c}:{v} does not exist")
    if (c2, v2) < (c1, v1):
        raise ValueError(f"'{ref}': range runs backwards")
    verses, c, v = [], c1, v1
    while (c, v) <= (c2, v2):
        verses.append((c, v))
        v += 1
        if v > chs[c - 1]:
            c, v = c + 1, 1
    return book, verses


def labels(ref):
    """Return (what readers see, what ESV.org is asked for), e.g. ('Philemon 15–17', 'Philemon 1:15-17')."""
    book, vs = parse_ref(ref)
    (c1, v1), (c2, v2) = vs[0], vs[-1]
    name = NAME[book]
    if book == "3John" and (c1, v1) <= (1, 14) <= (c2, v2):  # some Bibles split 3 John 14 into 14-15
        v2 = 15
    if book in SINGLE:
        return name + f" {v1}" + (f"–{v2}" if v2 != v1 else ""), name + f" 1:{v1}" + (f"-{v2}" if v2 != v1 else "")
    if (c1, v1) == (c2, v2):
        return f"{name} {c1}:{v1}", f"{name} {c1}:{v1}"
    if c1 == c2:
        return f"{name} {c1}:{v1}–{v2}", f"{name} {c1}:{v1}-{v2}"
    return f"{name} {c1}:{v1}–{c2}:{v2}", f"{name} {c1}:{v1}-{c2}:{v2}"


def check(e, i):
    tag = f"entry {i + 1} ({e.get('ref', '?')})"
    problems = []
    for f in sorted(set(e) - FIELDS):
        problems.append(f"{tag}: unknown field '{f}'")
    for f in ("ref", "title", "summary", "themes", "type"):
        if f not in e:
            problems.append(f"{tag}: missing '{f}'")
    for f in ("ref", "context"):
        if f in e:
            try:
                parse_ref(e[f])
            except ValueError as ex:
                problems.append(f"{tag}: {f}: {ex}")
    for p in e.get("parallels", []):
        try:
            parse_ref(p)
        except ValueError as ex:
            problems.append(f"{tag}: parallel: {ex}")
    for x in e.get("xref", []):
        if x.get("rel") not in XREL:
            problems.append(f"{tag}: xref rel must be one of {sorted(XREL)}")
        try:
            parse_ref(x.get("ref", ""))
        except ValueError as ex:
            problems.append(f"{tag}: xref: {ex}")
    themes = e.get("themes", [])
    if not 1 <= len(themes) <= 3:
        problems.append(f"{tag}: give 1 to 3 topics")
    for t in themes:
        if t not in THEMES:
            problems.append(f"{tag}: unknown topic '{t}'")
    if e.get("type") not in TYPE_CODE:
        problems.append(f"{tag}: type must be one of {sorted(TYPE_CODE)}")
    return problems


def main():
    problems = [p for i, e in enumerate(CATALOG) for p in check(e, i)]
    refs = [e.get("ref") for e in CATALOG]
    problems += [f"duplicate entry for {r}" for r in sorted({r for r in refs if refs.count(r) > 1})]
    if problems:
        print("Not built. Fix these in data/catalog.json:")
        print("\n".join("  - " + p for p in problems))
        sys.exit(1)

    def sort_key(e):
        book, vs = parse_ref(e["ref"])
        return ORDER.index(book), vs[0], len(vs)

    rows = []
    for e in sorted(CATALOG, key=sort_key):
        book, vs = parse_ref(e["ref"])
        shown, query = labels(e["ref"])
        row = {"id": e["ref"], "d": shown, "q": query, "t": e["title"], "s": e["summary"], "th": e["themes"],
               "ty": TYPE_CODE[e["type"]], "bk": ORDER.index(book),
               "f": "".join(c for c, k in (("K", "key"), ("J", "jesus"), ("C", "cautionary")) if e.get(k)),
               "a": GIDX[(book, *vs[0])], "b": GIDX[(book, *vs[-1])]}
        if e.get("context"):
            row["cx"] = list(labels(e["context"]))
        if e.get("parallels"):
            row["pl"] = [list(labels(p)) for p in e["parallels"]]
        if e.get("xref"):
            row["x"] = [[x["rel"], *labels(x["ref"])] for x in e["xref"]]
        if e.get("note"):
            row["n"] = e["note"]
        rows.append(row)

    prov = ORDER.index(PROV)
    nt_rows = [r for r in rows if r["bk"] != prov]
    covered = set()
    for r in nt_rows:
        covered.update(range(r["a"], r["b"] + 1))
    covered -= OMITTED
    nt_total = sum(sum(CHAPTERS[a]) for a in ORDER if a != PROV) - len(OMITTED)

    payload = {"entries": rows, "books": [NAME[a] for a in ORDER], "blank": sorted(OMITTED)}
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (TEMPLATE.replace("__DATA__", blob)
            .replace("__NTCOUNT__", str(len(nt_rows)))
            .replace("__PROVCOUNT__", str(len(rows) - len(nt_rows)))
            .replace("__NTVERSES__", f"{len(covered):,}")
            .replace("__NTTOTAL__", f"{nt_total:,}"))
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Built index.html: {len(nt_rows)} New Testament passages ({len(covered):,} of {nt_total:,} verses) "
          f"and {len(rows) - len(nt_rows)} proverbs.")


if __name__ == "__main__":
    main()
