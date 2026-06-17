#!/usr/bin/env python3
"""Auto-discover benchmark entries for VLM/VLA/WM and append to benchmarks.yaml.

Design goal: stop guessing fields from raw README text. Instead, anchor on
structured, authoritative sources and (optionally) an LLM for the few prose
fields that need natural-language understanding.

Pipeline per candidate GitHub repo:
  1. Hard guards: must have a paper link (arXiv), pass star threshold,
     and NOT look like a survey / awesome-list / paper-collection repo.
  2. arXiv API  -> canonical paper title (the benchmark name), year, abstract.
     This replaces the old "grab the first README heading" heuristic that
     produced names like "Clone repository".
  3. Classification + prose fields:
       - If an OpenAI-compatible LLM is configured (env LLM_API_KEY), ask it to
         decide is_benchmark and to write a concise "what it tests" + metric in
         English and Chinese, grounded in the title + abstract.
       - Otherwise fall back to deterministic rules: require a benchmark signal
         in title/abstract and use the abstract's first sentence as the summary.
  4. Optional influence gate via Semantic Scholar citation count
     (only enabled when env S2_API_KEY is set; otherwise skipped).

Writing is APPEND-ONLY: new entries are appended as text to benchmarks.yaml so
the human-curated header comments and existing formatting are preserved. Order
within the file does not matter -- render_readme.py groups entries by track.

This script only edits data/benchmarks.yaml.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
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
ARXIV_API = "https://export.arxiv.org/api/query?id_list={arxiv_id}"
S2_API = "https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=citationCount"

ARXIV_ID_RE = re.compile(r"arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5})(?:v[0-9]+)?", re.IGNORECASE)


# --------------------------------------------------------------------------- #
# HTTP helpers (stdlib only; honors http(s)_proxy env vars)
# --------------------------------------------------------------------------- #
def gh_headers(raw: bool = False) -> dict:
    headers = {"Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json"}
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


def http_post_json(url: str, payload: dict, headers: dict, timeout: int = 60) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


# --------------------------------------------------------------------------- #
# Text utilities
# --------------------------------------------------------------------------- #
def normalize_text(*parts: str) -> str:
    return " ".join((p or "").lower() for p in parts)


def first_sentence(text: str, limit: int = 240) -> str:
    text = " ".join((text or "").split())
    if not text:
        return ""
    m = re.search(r"(.+?[.!?])\s", text + " ")
    sentence = m.group(1) if m else text
    return sentence[:limit].strip()


def extract_arxiv_id(*texts: str) -> str | None:
    for text in texts:
        if not text:
            continue
        m = ARXIV_ID_RE.search(text)
        if m:
            return m.group(1)
    return None


def looks_like_survey(text: str, blocklist_terms: list[str]) -> bool:
    return any(term in text for term in blocklist_terms)


def clean_benchmark_name(title: str) -> str:
    """Derive a concise benchmark name from a paper title.

    Many benchmark papers are titled "NAME: long subtitle". Prefer the short
    left-hand side when it looks like a proper name; otherwise keep the title.
    """
    title = " ".join((title or "").split())
    if not title:
        return ""
    if ":" in title:
        head = title.split(":", 1)[0].strip()
        # A real benchmark name is usually short and not a full sentence.
        if 2 <= len(head) <= 40 and len(head.split()) <= 6:
            return head
    return title[:80].strip()


def stable_name_from_assess(assess_name: str | None, arxiv_title: str) -> str:
    """Stabilize LLM naming with deterministic fallback rules.

    Rule order:
    1) If the paper title is "X: ...", use exactly X.
    2) Otherwise, allow the LLM name only when it appears in the title text.
    3) If uncertain, fall back to clean_benchmark_name(arxiv_title).
    """
    title = " ".join((arxiv_title or "").split())
    fallback = clean_benchmark_name(title)
    candidate = " ".join((assess_name or "").split()).strip()
    if not candidate:
        return fallback

    # For "X: ..." titles, keep exactly X to avoid ad-hoc aliases.
    if ":" in title:
        return candidate if candidate == fallback else fallback

    # For non-colon titles, only keep names that are explicitly present.
    if candidate == title or candidate.lower() in title.lower():
        return candidate
    return fallback


# --------------------------------------------------------------------------- #
# Structured sources
# --------------------------------------------------------------------------- #
def fetch_arxiv_meta(arxiv_id: str) -> dict | None:
    """Return {'title', 'year', 'abstract'} from the arXiv API, or None."""
    try:
        raw = http_text(ARXIV_API.format(arxiv_id=arxiv_id), timeout=20)
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] arxiv fetch failed for {arxiv_id}: {exc}", file=sys.stderr)
        return None

    def grab(tag: str) -> str | None:
        m = re.search(rf"<entry>.*?<{tag}>(.*?)</{tag}>", raw, re.DOTALL)
        return " ".join(html.unescape(m.group(1)).split()) if m else None

    title = grab("title")
    if not title:
        return None
    published = grab("published") or ""
    return {
        "title": title,
        "year": published[:4] if published[:4].isdigit() else "",
        "abstract": grab("summary") or "",
    }


def fetch_citations(arxiv_id: str) -> int | None:
    """Citation count via Semantic Scholar; only when S2_API_KEY is set."""
    key = os.environ.get("S2_API_KEY")
    if not key:
        return None
    try:
        data = http_json(S2_API.format(arxiv_id=arxiv_id), headers={"x-api-key": key}, timeout=20)
        return int(data.get("citationCount", 0))
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] semantic-scholar failed for {arxiv_id}: {exc}", file=sys.stderr)
        return None


# --------------------------------------------------------------------------- #
# Classification + prose fields
# --------------------------------------------------------------------------- #
def _resolve_llm() -> dict | None:
    """Resolve LLM provider config from env vars.

    Accepts either Anthropic-style vars (ANTHROPIC_AUTH_TOKEN / ANTHROPIC_API_KEY,
    ANTHROPIC_BASE_URL, ANTHROPIC_MODEL) or OpenAI-style vars (LLM_API_KEY,
    LLM_API_BASE, LLM_MODEL).

    The actual protocol is chosen by the base URL host, NOT by the variable
    names: only api.anthropic.com (or any *anthropic* host) uses the Anthropic
    Messages API; every other host (e.g. OpenAI-compatible proxies such as
    chatanywhere) uses the OpenAI chat-completions format. This lets users keep
    ANTHROPIC_* names while pointing at an OpenAI-compatible gateway.
    """
    a_token = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY")
    if a_token:
        base = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/")
        model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
        use_bearer = bool(os.environ.get("ANTHROPIC_AUTH_TOKEN"))
    else:
        key = os.environ.get("LLM_API_KEY")
        if not key:
            return None
        a_token = key
        base = os.environ.get("LLM_API_BASE", "https://api.openai.com/v1").rstrip("/")
        model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
        use_bearer = True

    host = urllib.parse.urlparse(base).netloc.lower()
    protocol = "anthropic" if "anthropic" in host else "openai"
    return {"protocol": protocol, "base": base, "token": a_token, "model": model, "use_bearer": use_bearer}


def llm_enabled() -> bool:
    return _resolve_llm() is not None


def _build_prompt(track: str, title: str, abstract: str) -> tuple[str, str]:
    track_desc = {
        "vlm": "embodied vision-language model evaluation (spatial reasoning, embodied planning, physical reasoning, embodied QA)",
        "vla": "vision-language-action / robot manipulation/control policy evaluation",
        "wm": "world model / video-generation-for-embodied evaluation",
    }.get(track, track)

    system = (
        "You curate an awesome-list of EMBODIED AI evaluation benchmarks. "
        "Given a paper title and abstract, decide whether it introduces a concrete "
        "EVALUATION BENCHMARK (with tasks + metrics), and summarize it. "
        "Reject surveys, awesome-lists, datasets-without-protocol, and methods/models "
        "that are not benchmarks. Respond with STRICT JSON only."
    )
    subcategory_hint = {
        "vlm": (
            '  "vlm_category": one of spatial | planning | qa | physical | reasoning,\n'
        ),
        "vla": (
            '  "vla_env": one of simulation | sim2real | real,\n'
            '  "vla_category": for simulation, one of core | robustness | memory | long_horizon | task_generalist,\n'
        ),
        "wm": (
            '  "wm_category": one of perceptual | generation | interactive | embodied_utility | physical,\n'
        ),
    }.get(track, "")

    user = (
        f"Track: {track} ({track_desc}).\n"
        f"Title: {title}\n"
        f"Abstract: {abstract[:1800]}\n\n"
        "Return JSON with keys:\n"
        '  "is_benchmark": boolean,\n'
        '  "name": benchmark name (string),\n'
        + subcategory_hint
        + '  "tests_en": one concise sentence on what it evaluates (English),\n'
        '  "tests_cn": same in Simplified Chinese,\n'
        '  "metric_en": main metric(s) (English, short),\n'
        '  "metric_cn": main metric(s) in Simplified Chinese.\n'
        "\n"
        'Naming rule for "name" (must follow):\n'
        "1) If title matches 'X: ...', set name to exactly X (keep original casing).\n"
        "2) Otherwise set name to the full paper title (do not shorten).\n"
        "3) NEVER invent a new alias/acronym not explicitly present in the title.\n"
        "4) If uncertain, keep the full title.\n"
        "If not a benchmark, set is_benchmark=false and leave other fields empty.\n"
        "Return ONLY the JSON object, with no prose and no code fences."
    )
    return system, user


def _join_url(base: str, suffix_with_v1: str) -> str:
    """Join base with an endpoint, avoiding a duplicate /v1 segment.

    `suffix_with_v1` looks like "/v1/messages" or "/v1/chat/completions".
    """
    base = base.rstrip("/")
    after_v1 = suffix_with_v1[len("/v1"):]  # "/messages" | "/chat/completions"
    if base.endswith(after_v1):
        return base
    if base.endswith("/v1"):
        return base + after_v1
    return base + suffix_with_v1


def _call_anthropic(cfg: dict, system: str, user: str) -> str:
    headers = {"Content-Type": "application/json", "anthropic-version": "2023-06-01"}
    if cfg["use_bearer"]:
        headers["Authorization"] = f"Bearer {cfg['token']}"
    else:
        headers["x-api-key"] = cfg["token"]
    payload = {
        "model": cfg["model"],
        "max_tokens": 1024,
        "temperature": 0,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    resp = http_post_json(_join_url(cfg["base"], "/v1/messages"), payload, headers, timeout=60)
    return "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")


def _call_openai(cfg: dict, system: str, user: str) -> str:
    headers = {"Authorization": f"Bearer {cfg['token']}", "Content-Type": "application/json"}
    payload = {
        "model": cfg["model"],
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0,
    }
    resp = http_post_json(_join_url(cfg["base"], "/v1/chat/completions"), payload, headers, timeout=60)
    return resp["choices"][0]["message"]["content"]


def llm_assess(track: str, title: str, abstract: str) -> dict | None:
    """Classify and summarize a candidate via the configured LLM.

    Returns a dict with keys: is_benchmark(bool), name, tests_en, tests_cn,
    metric_en, metric_cn -- or None on failure.
    """
    cfg = _resolve_llm()
    if cfg is None:
        return None
    system, user = _build_prompt(track, title, abstract)
    try:
        raw = _call_anthropic(cfg, system, user) if cfg["protocol"] == "anthropic" else _call_openai(cfg, system, user)
        content = re.sub(r"^```(?:json)?|```$", "", (raw or "").strip(), flags=re.MULTILINE).strip()
        # Be tolerant of leading/trailing prose around the JSON object.
        m = re.search(r"\{.*\}", content, re.DOTALL)
        return json.loads(m.group(0) if m else content)
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] LLM assess failed for '{title[:60]}': {exc}", file=sys.stderr)
        return None


def rule_based_assess(global_cfg: dict, title: str, abstract: str) -> dict:
    """Deterministic fallback when no LLM is configured."""
    benchmark_terms = global_cfg.get("benchmark_terms", [])
    text = normalize_text(title, abstract)
    is_benchmark = any(term in text for term in benchmark_terms)
    summary = first_sentence(abstract)
    return {
        "is_benchmark": is_benchmark,
        "name": "",  # caller falls back to arXiv-derived name
        "tests_en": summary or "See the paper and official repository for the evaluation protocol.",
        "tests_cn": "请参考论文与官方仓库中的评测任务与协议定义。",
        "metric_en": "Task-specific metrics (see official protocol)",
        "metric_cn": "任务定义指标（见官方协议）",
    }


# --------------------------------------------------------------------------- #
# Candidate scoring + entry construction
# --------------------------------------------------------------------------- #
def passes_track_relevance(track_cfg: dict, text: str) -> bool:
    track_terms = track_cfg.get("track_terms", [])
    min_track_hits = int(track_cfg.get("min_track_hits", 2))
    return sum(1 for term in track_terms if term in text) >= min_track_hits


def build_entry(track: str, track_cfg: dict, repo_item: dict, arxiv_id: str,
                arxiv_meta: dict, assess: dict) -> dict:
    repo_full = repo_item["full_name"]
    raw_name = (assess.get("name") or "").strip()
    name = stable_name_from_assess(raw_name, arxiv_meta["title"])
    if raw_name and name != raw_name:
        print(f"[warn] unstable-name fallback for {repo_full}: '{raw_name}' -> '{name}'", file=sys.stderr)
    year = arxiv_meta.get("year") or (repo_item.get("created_at", "1970")[:4])

    site = (repo_item.get("homepage") or "").strip()
    if site and "github.com" in site:
        site = ""

    links = [
        {"en": "Paper", "cn": "论文", "url": f"https://arxiv.org/abs/{arxiv_id}"},
        {"en": "Code", "cn": "代码", "url": repo_item["html_url"]},
    ]
    if site:
        links.append({"en": "Site", "cn": "主页", "url": site})

    entry = {
        "name": name,
        "track": track,
        "year_en": year,
        "year_cn": year,
        "tests_en": assess.get("tests_en") or "",
        "tests_cn": assess.get("tests_cn") or "",
        "metric_en": assess.get("metric_en") or "Task-specific metrics (see official protocol)",
        "metric_cn": assess.get("metric_cn") or "任务定义指标（见官方协议）",
        "repo": repo_full,
        "links": links,
    }
    for k, v in (track_cfg.get("extra_fields") or {}).items():
        entry[k] = v
    for key in ("vlm_category", "vla_env", "wm_category", "vlm_group"):
        if assess.get(key):
            entry[key] = assess[key]
    return entry


def discover_for_track(track: str, cfg: dict, existing_repos: set[str], existing_names: set[str]) -> list[dict]:
    global_cfg = cfg["automation"]
    track_cfg = global_cfg["tracks"][track]
    blocked = set(global_cfg.get("blocked_repos", []))
    survey_terms = [t.lower() for t in global_cfg.get("survey_blocklist_terms", [])]
    per_track_limit = int(global_cfg.get("per_track_limit", 2))
    per_query = int(global_cfg.get("search_per_query", 15))
    min_stars = int(track_cfg.get("min_stars", 0))
    min_citations = int(track_cfg.get("min_citations", 0))

    discovered: list[dict] = []
    seen_repos: set[str] = set()

    for query in track_cfg.get("queries", []):
        encoded = urllib.parse.quote_plus(query)
        try:
            payload = http_json(GITHUB_SEARCH_API.format(query=encoded, n=per_query), headers=gh_headers(), timeout=20)
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] search failed for track={track} query='{query}': {exc}", file=sys.stderr)
            continue

        for item in payload.get("items", []):
            repo = item.get("full_name")
            if not repo or repo in blocked or repo in existing_repos or repo in seen_repos:
                continue

            stars = int(item.get("stargazers_count", 0))
            if stars < min_stars:
                continue

            try:
                readme_text = http_text(GITHUB_README_API.format(repo=repo), headers=gh_headers(raw=True), timeout=15)
            except Exception:  # noqa: BLE001
                readme_text = ""

            combined = normalize_text(
                item.get("name", ""), item.get("description", ""),
                " ".join(item.get("topics", []) or []), readme_text,
            )

            # Hard negative guard: surveys / awesome-lists / paper collections.
            if looks_like_survey(normalize_text(item.get("name", ""), item.get("description", ""),
                                                " ".join(item.get("topics", []) or [])), survey_terms):
                print(f"[skip] {repo}: looks-like-survey/list", file=sys.stderr)
                continue

            if not passes_track_relevance(track_cfg, combined):
                continue

            arxiv_id = extract_arxiv_id(readme_text, item.get("homepage", "") or "")
            if not arxiv_id:
                print(f"[skip] {repo}: no-arxiv-link", file=sys.stderr)
                continue

            arxiv_meta = fetch_arxiv_meta(arxiv_id)
            if not arxiv_meta:
                print(f"[skip] {repo}: arxiv-meta-unavailable", file=sys.stderr)
                continue

            # Title-level survey guard (paper itself is a survey).
            if looks_like_survey(arxiv_meta["title"].lower(), survey_terms):
                print(f"[skip] {repo}: paper-is-survey", file=sys.stderr)
                continue

            if min_citations > 0:
                citations = fetch_citations(arxiv_id)
                if citations is not None and citations < min_citations:
                    print(f"[skip] {repo}: citations<{min_citations}", file=sys.stderr)
                    continue

            assess = llm_assess(track, arxiv_meta["title"], arxiv_meta["abstract"]) if llm_enabled() else None
            if assess is None:
                assess = rule_based_assess(global_cfg, arxiv_meta["title"], arxiv_meta["abstract"])

            if not assess.get("is_benchmark"):
                print(f"[skip] {repo}: not-a-benchmark", file=sys.stderr)
                continue

            entry = build_entry(track, track_cfg, item, arxiv_id, arxiv_meta, assess)
            if entry["name"].lower() in existing_names:
                print(f"[skip] {repo}: duplicate-name '{entry['name']}'", file=sys.stderr)
                continue

            discovered.append(entry)
            seen_repos.add(repo)
            existing_names.add(entry["name"].lower())
            print(f"[add] {track}: {repo} -> '{entry['name']}'")
            if len(discovered) >= per_track_limit:
                return discovered

    return discovered


# --------------------------------------------------------------------------- #
# Append-only YAML writing (preserves existing comments/formatting)
# --------------------------------------------------------------------------- #
def next_seq(benchmarks: list[dict], track: str) -> int:
    existing = [
        int(e["seq"])
        for e in benchmarks
        if e.get("track") == track and e.get("seq") is not None
    ]
    return max(existing, default=0) + 1


def assign_new_sequences(benchmarks: list[dict], new_entries: list[dict]) -> None:
    next_by_track = {track: next_seq(benchmarks, track) for track in ("vlm", "vla", "wm")}
    for entry in new_entries:
        track = entry["track"]
        entry["seq"] = next_by_track[track]
        next_by_track[track] += 1


def yaml_snippet(entries: list[dict]) -> str:
    dumped = yaml.safe_dump(entries, sort_keys=False, allow_unicode=True, width=120)
    # Indent list items by 2 spaces to match the existing `benchmarks:` block.
    return "".join(("  " + line if line.strip() else line) for line in dumped.splitlines(keepends=True))


def append_entries(new_entries: list[dict]) -> None:
    text = BENCHMARKS_PATH.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    today = dt.date.today().isoformat()
    block = f"\n  # ---------------- auto-discovered ({today}) ----------------\n"
    block += yaml_snippet(new_entries)
    BENCHMARKS_PATH.write_text(text + block, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print discoveries without writing benchmarks.yaml")
    args = parser.parse_args()

    bench_data = yaml.safe_load(BENCHMARKS_PATH.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    benchmarks: list[dict] = bench_data.get("benchmarks", [])

    if not cfg.get("automation", {}).get("enabled", True):
        print("[ok] auto-discovery disabled in config")
        return 0

    llm_cfg = _resolve_llm()
    if llm_cfg:
        host = urllib.parse.urlparse(llm_cfg["base"]).netloc
        print(f"[info] LLM provider: {llm_cfg['protocol']} (host={host}, model={llm_cfg['model']})")
    else:
        print("[info] LLM not configured -> rule-based assessment")

    existing_repos = {e.get("repo") for e in benchmarks if e.get("repo")}
    existing_names = {(e.get("name") or "").lower() for e in benchmarks}

    all_new: list[dict] = []
    for track in ("vlm", "vla", "wm"):
        discovered = discover_for_track(track, cfg, existing_repos, existing_names)
        for e in discovered:
            if e.get("repo"):
                existing_repos.add(e["repo"])
        all_new.extend(discovered)

    if args.dry_run:
        print(json.dumps(all_new, ensure_ascii=False, indent=2))
        return 0

    if not all_new:
        print("[ok] no new benchmark entries discovered")
        return 0

    assign_new_sequences(benchmarks, all_new)
    append_entries(all_new)
    print(f"[ok] appended {len(all_new)} new benchmark entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
