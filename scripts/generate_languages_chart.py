#!/usr/bin/env python3
"""Generate a premium languages.svg from all accessible GitHub repositories."""

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

# GitHub Linguist-inspired palette
LANG_COLORS: Dict[str, str] = {
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "PHP": "#4F5D95",
    "Python": "#3572A5",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "Java": "#b07219",
    "C": "#555555",
    "C++": "#f34b7d",
    "C#": "#178600",
    "Ruby": "#701516",
    "Swift": "#F05138",
    "Kotlin": "#A97BFF",
    "Dart": "#00B4AB",
    "Shell": "#89e051",
    "Vue": "#41b883",
    "Svelte": "#ff3e00",
    "Haskell": "#5e5086",
    "Scala": "#c22d40",
    "Elixir": "#6e4a7e",
    "Liquid": "#67b8de",
    "SCSS": "#c6538c",
    "CSS": "#563d7c",
    "HTML": "#e34c26",
    "Markdown": "#083fa1",
    "Other": "#8b949e",
}

FALLBACK_PALETTE = [
    "#58a6ff",
    "#3fb950",
    "#d2a8ff",
    "#ffa657",
    "#ff7b72",
    "#79c0ff",
    "#56d364",
    "#e3b341",
]


def lang_color(name: str, index: int) -> str:
    if name in LANG_COLORS:
        return LANG_COLORS[name]
    return FALLBACK_PALETTE[index % len(FALLBACK_PALETTE)]


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
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def generate_svg(languages: List[Tuple[str, float]], updated: str, dark: bool = True) -> str:
    if not languages:
        bg = "#0d1117" if dark else "#ffffff"
        fg = "#c9d1d9" if dark else "#1f2328"
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="80" viewBox="0 0 840 80">
  <rect width="840" height="80" rx="12" fill="{bg}"/>
  <text x="32" y="46" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="14" fill="{fg}">No language data available</text>
</svg>
"""

    if dark:
        bg, border, title, muted, track = (
            "#0d1117",
            "#30363d",
            "#e6edf3",
            "#8b949e",
            "#21262d",
        )
    else:
        bg, border, title, muted, track = (
            "#ffffff",
            "#d0d7de",
            "#1f2328",
            "#656d76",
            "#eaeef2",
        )

    width = 840
    pad_x = 32
    header_h = 72
    spectrum_h = 10
    row_h = 36
    footer_h = 44
    n = len(languages)
    height = header_h + spectrum_h + 28 + n * row_h + footer_h

    # Normalize spectrum to 100% of displayed languages
    shown_total = sum(p for _, p in languages) or 1.0
    colors = [lang_color(name, i) for i, (name, _) in enumerate(languages)]

    parts: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Top languages">'
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="{bg}" stroke="{border}"/>'
        f'<text x="{pad_x}" y="38" fill="{title}" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Helvetica,Arial,sans-serif" font-size="18" font-weight="600">Top Languages</text>'
        f'<text x="{width - pad_x}" y="38" fill="{muted}" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif" font-size="12" text-anchor="end">Across public &amp; private repos</text>'
        f'<rect x="{pad_x}" y="50" width="40" height="3" rx="1.5" fill="#58a6ff"/>'
    ]

    # Stacked spectrum bar
    spectrum_y = header_h
    spectrum_w = width - pad_x * 2
    x_cursor = pad_x
    parts.append(
        f'<rect x="{pad_x}" y="{spectrum_y}" width="{spectrum_w}" height="{spectrum_h}" rx="5" fill="{track}"/>'
    )
    for i, ((name, pct), color) in enumerate(zip(languages, colors)):
        seg_w = max(spectrum_w * (pct / shown_total), 2.0)
        # Clip last segment to fit
        if i == n - 1:
            seg_w = pad_x + spectrum_w - x_cursor
        # Rounded ends via first/last mask feel — use rects with clip on container
        parts.append(
            f'<rect x="{x_cursor:.1f}" y="{spectrum_y}" width="{seg_w:.1f}" height="{spectrum_h}" fill="{color}"/>'
        )
        x_cursor += seg_w
    # Soft rounded overlay mask edges
    parts.append(
        f'<rect x="{pad_x}" y="{spectrum_y}" width="{spectrum_w}" height="{spectrum_h}" rx="5" fill="none" stroke="{bg}" stroke-width="0"/>'
    )
    # Re-draw rounded clip using a mask-like border match
    parts.append(
        f'<rect x="{pad_x}" y="{spectrum_y}" width="{spectrum_w}" height="{spectrum_h}" rx="5" fill="none" stroke="{border}" stroke-width="1" opacity="0.35"/>'
    )

    # Language rows
    rows_top = spectrum_y + spectrum_h + 28
    bar_max = 320
    bar_x = width - pad_x - bar_max - 64  # leave room for %
    for i, ((name, pct), color) in enumerate(zip(languages, colors)):
        y = rows_top + i * row_h
        cy = y + 10
        bar_w = max(bar_max * (pct / 100.0), 4.0)

        # Dot
        parts.append(f'<circle cx="{pad_x + 6}" cy="{cy}" r="5" fill="{color}"/>')
        # Name
        parts.append(
            f'<text x="{pad_x + 22}" y="{cy + 1}" fill="{title}" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif" font-size="14" font-weight="500" dominant-baseline="middle">{escape(name)}</text>'
        )
        # Track + fill
        parts.append(
            f'<rect x="{bar_x}" y="{cy - 4}" width="{bar_max}" height="8" rx="4" fill="{track}"/>'
        )
        parts.append(
            f'<rect x="{bar_x}" y="{cy - 4}" width="{bar_w:.1f}" height="8" rx="4" fill="{color}"/>'
        )
        # Percent
        parts.append(
            f'<text x="{width - pad_x}" y="{cy + 1}" fill="{muted}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="13" text-anchor="end" dominant-baseline="middle">{pct:5.1f}%</text>'
        )

    # Footer
    parts.append(
        f'<text x="{pad_x}" y="{height - 18}" fill="{muted}" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif" font-size="11">Updated {escape(updated)}</text>'
    )
    parts.append(
        f'<text x="{width - pad_x}" y="{height - 18}" fill="{muted}" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif" font-size="11" text-anchor="end">Self-hosted · daily refresh</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    now = datetime.now(timezone.utc)
    updated = now.strftime("%Y-%m-%d")
    print("Fetching language data...")
    sizes = fetch_language_sizes()
    languages = process(sizes)

    dark = generate_svg(languages, updated, dark=True)
    light = generate_svg(languages, updated, dark=False)

    (ROOT / "languages.svg").write_text(dark, encoding="utf-8")
    (ROOT / "languages-dark.svg").write_text(dark, encoding="utf-8")
    (ROOT / "languages-light.svg").write_text(light, encoding="utf-8")

    meta_dir = ROOT / "data"
    meta_dir.mkdir(exist_ok=True)
    meta = {
        "lastRefresh": now.isoformat(),
        "languages": [{"name": n, "percent": round(p, 2)} for n, p in languages],
    }
    (meta_dir / "last-refresh.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote premium language cards ({len(languages)} languages)")


if __name__ == "__main__":
    main()
