#!/usr/bin/env python3
"""Render the benchmark tables in README.md / README_CN.md from benchmarks.yaml.

Single source of truth: data/benchmarks.yaml (human-curated).
Machine-managed columns (Stars / Updated) are fetched from the GitHub REST API
and injected only into the marked table blocks:

    <!-- AEE-TABLE:VLM:START --> ... <!-- AEE-TABLE:VLM:END -->
    <!-- AEE-TABLE:VLA:START --> ... <!-- AEE-TABLE:VLA:END -->
    <!-- AEE-TABLE:WM:START -->  ... <!-- AEE-TABLE:WM:END -->

Everything outside the markers (prose, related lists, etc.) is left untouched.

The script is idempotent: a file is only rewritten when its rendered content
actually changes. Transient GitHub API failures fall back to the cache in
data/.cache/metadata.json so existing values are never wiped to blanks.

Usage:
    python scripts/render_readme.py            # render in place
    python scripts/render_readme.py --check     # exit 1 if files would change
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = REPO_ROOT / "data" / "benchmarks.yaml"
CACHE_PATH = REPO_ROOT / "data" / ".cache" / "metadata.json"
README_EN = REPO_ROOT / "README.md"
README_CN = REPO_ROOT / "README_CN.md"

GITHUB_API = "https://api.github.com/repos/{repo}"
PLACEHOLDER = "—"

# Track render order and the marker key used in the README comment markers.
TRACKS = [
    ("vlm", "VLM"),
    ("vla", "VLA"),
    ("wm", "WM"),
]

HEADERS = {
    "en": ["Benchmark", "Year", "What it tests", "Metric", "Stars", "Updated", "Links"],
    "cn": ["基准", "年份", "评什么", "指标", "Stars", "最近更新", "链接"],
}


def gh_headers() -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def fetch_repo_meta(repo: str, cache: dict) -> dict | None:
    """Return {'stars': int, 'updated': 'YYYY-MM'} for a repo, or None.

    On API failure, fall back to any cached value for the repo.
    """
    try:
        resp = requests.get(GITHUB_API.format(repo=repo), headers=gh_headers(), timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            meta = {
                "stars": int(data.get("stargazers_count", 0)),
                "updated": (data.get("pushed_at") or "")[:7],  # YYYY-MM
            }
            cache[repo] = meta
            return meta
        print(f"[warn] GitHub API {resp.status_code} for {repo}; using cache", file=sys.stderr)
    except requests.RequestException as exc:
        print(f"[warn] GitHub API error for {repo}: {exc}; using cache", file=sys.stderr)
    return cache.get(repo)


def fmt_stars(stars: int | None) -> str:
    if stars is None:
        return PLACEHOLDER
    if stars >= 1000:
        return f"{stars / 1000:.1f}k"
    return str(stars)


def render_links(links: list[dict], lang: str) -> str:
    label_key = "en" if lang == "en" else "cn"
    parts = []
    for link in links or []:
        label = link.get(label_key) or link.get("en") or link.get("cn") or "Link"
        parts.append(f"[{label}]({link['url']})")
    return " · ".join(parts)


def render_row(entry: dict, lang: str) -> str:
    if lang == "en":
        name = entry["name"]
        year = entry.get("year_en", "")
        tests = entry.get("tests_en", "")
        metric = entry.get("metric_en", "")
    else:
        name = entry.get("name_cn") or entry["name"]
        year = entry.get("year_cn", "")
        tests = entry.get("tests_cn", "")
        metric = entry.get("metric_cn", "")

    meta = entry.get("_meta")
    if meta:
        stars = fmt_stars(meta.get("stars"))
        updated = meta.get("updated") or PLACEHOLDER
    else:
        stars = PLACEHOLDER
        updated = PLACEHOLDER

    links = render_links(entry.get("links"), lang)
    cells = [f"**{name}**", year, tests, metric, stars, updated, links]
    return "| " + " | ".join(cells) + " |"


def render_table(entries: list[dict], lang: str) -> str:
    header = "| " + " | ".join(HEADERS[lang]) + " |"
    sep = "|" + "|".join(["---"] * len(HEADERS[lang])) + "|"
    rows = [render_row(e, lang) for e in entries]
    return "\n".join([header, sep, *rows])


def replace_block(text: str, marker: str, body: str) -> str:
    start = f"<!-- AEE-TABLE:{marker}:START -->"
    end = f"<!-- AEE-TABLE:{marker}:END -->"
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        re.DOTALL,
    )
    if not pattern.search(text):
        raise ValueError(f"Marker block AEE-TABLE:{marker} not found")
    replacement = f"{start}\n{body}\n{end}"
    return pattern.sub(lambda _m: replacement, text)


def render_readme(path: Path, entries_by_track: dict, lang: str) -> bool:
    """Render one README file. Return True if the file content changed."""
    text = path.read_text(encoding="utf-8")
    new_text = text
    for track, marker in TRACKS:
        table = render_table(entries_by_track.get(track, []), lang)
        new_text = replace_block(new_text, marker, table)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write; exit 1 if the rendered output differs from on-disk files.",
    )
    args = parser.parse_args()

    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    benchmarks = data.get("benchmarks", [])

    cache = load_cache()
    for entry in benchmarks:
        repo = entry.get("repo")
        entry["_meta"] = fetch_repo_meta(repo, cache) if repo else None
    save_cache(cache)

    entries_by_track: dict[str, list[dict]] = {track: [] for track, _ in TRACKS}
    for entry in benchmarks:
        track = entry.get("track")
        if track in entries_by_track:
            entries_by_track[track].append(entry)
        else:
            print(f"[warn] unknown track '{track}' for entry '{entry.get('name')}'", file=sys.stderr)

    if args.check:
        changed = False
        for path, lang in [(README_EN, "en"), (README_CN, "cn")]:
            text = path.read_text(encoding="utf-8")
            new_text = text
            for track, marker in TRACKS:
                table = render_table(entries_by_track.get(track, []), lang)
                new_text = replace_block(new_text, marker, table)
            if new_text != text:
                print(f"[check] {path.name} would change")
                changed = True
        return 1 if changed else 0

    changed_files = []
    for path, lang in [(README_EN, "en"), (README_CN, "cn")]:
        if render_readme(path, entries_by_track, lang):
            changed_files.append(path.name)

    if changed_files:
        print(f"[ok] updated: {', '.join(changed_files)}")
    else:
        print("[ok] no changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
