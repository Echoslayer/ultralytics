"""Compare hand-written arg tables and links in docs against their code owners. Prints observations only."""

import re
import sys
from pathlib import Path

import yaml

root = Path(sys.argv[1])
from ultralytics.cfg import DEFAULT_CFG_DICT

mac = root / "docs/macros"
sets = dict(re.findall(r"\{%-?\s*set\s+(\w+)\s*=\s*(.+?)\s*-?%\}", "\n".join(p.read_text() for p in mac.glob("*.md"))))

print("== default.yaml keys never mentioned in docs/macros or usage/cfg.md")
corpus = "\n".join(p.read_text() for p in mac.glob("*.md")) + (root / "docs/en/usage/cfg.md").read_text()
print([k for k in DEFAULT_CFG_DICT if not re.search(rf"`{k}`|\b{k}\b", corpus)])

print("\n== macro table rows: documented default vs default.yaml")
rowre = re.compile(r"^\|\s*`(\w+)`\s*\|\s*`?([\w\[\]., ]+?)`?\s*\|\s*(.+?)\s*\|", re.M)
for p in sorted(mac.glob("*.md")):
    for line in p.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not cells[0].startswith("`"):
            continue
        k = cells[0].strip("`")
        if k not in DEFAULT_CFG_DICT:
            print(f"  {p.name}: `{k}` not in default.yaml")
            continue
        for c in cells[1:3]:
            if "{{" in c:
                break
        else:
            d = cells[2].strip("`") if cells[1].strip("`").lower() in {"int", "float", "bool", "str", "tuple", "list", "dict", "str | int", "int | tuple", "int | list", "bool | int"} or "|" in cells[1] else cells[1].strip("`")
            live = DEFAULT_CFG_DICT[k]
            if str(live).lower() != d.strip("'\"").lower():
                print(f"  {p.name}: {k} doc={d!r} yaml={live!r}")

print("\n== tracker YAML vs track.md")
tm = (root / "docs/en/modes/track.md").read_text()
for y in sorted((root / "ultralytics/cfg/trackers").glob("*.yaml")):
    cfg = yaml.safe_load(y.read_text())
    print(y.name, "keys missing from track.md:", [k for k in cfg if f"`{k}`" not in tm and k not in tm])

print("\n== SolutionConfig vs docs/macros/solutions-args.md")
from dataclasses import fields

from ultralytics.solutions.config import SolutionConfig

doc = (mac / "solutions-args.md").read_text() if (mac / "solutions-args.md").exists() else ""
live = {f.name: f.default for f in fields(SolutionConfig)}
for line in doc.splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) >= 3 and cells[0].startswith("`"):
        k = cells[0].strip("`")
        print(f"  {k}: doc={cells[2]!r} live={live.get(k, '<<absent>>')!r}")
print("  undocumented:", [k for k in live if f"`{k}`" not in doc])

print("\n== broken relative links / anchors in docs/en")
slug = lambda s: re.sub(r"[\s]+", "-", re.sub(r"[^\w\s-]", "", s.lower().replace("`", "")).strip())
heads = {}
for p in (root / "docs/en").rglob("*.md"):
    t = re.sub(r"^```.*?^```", "", p.read_text(encoding="utf-8"), flags=re.S | re.M)
    ids = {slug(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", m)) for m in re.findall(r"^#{1,6}\s+(.+?)\s*$", t, re.M)}
    ids |= set(re.findall(r"(?:id|name)=[\"']([^\"']+)", t)) | set(re.findall(r"\{#([\w-]+)\}", t))
    heads[p.resolve()] = ids
bad = []
for p in heads:
    if "reference" in p.parts or "compare" in p.parts:
        continue
    t = re.sub(r"^[ \t]*```.*?^[ \t]*```", "", p.read_text(encoding="utf-8"), flags=re.S | re.M)
    for m in re.finditer(r"\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)", t):
        u = m.group(1)
        if u.startswith(("http", "mailto", "<", "{")):
            continue
        path, _, frag = u.partition("#")
        tgt = (p.parent / path).resolve() if path else p
        if path and not path.endswith(".md"):
            continue
        rel = p.relative_to((root / "docs/en").resolve())
        if tgt not in heads:
            if "compare" not in str(tgt):
                bad.append(f"{rel}: missing file {u}")
        elif frag and "reference" not in tgt.parts and frag not in heads[tgt]:
            bad.append(f"{rel}: missing anchor {u}")
print(*sorted(bad), sep="\n")
print(len(bad))
