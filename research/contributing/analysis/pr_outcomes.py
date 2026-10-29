"""Fetch public PR metadata with gh, or recompute the saved cohort without network access."""

import json
import re
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


def graphql(query):
    request = ROOT / "public-query.json"
    request.write_text(json.dumps({"query": query}), encoding="utf-8")
    response = json.loads(subprocess.check_output(["gh", "api", "graphql", "--input", str(request)], encoding="utf-8"))
    assert "errors" not in response, response.get("errors")
    request.unlink()
    return response["data"]


def area(path):
    if path.startswith("docs/") or path.endswith((".md", ".rst")) or path == "mkdocs.yml":
        return "documentation"
    if path.startswith("ultralytics/"):
        return "package"
    if path.startswith("tests/"):
        return "tests"
    if path.startswith("examples/"):
        return "examples"
    if path.startswith((".github/", "docker/")):
        return "automation"
    return "project_other"


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
details_path = DATA / "pr-files-2026-q3.json"
if "--details" in sys.argv:
    details = (
        json.loads(details_path.read_text(encoding="utf-8"))
        if details_path.exists()
        else {"fetch_started_at": datetime.now(timezone.utc).isoformat(), "prs": {}}
    )
    pending = [r["number"] for r in rows if str(r["number"]) not in details["prs"]]
    for offset in range(0, len(pending), 25):
        numbers = pending[offset : offset + 25]
        fields = [
            f"p{n}: pullRequest(number: {n}) {{ number headRefOid additions deletions changedFiles state mergedAt files(first: 100) {{ nodes {{ path additions deletions }} pageInfo {{ hasNextPage endCursor }} }} }}"
            for n in numbers
        ]
        batch = graphql('query { repository(owner: "ultralytics", name: "ultralytics") { ' + " ".join(fields) + " } }")[
            "repository"
        ]
        for pr in batch.values():
            assert pr is not None
            files = pr.pop("files")
            paths = files["nodes"]
            while files["pageInfo"]["hasNextPage"]:
                cursor = json.dumps(files["pageInfo"]["endCursor"])
                query = f'query {{ repository(owner: "ultralytics", name: "ultralytics") {{ pullRequest(number: {pr["number"]}) {{ files(first: 100, after: {cursor}) {{ nodes {{ path additions deletions }} pageInfo {{ hasNextPage endCursor }} }} }} }} }}'
                files = graphql(query)["repository"]["pullRequest"]["files"]
                paths.extend(files["nodes"])
            assert len(paths) == pr["changedFiles"], pr["number"]
            assert len({p["path"] for p in paths}) == len(paths)
            details["prs"][str(pr["number"])] = {**pr, "files": paths}
        details["fetched_at"] = datetime.now(timezone.utc).isoformat()
        details_path.write_text(json.dumps(details, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"file details: {len(details['prs'])}/{len(rows)} PRs", flush=True)
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
        response = graphql("query { " + " ".join(fields) + " }")
        for i, author in enumerate(batch):
            histories[author] = {
                "prior_prs": response[f"prior{i}"]["issueCount"],
                "prior_merged": response[f"merged{i}"]["issueCount"],
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
timeline_path = DATA / "pr-external-timeline-2026-q3.json"
if "--timeline" in sys.argv:
    timeline = (
        json.loads(timeline_path.read_text(encoding="utf-8"))
        if timeline_path.exists()
        else {"fetch_started_at": datetime.now(timezone.utc).isoformat(), "prs": {}}
    )
    actor = "author { login __typename } authorAssociation"
    events = (
        "... on ClosedEvent { actor { login __typename } createdAt } ... on MarkedAsDuplicateEvent { createdAt } "
        "... on CrossReferencedEvent { createdAt source { __typename ... on PullRequest { number merged author { login } } } }"
    )
    pending = [r["number"] for r in rows if r["author"] in histories and str(r["number"]) not in timeline["prs"]]
    for offset in range(0, len(pending), 10):
        fields = [
            f"p{n}: pullRequest(number: {n}) {{ number comments(first: 100) {{ nodes {{ {actor} createdAt url }} }} "
            f"reviews(first: 100) {{ nodes {{ {actor} submittedAt url }} }} "
            f"timelineItems(last: 50, itemTypes: [CLOSED_EVENT, MARKED_AS_DUPLICATE_EVENT, CROSS_REFERENCED_EVENT]) {{ nodes {{ __typename {events} }} }} }}"
            for n in pending[offset : offset + 10]
        ]
        batch = graphql('query { repository(owner: "ultralytics", name: "ultralytics") { ' + " ".join(fields) + " } }")[
            "repository"
        ]
        for pr in batch.values():
            # First pages are chronological, so they always contain the earliest response.
            timeline["prs"][str(pr["number"])] = {k: v["nodes"] if isinstance(v, dict) else v for k, v in pr.items()}
        timeline["fetched_at"] = datetime.now(timezone.utc).isoformat()
        timeline_path.write_text(json.dumps(timeline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"timeline: {len(timeline['prs'])}/{len(pending) + len(timeline['prs']) - offset - len(fields)}", flush=True)
if timeline_path.exists() and history_path.exists():
    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))["prs"]
    external = [r for r in rows if r["author"] in histories]
    if set(timeline) == {str(r["number"]) for r in external}:
        bots = {"ultralyticsassistant", "copilot", "copilot-pull-request-reviewer"}

        def responses(row, maintainers_only):
            pr = timeline[str(row["number"])]
            items = [(c["createdAt"], c) for c in pr["comments"]] + [
                (r["submittedAt"], r) for r in pr["reviews"] if r["submittedAt"]
            ]
            # Merging, or closing by someone else, also answers the author.
            closed = [e for e in pr["timelineItems"] if e["__typename"] == "ClosedEvent"]
            if row["merged_at"]:
                items.append((row["merged_at"], {"author": {"login": "", "__typename": "User"}, "authorAssociation": "MEMBER"}))
            elif closed and closed[0]["actor"]:
                items.append((closed[0]["createdAt"], {"author": closed[0]["actor"], "authorAssociation": "MEMBER"}))
            return sorted(
                t
                for t, c in items
                if c["author"]
                and c["author"]["__typename"] != "Bot"
                and c["author"]["login"].lower() not in bots | {row["author"].lower()}
                and (not maintainers_only or c["authorAssociation"] in {"MEMBER", "OWNER", "COLLABORATOR"})
            )

        def hours_summary(values, total):
            values = sorted(values)

            def pick(p):
                if not values:
                    return None
                x = (len(values) - 1) * p
                lo = int(x)
                return round(values[lo] + (values[min(lo + 1, len(values) - 1)] - values[lo]) * (x - lo), 2)

            return {
                "prs": total,
                "responded": len(values),
                "median_hours": pick(0.5),
                "p75_hours": pick(0.75),
                "p90_hours": pick(0.9),
                "within_24h": sum(v <= 24 for v in values),
                "within_72h": sum(v <= 72 for v in values),
            }

        first_response = {}
        for status, selected in (
            ("all", external),
            ("merged", [r for r in external if r["merged_at"]]),
            ("not_merged", [r for r in external if not r["merged_at"]]),
        ):
            first_response[status] = hours_summary(
                [elapsed(r["created_at"], t[0]) for r in selected if (t := responses(r, True))], len(selected)
            )
        first_response["any_human_all"] = hours_summary(
            [elapsed(r["created_at"], t[0]) for r in external if (t := responses(r, False))], len(external)
        )
        closers = Counter()
        for row in external:
            if row["merged_at"] or row["state"] != "closed":
                continue
            closed = [e for e in timeline[str(row["number"])]["timelineItems"] if e["__typename"] == "ClosedEvent"]
            who = closed[-1]["actor"] if closed and closed[-1]["actor"] else None
            closers[
                "author"
                if who and who["login"] == row["author"]
                else "automation"
                if not who or who["__typename"] == "Bot" or who["login"].lower() in bots
                else "other_human"
            ] += 1
        result["external_first_response"] = first_response
        result["external_closed_unmerged_by"] = dict(closers)
        reasons_path = DATA / "pr-closed-reasons-2026-q3.json"
        if reasons_path.exists():
            reasons = json.loads(reasons_path.read_text(encoding="utf-8"))["labels"]
            assert set(reasons) == {
                str(r["number"]) for r in external if r["state"] == "closed" and not r["merged_at"]
            }
            result["external_closed_unmerged_reasons"] = dict(Counter(v["reason"] for v in reasons.values()).most_common())
assert sum(g["prs"] for g in result["groups"].values()) == len(rows)
assert all(g["prs"] == g["merged"] + g["closed_unmerged"] + g["open"] for g in result["groups"].values())
(DATA / "pr-summary-2026-q3.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if details_path.exists():
    details = json.loads(details_path.read_text(encoding="utf-8"))["prs"]
    if len(details) == len(rows):
        assert set(details) == {str(r["number"]) for r in rows}
        assert all(len(pr["files"]) == pr["changedFiles"] for pr in details.values())
        assert all(len({f["path"] for f in pr["files"]}) == pr["changedFiles"] for pr in details.values())
        distribution = {}
        for status, selected in (("submitted", rows), ("merged", [r for r in rows if r["merged_at"]])):
            human = [r for r in selected if group(r) not in {"AUTOMATION", "UNKNOWN_DELETED"}]
            by_author, sizes, scopes, touched, modules = (
                defaultdict(list),
                defaultdict(list),
                defaultdict(list),
                defaultdict(list),
                defaultdict(list),
            )
            for row in selected:
                pr = details[str(row["number"])]
                churn = pr["additions"] + pr["deletions"]
                size = (
                    "0"
                    if churn == 0
                    else "1-50"
                    if churn <= 50
                    else "51-200"
                    if churn <= 200
                    else "201-1000"
                    if churn <= 1000
                    else "1001+"
                )
                sizes[size].append(row)
                areas = {area(f["path"]) for f in pr["files"]}
                scope = "empty" if not areas else next(iter(areas)) + "_only" if len(areas) == 1 else "mixed"
                scopes[scope].append(row)
                for a in areas:
                    touched[a].append(row)
                for module in {f["path"].split("/")[1] for f in pr["files"] if f["path"].startswith("ultralytics/")}:
                    modules[module].append(row)
            for row in human:
                by_author[row["author"]].append(row)
            counts = sorted((len(v) for v in by_author.values()), reverse=True)
            distribution[status] = {
                "prs": len(selected),
                "human_prs": len(human),
                "human_authors": len(by_author),
                "top_authors": sorted(((a, len(v)) for a, v in by_author.items()), key=lambda p: (-p[1], p[0]))[:10],
                "top1_share": round(100 * sum(counts[:1]) / len(human), 2),
                "top5_share": round(100 * sum(counts[:5]) / len(human), 2),
                "top10_share": round(100 * sum(counts[:10]) / len(human), 2),
                "authors_one_pr": sum(c == 1 for c in counts),
                "authors_2_to_5": sum(2 <= c <= 5 for c in counts),
                "authors_6_plus": sum(c >= 6 for c in counts),
                "median_changed_files": median(details[str(r["number"])]["changedFiles"] for r in selected),
                "median_churn": median(
                    details[str(r["number"])]["additions"] + details[str(r["number"])]["deletions"] for r in selected
                ),
                "size_groups": {g: summarize(rs) for g, rs in sorted(sizes.items())},
                "exclusive_scopes": {g: summarize(rs) for g, rs in sorted(scopes.items())},
                "touched_areas": {g: summarize(rs) for g, rs in sorted(touched.items())},
                "area_relations": {a: dict(Counter(group(r) for r in rs)) for a, rs in sorted(touched.items())},
                "package_modules": {g: summarize(rs) for g, rs in sorted(modules.items())},
                "external_size_groups": {
                    g: summarize(external)
                    for g, rs in sorted(sizes.items())
                    if (external := [r for r in rs if r["author"] in histories])
                },
                "external_scopes": {
                    g: summarize(external)
                    for g, rs in sorted(scopes.items())
                    if (external := [r for r in rs if r["author"] in histories])
                },
            }
            assert sum(len(v) for v in scopes.values()) == len(selected)
            assert sum(len(v) for v in sizes.values()) == len(selected)
        (DATA / "pr-distribution-2026-q3.json").write_text(
            json.dumps(distribution, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
conversation_path = DATA / "pr-review-conversations-2026-q3.json"
if "--conversations" in sys.argv:
    conversations = (
        json.loads(conversation_path.read_text(encoding="utf-8"))
        if conversation_path.exists()
        else {"fetch_started_at": datetime.now(timezone.utc).isoformat(), "prs": {}}
    )
    selected = sorted((r for r in first_prs.values()), key=lambda r: r["number"])
    connections = {
        "comments": "author { login __typename } authorAssociation body createdAt lastEditedAt url",
        "reviews": "author { login __typename } authorAssociation submittedAt url",
        "timelineItems": "... on ReviewRequestedEvent { actor { login __typename } createdAt requestedReviewer { __typename ... on User { login } } }",
        "reviewThreads": "id comments(first: 100) { totalCount nodes { author { login __typename } authorAssociation body createdAt lastEditedAt url } pageInfo { hasNextPage endCursor } }",
    }
    pending = [r["number"] for r in selected if "inlineComments" not in conversations["prs"].get(str(r["number"]), {})]
    for offset in range(0, len(pending), 10):
        fields = []
        for n in pending[offset : offset + 10]:
            body = "number author { login } mergedAt mergedBy { login __typename }"
            for name, nodes in connections.items():
                extra = ", itemTypes: [REVIEW_REQUESTED_EVENT]" if name == "timelineItems" else ""
                body += f" {name}(first: 100{extra}) {{ totalCount nodes {{ {nodes} }} pageInfo {{ hasNextPage endCursor }} }}"
            fields.append(f"p{n}: pullRequest(number: {n}) {{ {body} }}")
        batch = graphql('query { repository(owner: "ultralytics", name: "ultralytics") { ' + " ".join(fields) + " } }")[
            "repository"
        ]
        for pr in batch.values():
            for name, node_fields in connections.items():
                connection = pr[name]
                nodes = list(connection["nodes"])
                total = connection["totalCount"]
                while connection["pageInfo"]["hasNextPage"]:
                    cursor = json.dumps(connection["pageInfo"]["endCursor"])
                    extra = ", itemTypes: [REVIEW_REQUESTED_EVENT]" if name == "timelineItems" else ""
                    query = f'query {{ repository(owner: "ultralytics", name: "ultralytics") {{ pullRequest(number: {pr["number"]}) {{ {name}(first: 100, after: {cursor}{extra}) {{ nodes {{ {node_fields} }} pageInfo {{ hasNextPage endCursor }} }} }} }} }}'
                    connection = graphql(query)["repository"]["pullRequest"][name]
                    nodes.extend(connection["nodes"])
                # Filtered timeline totalCount also includes other event types; pageInfo owns completeness.
                if name != "timelineItems":
                    assert len(nodes) == total, (pr["number"], name)
                pr[name] = nodes
            pr["inlineComments"] = []
            for thread in pr.pop("reviewThreads"):
                connection = thread["comments"]
                nodes = list(connection["nodes"])
                total = connection["totalCount"]
                while connection["pageInfo"]["hasNextPage"]:
                    query = f"query {{ node(id: {json.dumps(thread['id'])}) {{ ... on PullRequestReviewThread {{ comments(first: 100, after: {json.dumps(connection['pageInfo']['endCursor'])}) {{ nodes {{ {connections['comments']} }} pageInfo {{ hasNextPage endCursor }} }} }} }} }}"
                    connection = graphql(query)["node"]["comments"]
                    nodes.extend(connection["nodes"])
                assert len(nodes) == total
                pr["inlineComments"].extend(nodes)
            # Keep other participants' identities and timing, not their full conversation text.
            for comment in pr["comments"] + pr["inlineComments"]:
                if not comment["author"] or comment["author"]["login"] != pr["author"]["login"]:
                    del comment["body"]
            conversations["prs"][str(pr["number"])] = pr
        conversations["fetched_at"] = datetime.now(timezone.utc).isoformat()
        conversation_path.write_text(json.dumps(conversations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"conversations: {len(conversations['prs'])}/{len(selected)}", flush=True)

if conversation_path.exists():
    conversations = json.loads(conversation_path.read_text(encoding="utf-8"))["prs"]
    if len(conversations) == len(first_prs) and all("inlineComments" in pr for pr in conversations.values()):
        maintainers = {r["author"].lower() for r in rows if group(r) in {"MEMBER", "COLLABORATOR", "OWNER"}}
        mention_rows = []
        for (experience, _), row in first_prs.items():
            pr = conversations[str(row["number"])]
            cutoff = row["merged_at"] or row["closed_at"] or snapshot["fetched_at"]
            author = row["author"].lower()
            reviewers = {
                r["author"]["login"].lower()
                for r in pr["reviews"]
                if r["author"]
                and r["author"]["__typename"] != "Bot"
                and r["submittedAt"]
                and elapsed(r["submittedAt"], cutoff) >= 0
            }
            targets = maintainers | reviewers
            all_comments = pr["comments"] + pr["inlineComments"]
            targets.update(
                c["author"]["login"].lower()
                for c in all_comments
                if c["author"]
                and c["author"]["__typename"] != "Bot"
                and c["authorAssociation"] in {"MEMBER", "OWNER", "COLLABORATOR"}
                and elapsed(c["createdAt"], cutoff) >= 0
            )
            if pr["mergedBy"] and pr["mergedBy"]["__typename"] != "Bot":
                targets.add(pr["mergedBy"]["login"].lower())
            requests = [r for r in pr["timelineItems"] if elapsed(r["createdAt"], cutoff) >= 0]
            for request in requests:
                target = request["requestedReviewer"]
                if target and target["__typename"] == "User":
                    targets.add(target["login"].lower())
            candidates = []
            for comment in all_comments:
                if "body" not in comment or elapsed(comment["createdAt"], cutoff) < 0:
                    continue
                body = re.sub(r"```.*?```|~~~.*?~~~", "", comment["body"], flags=re.DOTALL)
                body = re.sub(r"(?m)^\s*>.*$|`[^`\n]+`", "", body)
                mentions = {
                    m.lower()
                    for m in re.findall(r"(?<![\w/])@([A-Za-z0-9][A-Za-z0-9-]*(?:\[bot\])?(?:/[A-Za-z0-9_-]+)?)", body)
                }
                if mentions:
                    candidates.append(
                        {
                            "url": comment["url"],
                            "created_at": comment["createdAt"],
                            "edited_after_cutoff": bool(
                                comment["lastEditedAt"] and elapsed(comment["lastEditedAt"], cutoff) < 0
                            ),
                            "mentions": sorted(mentions),
                            "reviewer_targets": sorted(
                                (mentions & targets)
                                - {author, "ultralyticsassistant", "copilot", "copilot-pull-request-reviewer"}
                            ),
                            "prior_participants": sorted(
                                {
                                    c["author"]["login"].lower()
                                    for c in all_comments
                                    if c["author"] and elapsed(c["createdAt"], comment["createdAt"]) > 0
                                }
                                | {
                                    r["author"]["login"].lower()
                                    for r in pr["reviews"]
                                    if r["author"]
                                    and r["submittedAt"]
                                    and elapsed(r["submittedAt"], comment["createdAt"]) > 0
                                }
                            ),
                            "body": comment["body"],
                        }
                    )
            mention_rows.append(
                {
                    "number": row["number"],
                    "author": row["author"],
                    "experience": experience,
                    "merged": bool(row["merged_at"]),
                    "cutoff": cutoff,
                    "author_requested_review": any(
                        r["actor"] and r["actor"]["login"].lower() == author for r in requests
                    ),
                    "review_request_events": requests,
                    "mention_comments": candidates,
                }
            )
        assert len({r["number"] for r in mention_rows}) == len(first_prs)
        (DATA / "pr-review-mention-candidates.json").write_text(
            json.dumps(mention_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
print(json.dumps({k: v for k, v in result.items() if k != "monthly_groups"}, ensure_ascii=False, indent=2))
