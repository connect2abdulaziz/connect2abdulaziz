#!/usr/bin/env python3
"""Generate languages.svg from all accessible GitHub repositories."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import requests

TOKEN = os.environ.get("GH_TOKEN")
if not TOKEN:
    print("Error: Missing GH_TOKEN", file=sys.stderr)
    sys.exit(1)

API = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
IGNORED = {"HTML", "CSS", "Jupyter Notebook", "Dockerfile", "Makefile"}
MIN_PCT = 1.0
MAX_LANGS = 8
ROOT = Path(__file__).resolve().parents[1]


def fetch_language_sizes() -> Dict[str, int]:
    lang_sizes: Dict[str, int] = {}
    after = None
    query = """
    query($after: String) {
      viewer {
        repositories(
          first: 100,
          after: $after,
          affiliations: [OWNER, ORGANIZATION_MEMBER, COLLABORATOR],
          isFork: false,
          orderBy: {field: UPDATED_AT, direction: DESC}
        ) {
          pageInfo { hasNextPage endCursor }
          nodes {
            languages(first: 100, orderBy: {field: SIZE, direction: DESC}) {
              edges { size node { name } }
            }
          }
        }
      }
    }
    """

    while True:
        response = requests.post(
            API,
            json={"query": query, "variables": {"after": after}},
            headers=HEADERS,
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        if "errors" in payload:
            print(f"GraphQL errors: {payload['errors']}", file=sys.stderr)
            sys.exit(1)

        repos = payload["data"]["viewer"]["repositories"]
        for repo in repos["nodes"]:
            for edge in repo["languages"]["edges"]:
                name = edge["node"]["name"]
                if name not in IGNORED:
                    lang_sizes[name] = lang_sizes.get(name, 0) + int(edge["size"])

        if not repos["pageInfo"]["hasNextPage"]:
            break
        after = repos["pageInfo"]["endCursor"]

    return lang_sizes


def process(lang_sizes: Dict[str, int]) -> List[Tuple[str, float]]:
    if not lang_sizes:
        return []
    items = sorted(lang_sizes.items(), key=lambda x: x[1], reverse=True)
    total = sum(size for _, size in items)
    percentages = [(name, (size / total) * 100.0) for name, size in items]
    major = [(n, p) for n, p in percentages if p >= MIN_PCT]
    other = sum(p for _, p in percentages if p < MIN_PCT)
    if other > 0:
        major.append(("Other", other))
    return major[:MAX_LANGS]


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def generate_svg(languages: List[Tuple[str, float]], updated: str) -> str:
    if not languages:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="60">
  <rect width="100%" height="100%" fill="#0d1117" rx="8"/>
  <text x="20" y="35" font-family="system-ui,sans-serif" font-size="14" fill="#c9d1d9">No language data available</text>
</svg>
"""

    width = 1000
    left, right, top, bottom = 100, 36, 100, 100
    bar_h, gap = 26, 12
    n = len(languages)
    height = top + bottom + n * bar_h + (n - 1) * gap
    chart_left = left
    chart_right = width - right
    chart_top = top
    chart_bottom = height - bottom
    chart_w = chart_right - chart_left

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        """
<style>
  :root { --bg:#ffffff; --fg:#1f2328; --muted:#66707a; --bar:#0969da; --grid:#e6e8eb; }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#0d1117; --fg:#c9d1d9; --muted:#8b949e; --bar:#58a6ff; --grid:#30363d; }
  }
  text { font-family: system-ui,-apple-system,"Segoe UI",sans-serif; dominant-baseline: middle; }
  .title { font-weight:600; font-size:16px; fill:var(--fg); }
  .small { font-size:12px; fill:var(--muted); }
  .label { font-size:13px; fill:var(--fg); }
  .value { font-size:12px; fill:var(--fg); }
</style>
""",
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="14" fill="var(--bg)"/>',
        f'<text x="{left}" y="{top - 24}" class="title">Programming Languages Distribution</text>',
    ]

    for tick in (0, 20, 40, 60, 80, 100):
        x = chart_left + chart_w * tick / 100.0
        parts.append(
            f'<line x1="{x:.1f}" y1="{chart_top}" x2="{x:.1f}" y2="{chart_bottom}" stroke="var(--grid)" stroke-width="1" opacity="0.5"/>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{chart_bottom + 18}" class="small" text-anchor="middle">{tick}%</text>'
        )

    for i, (name, pct) in enumerate(languages):
        y = chart_top + i * (bar_h + gap)
        bar_w = chart_w * (pct / 100.0)
        parts.append(
            f'<text x="{left - 12}" y="{y + bar_h / 2}" class="label" text-anchor="end">{escape(name)}</text>'
        )
        parts.append(
            f'<rect x="{chart_left}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" rx="6" fill="var(--bar)"/>'
        )
        if bar_w < 46:
            tx, anchor = chart_left + bar_w + 6, "start"
        else:
            tx, anchor = chart_left + bar_w - 6, "end"
        parts.append(
            f'<text x="{tx:.1f}" y="{y + bar_h / 2}" class="value" text-anchor="{anchor}">{pct:.1f}%</text>'
        )

    parts.append(
        f'<text x="{width - right}" y="{height - 20}" class="small" text-anchor="end">Updated {escape(updated)} · all accessible repos</text>'
    )
    parts.append("</svg>")
    return "".join(parts)


def main() -> None:
    now = datetime.now(timezone.utc)
    updated = now.strftime("%Y-%m-%d")
    print("Fetching language data...")
    sizes = fetch_language_sizes()
    languages = process(sizes)
    svg = generate_svg(languages, updated)

    (ROOT / "languages.svg").write_text(svg, encoding="utf-8")

    meta_dir = ROOT / "data"
    meta_dir.mkdir(exist_ok=True)
    meta = {
        "lastRefresh": now.isoformat(),
        "languages": [{"name": n, "percent": round(p, 2)} for n, p in languages],
    }
    (meta_dir / "last-refresh.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote languages.svg and data/last-refresh.json ({len(languages)} languages)")


if __name__ == "__main__":
    main()
