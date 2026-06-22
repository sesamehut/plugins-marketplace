#!/usr/bin/env python3
"""Snapshot GitHub traffic (clones + views) into per-repo CSV history.

GitHub retains only the last 14 days of traffic, so this is meant to run daily
(see ../.github/workflows/traffic.yml). Each run upserts every day the API
returns, keyed by date: past days converge to their final totals and today's
partial counts are refreshed until they age out of the 14-day window. No data is
ever dropped once a day has been recorded.

Auth: uses `gh api`, so `gh` must be authenticated with a token that has push
access to each repo. The built-in Actions GITHUB_TOKEN canNOT read the traffic
endpoints (they require push access the token lacks); the workflow injects a PAT
via the GH_TOKEN env var instead.

clones != installs: CI, mirrors, and archive bots clone too. `total` and
`unique` are kept in separate columns precisely so that machine noise (which
shows up as a high total-to-unique ratio) can be filtered downstream.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

# Track every repo you can push to. The marketplace repo has no CI, so its
# `unique` column is the cleanest "people who added the market" signal. Repos
# that also run CI (e.g. the plugin source) have inflated totals; trust their
# `unique` column and discount high total/unique days as automation.
REPOS = [
    "sesamehut/plugins-marketplace",
    "sesamehut/appstore-connect-skill",
    # add more "owner/repo" lines here
]

FIELDS = ["date", "clones_total", "clones_unique", "views_total", "views_unique"]
OUT_DIR = Path(__file__).resolve().parent


def gh_api(path):
    proc = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"gh api {path} failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def load(csv_path):
    rows = {}
    if csv_path.exists():
        with csv_path.open(newline="") as f:
            for row in csv.DictReader(f):
                rows[row["date"]] = row
    return rows


def row_for(rows, date):
    if date not in rows:
        rows[date] = {key: "" for key in FIELDS}
        rows[date]["date"] = date
    return rows[date]


def collect(repo):
    slug = repo.split("/")[-1]
    csv_path = OUT_DIR / f"{slug}.csv"
    rows = load(csv_path)

    for day in gh_api(f"repos/{repo}/traffic/clones").get("clones", []):
        row = row_for(rows, day["timestamp"][:10])
        row["clones_total"] = day["count"]
        row["clones_unique"] = day["uniques"]

    for day in gh_api(f"repos/{repo}/traffic/views").get("views", []):
        row = row_for(rows, day["timestamp"][:10])
        row["views_total"] = day["count"]
        row["views_unique"] = day["uniques"]

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for date in sorted(rows):
            writer.writerow(rows[date])
    print(f"{repo}: {len(rows)} days -> {csv_path.name}")


def main():
    failures = []
    for repo in REPOS:
        try:
            collect(repo)
        except Exception as err:  # one inaccessible repo must not lose the rest
            print(f"{repo}: SKIPPED ({err})", file=sys.stderr)
            failures.append(repo)
    if failures:
        # Exit non-zero so the run is flagged, but only after archiving the repos
        # that did succeed.
        raise SystemExit(f"failed for: {', '.join(failures)}")


if __name__ == "__main__":
    main()
