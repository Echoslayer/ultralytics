"""Fetch public PR metadata with gh, or recompute the saved cohort without network access."""

import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "docs" / "assets"
START, END = "2026-07-01T00:00:00Z", "2026-10-01T00:00:00Z"
SNAPSHOT = DATA / "pr-cohort-2026-q3.json"


def api(endpoint):
    return json.loads(subprocess.check_output(["gh", "api", endpoint], encoding="utf-8"))


def elapsed(start, end):
    return (
        datetime.fromisoformat(end.replace("Z", "+00:00")) - datetime.fromisoformat(start.replace("Z", "+00:00"))
    ).total_seconds() / 3600


def group(row):
    if row["user_type"] == "Bot" or row["author"] == "UltralyticsAssistant":
        return "AUTOMATION"
    if row["author"] == "ghost":
        return "UNKNOWN_DELETED"
    return row["author_association"]


def summarize(rows):
    merged = [r for r in rows if r["merged_at"]]
    authors = defaultdict(list)
    for row in rows:
        authors[row["author"]].append(row)
    return {
        "prs": len(rows),
        "authors": len(authors),
        "merged": len(merged),
        "closed_unmerged": sum(r["state"] == "closed" and not r["merged_at"] for r in rows),
        "open": sum(r["state"] == "open" for r in rows),
        "merged_pct": round(100 * len(merged) / len(rows), 2),
        "merged_14d": sum(elapsed(r["created_at"], r["merged_at"]) <= 336 for r in merged),
        "median_merged_hours": round(median(elapsed(r["created_at"], r["merged_at"]) for r in merged), 2)
        if merged
        else None,
        "equal_author_merged_pct": round(
            100 * sum(sum(bool(r["merged_at"]) for r in rs) / len(rs) for rs in authors.values()) / len(authors), 2
        ),
        "top_authors": Counter(r["author"] for r in rows).most_common(5),
    }


if "--fetch" in sys.argv:
    started = datetime.now(timezone.utc).isoformat()
    rows, page = [], 1
    while True:
        endpoint = f"repos/ultralytics/ultralytics/pulls?state=all&sort=created&direction=desc&per_page=100&page={page}"
        batch = api(endpoint)
        print(f"page {page}: {len(batch)} PRs, oldest {batch[-1]['created_at'] if batch else 'none'}", flush=True)
        for pr in batch:
            if START <= pr["created_at"] < END:
                rows.append(
                    {
                        **{
                            k: pr[k]
                            for k in (
                                "number",
                                "title",
                                "html_url",
                                "state",
                                "created_at",
                                "updated_at",
                                "closed_at",
                                "merged_at",
                                "author_association",
                                "draft",
                            )
                        },
                        "author": pr["user"]["login"],
                        "user_type": pr["user"]["type"],
                        "labels": [label["name"] for label in pr["labels"]],
                        "base": pr["base"]["ref"],
                    }
                )
        if not batch or batch[-1]["created_at"] < START:
            break
        page += 1
    snapshot = {
        "repository": "ultralytics/ultralytics",
        "start_inclusive": START,
        "end_exclusive": END,
        "fetch_started_at": started,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "pages_fetched": page,
        "last_endpoint": endpoint,
        "last_page_oldest": batch[-1]["created_at"] if batch else None,
        "rows": sorted(rows, key=lambda r: r["number"]),
    }
    SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
rows = snapshot["rows"]
history_path = DATA / "author-history-before-2026-q3.json"
if "--history" in sys.argv:
    authors = sorted(
        {r["author"] for r in rows if group(r) in {"CONTRIBUTOR", "NONE", "FIRST_TIMER", "FIRST_TIME_CONTRIBUTOR"}}
    )
    histories = {}
    for offset in range(0, len(authors), 10):
        batch = authors[offset : offset + 10]
        fields = []
        for i, author in enumerate(batch):
            for kind, qualifier in (("prior", "created:<2026-07-01"), ("merged", "is:merged merged:<2026-07-01")):
                search = f"repo:ultralytics/ultralytics is:pr author:{author} {qualifier}"
                fields.append(f"{kind}{i}: search(type: ISSUE, query: {json.dumps(search)}, first: 1) {{ issueCount }}")
        request = ROOT / "history-query.json"
        request.write_text(json.dumps({"query": "query { " + " ".join(fields) + " }"}), encoding="utf-8")
        response = json.loads(
            subprocess.check_output(["gh", "api", "graphql", "--input", str(request)], encoding="utf-8")
        )
        assert "errors" not in response, response.get("errors")
        request.unlink()
        for i, author in enumerate(batch):
            histories[author] = {
                "prior_prs": response["data"][f"prior{i}"]["issueCount"],
                "prior_merged": response["data"][f"merged{i}"]["issueCount"],
            }
        print(f"history: {min(offset + 10, len(authors))}/{len(authors)} authors", flush=True)
    history_path.write_text(
        json.dumps(
            {"cutoff_exclusive": START, "fetched_at": datetime.now(timezone.utc).isoformat(), "authors": histories},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
assert rows and len({r["number"] for r in rows}) == len(rows)
assert all(START <= r["created_at"] < END for r in rows)
assert all(elapsed(r["created_at"], snapshot["fetch_started_at"]) >= 336 for r in rows)
assert all(not r["merged_at"] or r["state"] == "closed" and elapsed(r["created_at"], r["merged_at"]) >= 0 for r in rows)
groups = defaultdict(list)
months = defaultdict(list)
for row in rows:
    groups[group(row)].append(row)
    months[row["created_at"][:7] + ":" + group(row)].append(row)
result = {
    "all": summarize(rows),
    "groups": {g: summarize(rs) for g, rs in sorted(groups.items())},
    "monthly_groups": {g: summarize(rs) for g, rs in sorted(months.items())},
}
if history_path.exists():
    histories = json.loads(history_path.read_text(encoding="utf-8"))["authors"]
    expected = {
        r["author"] for r in rows if group(r) in {"CONTRIBUTOR", "NONE", "FIRST_TIMER", "FIRST_TIME_CONTRIBUTOR"}
    }
    assert set(histories) == expected
    assert all(0 <= h["prior_merged"] <= h["prior_prs"] for h in histories.values())
    baseline, first_prs = defaultdict(list), {}
    for row in rows:
        if row["author"] not in histories:
            continue
        h = histories[row["author"]]
        category = "PRIOR_MERGED" if h["prior_merged"] else "PRIOR_PR_NO_MERGE" if h["prior_prs"] else "NEW_IN_QUARTER"
        baseline[category].append(row)
        key = (category, row["author"])
        if key not in first_prs or row["created_at"] < first_prs[key]["created_at"]:
            first_prs[key] = row
    result["baseline_external"] = {g: summarize(rs) for g, rs in sorted(baseline.items())}
    result["first_pr_per_external_author"] = {
        g: summarize([r for (category, _), r in first_prs.items() if category == g]) for g in sorted(baseline)
    }
assert sum(g["prs"] for g in result["groups"].values()) == len(rows)
assert all(g["prs"] == g["merged"] + g["closed_unmerged"] + g["open"] for g in result["groups"].values())
(DATA / "pr-summary-2026-q3.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in result.items() if k != "monthly_groups"}, ensure_ascii=False, indent=2))
