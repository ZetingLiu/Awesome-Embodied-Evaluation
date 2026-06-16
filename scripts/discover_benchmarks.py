#!/usr/bin/env python3
"""Auto-discover benchmark entries for VLM/VLA/WM and append to benchmarks.yaml.

Guard rails for auto insertion:
1) Must have code (GitHub repo itself).
2) Must have an identifiable paper link (arXiv / OpenReview / proceedings page).
3) Must pass relevance checks:
   - benchmark/evaluation signal
   - track-specific keyword hit threshold
   - minimum stars threshold

This script only edits data/benchmarks.yaml.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARKS_PATH = REPO_ROOT / "data" / "benchmarks.yaml"
CONFIG_PATH = REPO_ROOT / "data" / "auto_discovery.yaml"

GITHUB_SEARCH_API = "https://api.github.com/search/repositories?q={query}&sort=updated&order=desc&per_page={n}"
GITHUB_README_API = "https://api.github.com/repos/{repo}/readme"

PAPER_PATTERNS = [
    r"https?://arxiv\.org/abs/[0-9]{4}\.[0-9]{4,5}(?:v[0-9]+)?",
    r"https?://openreview\.net/forum\?id=[A-Za-z0-9_-]+",
    r"https?://proceedings\.mlr\.press/[^)\s]+",
    r"https?://openaccess\.thecvf\.com/[^)\s]+",
]


def gh_headers(raw: bool = False) -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    if raw:
        headers["Accept"] = "application/vnd.github.raw"
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def http_json(url: str, headers: dict | None = None, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_text(url: str, headers: dict | None = None, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def normalize_text(*parts: str) -> str:
    return " ".join((p or "").lower() for p in parts)


def extract_first(patterns: list[str], text: str) -> str | None:
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return m.group(0)
    return None


def infer_year(paper_url: str | None, created_at: str) -> str:
    if paper_url and "arxiv.org/abs/" in paper_url:
        m = re.search(r"arxiv\.org/abs/([0-9]{2})([0-9]{2})\.[0-9]{4,5}", paper_url)
        if m:
            return f"20{m.group(1)}"
    return created_at[:4]


def score_candidate(track_cfg: dict, global_cfg: dict, text: str, stars: int) -> tuple[bool, str]:
    benchmark_terms = global_cfg.get("benchmark_terms", [])
    track_terms = track_cfg.get("track_terms", [])
    min_track_hits = int(track_cfg.get("min_track_hits", 2))
    min_stars = int(track_cfg.get("min_stars", 0))

    has_benchmark_signal = any(term in text for term in benchmark_terms)
    track_hits = sum(1 for term in track_terms if term in text)

    if stars < min_stars:
        return False, f"stars<{min_stars}"
    if not has_benchmark_signal:
        return False, "no-benchmark-signal"
    if track_hits < min_track_hits:
        return False, f"track-hits<{min_track_hits}"
    return True, "ok"


def candidate_to_entry(track: str, track_cfg: dict, repo_item: dict, paper_url: str, readme_text: str) -> dict:
    repo_full = repo_item["full_name"]
    name = repo_item["name"]
    pretty_name = name.replace("-", " ").replace("_", " ").strip()

    # Prefer a README title if available.
    title_match = re.search(r"^#\s+(.+)$", readme_text, flags=re.MULTILINE)
    if title_match:
        candidate_name = title_match.group(1).strip()
        if 3 <= len(candidate_name) <= 80:
            pretty_name = candidate_name

    tests_en = (repo_item.get("description") or "").strip()
    if not tests_en:
        tests_en = "Benchmark details are described in the official repository and paper."
    metric_en = "Task-specific benchmark metrics (see official protocol)"

    if track == "vlm":
        tests_cn = "自动发现条目：请参考论文与官方仓库中的具身评测任务定义。"
        metric_cn = "任务定义指标（见官方协议）"
    elif track == "vla":
        tests_cn = "自动发现条目：请参考论文与官方仓库中的机器人任务评测设置。"
        metric_cn = "任务定义指标（见官方协议）"
    else:
        tests_cn = "自动发现条目：请参考论文与官方仓库中的世界模型评测维度。"
        metric_cn = "任务定义指标（见官方协议）"

    site = (repo_item.get("homepage") or "").strip()
    if site and "github.com" in site:
        site = ""

    year = infer_year(paper_url, repo_item.get("created_at", "1970-01-01T00:00:00Z"))
    links = [
        {"en": "Paper", "cn": "论文", "url": paper_url},
        {"en": "Code", "cn": "代码", "url": repo_item["html_url"]},
    ]
    if site:
        links.append({"en": "Site", "cn": "主页", "url": site})

    entry = {
        "name": pretty_name,
        "track": track,
        "year_en": year,
        "year_cn": year,
        "tests_en": tests_en,
        "tests_cn": tests_cn,
        "metric_en": metric_en,
        "metric_cn": metric_cn,
        "repo": repo_full,
        "links": links,
    }
    for k, v in (track_cfg.get("extra_fields") or {}).items():
        entry[k] = v
    return entry


def discover_for_track(track: str, cfg: dict, existing_repos: set[str]) -> list[dict]:
    global_cfg = cfg["automation"]
    track_cfg = global_cfg["tracks"][track]
    blocked = set(global_cfg.get("blocked_repos", []))
    per_track_limit = int(global_cfg.get("per_track_limit", 2))
    per_query = int(global_cfg.get("search_per_query", 15))
    discovered: list[dict] = []
    seen_repos: set[str] = set()

    for query in track_cfg.get("queries", []):
        encoded = urllib.parse.quote_plus(query)
        url = GITHUB_SEARCH_API.format(query=encoded, n=per_query)
        try:
            payload = http_json(url, headers=gh_headers(), timeout=20)
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] search failed for track={track} query='{query}': {exc}", file=sys.stderr)
            continue

        for item in payload.get("items", []):
            repo = item.get("full_name")
            if not repo or repo in blocked or repo in existing_repos or repo in seen_repos:
                continue

            try:
                readme_text = http_text(GITHUB_README_API.format(repo=repo), headers=gh_headers(raw=True), timeout=15)
            except Exception:  # noqa: BLE001
                readme_text = ""

            combined_text = normalize_text(
                item.get("name", ""),
                item.get("description", ""),
                " ".join(item.get("topics", []) or []),
                readme_text,
            )
            ok, reason = score_candidate(track_cfg, global_cfg, combined_text, int(item.get("stargazers_count", 0)))
            if not ok:
                continue

            paper_url = extract_first(PAPER_PATTERNS, readme_text) or extract_first(PAPER_PATTERNS, item.get("homepage", ""))
            if not paper_url:
                # Hard guard: must include paper link.
                print(f"[skip] {repo}: no-paper-link", file=sys.stderr)
                continue

            entry = candidate_to_entry(track, track_cfg, item, paper_url, readme_text)
            discovered.append(entry)
            seen_repos.add(repo)
            print(f"[add] {track}: {repo} ({reason})")
            if len(discovered) >= per_track_limit:
                break

        if len(discovered) >= per_track_limit:
            break

    return discovered


def insert_entries(benchmarks: list[dict], track: str, new_entries: list[dict]) -> list[dict]:
    if not new_entries:
        return benchmarks
    # Append to the end of the same track block.
    last_idx = -1
    for i, e in enumerate(benchmarks):
        if e.get("track") == track:
            last_idx = i
    if last_idx == -1:
        return benchmarks + new_entries
    return benchmarks[: last_idx + 1] + new_entries + benchmarks[last_idx + 1 :]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print discoveries without writing benchmarks.yaml")
    args = parser.parse_args()

    bench_data = yaml.safe_load(BENCHMARKS_PATH.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    benchmarks: list[dict] = bench_data.get("benchmarks", [])

    existing_repos = {e.get("repo") for e in benchmarks if e.get("repo")}
    by_track_new: dict[str, list[dict]] = {}
    total_new = 0

    for track in ("vlm", "vla", "wm"):
        discovered = discover_for_track(track, cfg, existing_repos)
        by_track_new[track] = discovered
        for e in discovered:
            repo = e.get("repo")
            if repo:
                existing_repos.add(repo)
        total_new += len(discovered)

    if args.dry_run:
        print(json.dumps(by_track_new, ensure_ascii=False, indent=2))
        return 0

    updated = benchmarks
    for track in ("vlm", "vla", "wm"):
        updated = insert_entries(updated, track, by_track_new[track])

    if total_new == 0:
        print("[ok] no new benchmark entries discovered")
        return 0

    bench_data["benchmarks"] = updated
    BENCHMARKS_PATH.write_text(
        yaml.safe_dump(bench_data, sort_keys=False, allow_unicode=True, width=120),
        encoding="utf-8",
    )
    print(f"[ok] appended {total_new} new benchmark entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
