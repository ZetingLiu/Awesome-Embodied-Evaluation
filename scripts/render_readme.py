#!/usr/bin/env python3
"""Render the benchmark tables in README.md / README_CN.md from benchmarks.yaml.

Single source of truth: data/benchmarks.yaml (human-curated).
Machine-managed columns (Stars / Updated) are fetched from the GitHub REST API
and injected only into the marked table blocks, e.g.:

    <!-- AEE-TABLE:VLM-PRIMARY-SPATIAL:START --> ... <!-- END -->
    <!-- AEE-TABLE:VLA-SIM-CORE:START --> ... <!-- END -->
    <!-- AEE-TABLE:WM-INTERACTIVE:START --> ... <!-- END -->

Everything outside the markers (prose, related lists, etc.) is left untouched.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = REPO_ROOT / "data" / "benchmarks.yaml"
CACHE_PATH = REPO_ROOT / "data" / ".cache" / "metadata.json"
README_EN = REPO_ROOT / "README.md"
README_CN = REPO_ROOT / "README_CN.md"

GITHUB_API = "https://api.github.com/repos/{repo}"
PLACEHOLDER = "—"

HEADERS = {
    "en": ["No.", "Benchmark", "Year", "What it tests", "Metric", "Stars", "Updated", "Links"],
    "cn": ["序号", "基准", "年份", "评什么", "指标", "Stars", "最近更新", "链接"],
}


def _vlm_primary(cat: str):
    return lambda e: (
        e.get("track") == "vlm"
        and e.get("vlm_group") == "primary"
        and e.get("vlm_category") == cat
    )


def _vlm_control(cat: str):
    return lambda e: (
        e.get("track") == "vlm"
        and e.get("vlm_group", "control") == "control"
        and e.get("vlm_category") == cat
    )


def _vla(env: str):
    return lambda e: e.get("track") == "vla" and e.get("vla_env") == env


def _vla_category(env: str, cat: str):
    return lambda e: (
        e.get("track") == "vla"
        and e.get("vla_env") == env
        and e.get("vla_category") == cat
    )


def _wm(cat: str):
    return lambda e: e.get("track") == "wm" and e.get("wm_category") == cat


# Marker specs: (marker_name, selector function)
MARKER_SPECS = [
    ("VLM-PRIMARY-SPATIAL", _vlm_primary("spatial")),
    ("VLM-PRIMARY-PLANNING", _vlm_primary("planning")),
    ("VLM-PRIMARY-QA", _vlm_primary("qa")),
    ("VLM-PRIMARY-PHYSICAL", _vlm_primary("physical")),
    ("VLM-PRIMARY-REASONING", _vlm_primary("reasoning")),
    ("VLM-CONTROL-REASONING", _vlm_control("reasoning")),
    ("VLM-CONTROL-PERCEPTION", _vlm_control("perception")),
    ("VLM-CONTROL-VIDEO", _vlm_control("video")),
    ("VLM-CONTROL-DOCUMENT", _vlm_control("document")),
    ("VLA-SIM-CORE", _vla_category("simulation", "core")),
    ("VLA-SIM-ROBUSTNESS", _vla_category("simulation", "robustness")),
    ("VLA-SIM-MEMORY", _vla_category("simulation", "memory")),
    ("VLA-SIM-LONG-HORIZON", _vla_category("simulation", "long_horizon")),
    ("VLA-SIM-GENERALIST", _vla_category("simulation", "task_generalist")),
    ("VLA-SIM2REAL", _vla("sim2real")),
    ("VLA-REAL", _vla("real")),
    ("WM-PERCEPTUAL", _wm("perceptual")),
    ("WM-GENERATION", _wm("generation")),
    ("WM-INTERACTIVE", _wm("interactive")),
    ("WM-EMBODIED", _wm("embodied_utility")),
    ("WM-PHYSICAL", _wm("physical")),
]


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
    req = urllib.request.Request(GITHUB_API.format(repo=repo), headers=gh_headers())
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        meta = {
            "stars": int(data.get("stargazers_count", 0)),
            "updated": (data.get("pushed_at") or "")[:7],
        }
        cache[repo] = meta
        return meta
    except urllib.error.HTTPError as exc:
        print(f"[warn] GitHub API {exc.code} for {repo}; using cache", file=sys.stderr)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
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


def global_ordered_entries(benchmarks: list[dict]) -> list[dict]:
    """Stable global order: MARKER_SPECS order, then YAML list order within each table."""
    ordered: list[dict] = []
    seen: set[int] = set()
    for _marker, selector in MARKER_SPECS:
        for entry in benchmarks:
            key = id(entry)
            if key in seen:
                continue
            if selector(entry):
                ordered.append(entry)
                seen.add(key)
    for entry in benchmarks:
        if id(entry) not in seen:
            print(
                f"[warn] entry not assigned to a marker: '{entry.get('name')}'",
                file=sys.stderr,
            )
    return ordered


def validate_sequences(benchmarks: list[dict]) -> None:
    seqs = [entry.get("seq") for entry in benchmarks]
    missing = [entry.get("name") for entry in benchmarks if entry.get("seq") is None]
    if missing:
        raise ValueError(
            "Missing seq for entries: "
            + ", ".join(str(name) for name in missing)
            + ". Run: python scripts/render_readme.py --assign-seq"
        )
    numeric = [int(s) for s in seqs]
    if len(set(numeric)) != len(numeric):
        raise ValueError("Duplicate seq values in benchmarks.yaml")
    if sorted(numeric) != list(range(1, len(numeric) + 1)):
        raise ValueError("seq must be a contiguous run starting at 1")


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
    seq = entry["seq"]
    cells = [str(seq), f"**{name}**", year, tests, metric, stars, updated, links]
    return "| " + " | ".join(cells) + " |"


def render_table(entries: list[dict], lang: str) -> str:
    if not entries:
        return "_No entries yet._" if lang == "en" else "_暂无条目。_"
    header = "| " + " | ".join(HEADERS[lang]) + " |"
    sep = "|" + "|".join(["---"] * len(HEADERS[lang])) + "|"
    rows = [render_row(e, lang) for e in sorted(entries, key=lambda e: int(e["seq"]))]
    return "\n".join([header, sep, *rows])


def replace_block(text: str, marker: str, body: str) -> str:
    start = f"<!-- AEE-TABLE:{marker}:START -->"
    end = f"<!-- AEE-TABLE:{marker}:END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        raise ValueError(f"Marker block AEE-TABLE:{marker} not found")
    replacement = f"{start}\n{body}\n{end}"
    return pattern.sub(lambda _m: replacement, text)


def render_readme(path: Path, entries_by_marker: dict, lang: str) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text = text
    for marker, _selector in MARKER_SPECS:
        table = render_table(entries_by_marker.get(marker, []), lang)
        new_text = replace_block(new_text, marker, table)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def assign_sequences() -> int:
    """Write contiguous seq: 1..N into benchmarks.yaml (preserves comments)."""
    try:
        from ruamel.yaml import YAML
    except ImportError:
        print("[error] ruamel.yaml is required for --assign-seq", file=sys.stderr)
        return 1

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 120
    yaml.indent(mapping=2, sequence=4, offset=2)
    data = yaml.load(YAML_PATH.read_text(encoding="utf-8"))
    benchmarks = data.get("benchmarks", [])
    for idx, entry in enumerate(global_ordered_entries(benchmarks), start=1):
        entry["seq"] = idx
    with YAML_PATH.open("w", encoding="utf-8") as fh:
        yaml.dump(data, fh)
    print(f"[ok] assigned seq 1..{len(benchmarks)} in {YAML_PATH.name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write; exit 1 if the rendered output differs from on-disk files.",
    )
    parser.add_argument(
        "--assign-seq",
        action="store_true",
        help="Assign contiguous seq: 1..N in benchmarks.yaml, then exit.",
    )
    args = parser.parse_args()

    if args.assign_seq:
        return assign_sequences()

    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    benchmarks = data.get("benchmarks", [])
    validate_sequences(benchmarks)

    cache = load_cache()
    for entry in benchmarks:
        repo = entry.get("repo")
        entry["_meta"] = fetch_repo_meta(repo, cache) if repo else None
    save_cache(cache)

    entries_by_marker: dict[str, list[dict]] = {marker: [] for marker, _ in MARKER_SPECS}
    for entry in benchmarks:
        for marker, selector in MARKER_SPECS:
            if selector(entry):
                entries_by_marker[marker].append(entry)
                break

    if args.check:
        changed = False
        for path, lang in [(README_EN, "en"), (README_CN, "cn")]:
            text = path.read_text(encoding="utf-8")
            new_text = text
            for marker, _selector in MARKER_SPECS:
                table = render_table(entries_by_marker.get(marker, []), lang)
                new_text = replace_block(new_text, marker, table)
            if new_text != text:
                print(f"[check] {path.name} would change")
                changed = True
        return 1 if changed else 0

    changed_files = []
    for path, lang in [(README_EN, "en"), (README_CN, "cn")]:
        if render_readme(path, entries_by_marker, lang):
            changed_files.append(path.name)

    if changed_files:
        print(f"[ok] updated: {', '.join(changed_files)}")
    else:
        print("[ok] no changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
