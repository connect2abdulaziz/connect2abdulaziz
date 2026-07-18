#!/usr/bin/env python3
"""Generate self-hosted GitHub stats SVGs (no third-party vercel hosts)."""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

TOKEN = os.environ.get("GH_TOKEN")
USERNAME = os.environ.get("GH_USERNAME", "connect2abdulaziz")
if not TOKEN:
    print("Error: Missing GH_TOKEN", file=sys.stderr)
    sys.exit(1)

API = "https://api.github.com/graphql"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "connect2abdulaziz-profile-stats",
}
ROOT = Path(__file__).resolve().parents[1]

QUERY = """
query($login: String!) {
  user(login: $login) {
    name
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      totalCount
      nodes { stargazerCount forkCount }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoriesWithContributedCommits
      contributionCalendar {
        totalContributions
      }
    }
    pullRequests(first: 1) { totalCount }
    issues(first: 1) { totalCount }
    createdAt
  }
}
"""


def fetch_stats() -> dict:
    response = requests.post(
        API,
        json={"query": QUERY, "variables": {"login": USERNAME}},
        headers=HEADERS,
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    if "errors" in payload:
        print(f"GraphQL errors: {payload['errors']}", file=sys.stderr)
        sys.exit(1)

    user = payload["data"]["user"]
    repos = user["repositories"]["nodes"] or []
    contrib = user["contributionsCollection"]
    stars = sum(r["stargazerCount"] for r in repos)
    forks = sum(r["forkCount"] for r in repos)
    year = datetime.now(timezone.utc).year

    return {
        "name": user["name"] or USERNAME,
        "followers": user["followers"]["totalCount"],
        "public_repos": user["repositories"]["totalCount"],
        "stars": stars,
        "forks": forks,
        "commits_year": contrib["totalCommitContributions"],
        "prs_year": contrib["totalPullRequestContributions"],
        "issues_year": contrib["totalIssueContributions"],
        "repos_contributed": contrib["totalRepositoriesWithContributedCommits"],
        "total_contributions": contrib["contributionCalendar"]["totalContributions"],
        "total_prs": user["pullRequests"]["totalCount"],
        "total_issues": user["issues"]["totalCount"],
        "member_since": datetime.fromisoformat(
            user["createdAt"].replace("Z", "+00:00")
        ).year,
        "year": year,
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }


def escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def fmt(n: int) -> str:
    if n >= 1000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return str(n)


def render_stats_card(stats: dict, dark: bool = True) -> str:
    if dark:
        bg, border, title, muted, accent, value = (
            "#0d1117",
            "#30363d",
            "#e6edf3",
            "#8b949e",
            "#58a6ff",
            "#e6edf3",
        )
    else:
        bg, border, title, muted, accent, value = (
            "#ffffff",
            "#d0d7de",
            "#1f2328",
            "#656d76",
            "#0969da",
            "#1f2328",
        )

    rows = [
        (fmt(stats["stars"]), "Total Stars"),
        (fmt(stats["commits_year"]), f"Commits ({stats['year']})"),
        (fmt(stats["total_prs"]), "Pull Requests"),
        (fmt(stats["total_issues"]), "Issues Opened"),
        (fmt(stats["repos_contributed"]), "Repos Contributed"),
        (fmt(stats["followers"]), "Followers"),
    ]

    # 2x3 grid
    cells = []
    for i, (num, label) in enumerate(rows):
        col = i % 3
        row = i // 3
        x = 28 + col * 155
        y = 72 + row * 48
        cells.append(
            f'<text x="{x}" y="{y}" fill="{value}" font-size="18" font-weight="700">{escape(num)}</text>'
            f'<text x="{x}" y="{y + 18}" fill="{muted}" font-size="12">{escape(label)}</text>'
        )

    return f"""<svg width="495" height="195" viewBox="0 0 495 195" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(stats['name'])} GitHub stats">
  <rect x="0.5" y="0.5" width="494" height="194" rx="8" fill="{bg}" stroke="{border}"/>
  <text x="28" y="36" fill="{title}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="18" font-weight="600">{escape(stats['name'])}'s GitHub Stats</text>
  <rect x="390" y="18" width="78" height="22" rx="11" fill="{accent}"/>
  <text x="429" y="33" fill="#ffffff" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="600" text-anchor="middle">Since {stats['member_since']}</text>
  <g font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif">
    {''.join(cells)}
  </g>
  <line x1="28" y1="168" x2="467" y2="168" stroke="{border}"/>
  <text x="28" y="184" fill="{muted}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11">{escape(fmt(stats['total_contributions']))} contributions this year · updated {escape(stats['updated'])}</text>
</svg>
"""


def render_overview_card(stats: dict) -> str:
    """Wide overview card used as the primary README graphic."""
    bg, border, title, muted, accent, value = (
        "#0d1117",
        "#30363d",
        "#e6edf3",
        "#8b949e",
        "#58a6ff",
        "#e6edf3",
    )
    metrics = [
        (fmt(stats["total_contributions"]), "Contributions (year)"),
        (fmt(stats["commits_year"]), "Commits"),
        (fmt(stats["total_prs"]), "Pull Requests"),
        (fmt(stats["stars"]), "Stars"),
        (fmt(stats["public_repos"]), "Public Repos"),
        (fmt(stats["followers"]), "Followers"),
    ]
    parts = []
    for i, (num, label) in enumerate(metrics):
        x = 40 + (i % 6) * 155
        parts.append(
            f'<text x="{x}" y="95" fill="{value}" font-size="26" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif">{escape(num)}</text>'
            f'<text x="{x}" y="118" fill="{muted}" font-size="12" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif">{escape(label)}</text>'
        )

    return f"""<svg width="980" height="150" viewBox="0 0 980 150" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GitHub activity overview">
  <rect x="0.5" y="0.5" width="979" height="149" rx="12" fill="{bg}" stroke="{border}"/>
  <text x="40" y="42" fill="{title}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="18" font-weight="600">GitHub Activity Overview</text>
  <text x="940" y="42" fill="{muted}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="12" text-anchor="end">Updated {escape(stats['updated'])}</text>
  <rect x="40" y="54" width="48" height="3" rx="1.5" fill="{accent}"/>
  {''.join(parts)}
</svg>
"""


def main() -> None:
    print(f"Fetching stats for {USERNAME}...")
    stats = fetch_stats()
    (ROOT / "github-stats-dark.svg").write_text(
        render_stats_card(stats, dark=True), encoding="utf-8"
    )
    (ROOT / "github-stats-light.svg").write_text(
        render_stats_card(stats, dark=False), encoding="utf-8"
    )
    (ROOT / "github-overview.svg").write_text(
        render_overview_card(stats), encoding="utf-8"
    )
    print(
        f"Wrote stats cards — contributions={stats['total_contributions']} "
        f"stars={stats['stars']} followers={stats['followers']}"
    )


if __name__ == "__main__":
    main()
