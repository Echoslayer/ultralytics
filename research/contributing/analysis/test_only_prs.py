"""Q3 2026 PR outcomes split by whether the PR touches tests/ only, tests and code, or no tests."""

import collections
import json
import sys
from pathlib import Path

ASSETS = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "docs" / "assets")
EXTERNAL = {"CONTRIBUTOR", "FIRST_TIME_CONTRIBUTOR", "FIRST_TIMER", "NONE"}

files = json.loads((ASSETS / "pr-files-2026-q3.json").read_text(encoding="utf-8"))["prs"]
rows = {str(r["number"]): r for r in json.loads((ASSETS / "pr-cohort-2026-q3.json").read_text(encoding="utf-8"))["rows"]}

counts = collections.Counter()
external_test_only = []
for number, pr in files.items():
    row, paths = rows.get(number), [f["path"] for f in pr["files"]]
    if not row or not paths:
        continue
    in_tests = [p.startswith("tests/") for p in paths]
    kind = "test-only" if all(in_tests) else "with-tests" if any(in_tests) else "no-tests"
    who = "external" if row["author_association"] in EXTERNAL else "member"
    state = pr["state"].lower()
    counts[who, kind, state] += 1
    if who == "external" and kind == "test-only":
        external_test_only.append((number, state, row["author"], row["title"]))

for key in sorted(counts):
    print(*key, counts[key])
print("external test-only:")
for item in sorted(external_test_only):
    print(" ", *item)
