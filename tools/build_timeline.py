#!/usr/bin/env python3
"""Generate wiki/timeline.md — the wiki viewed by date (what was added/changed each day).

Reads git history scoped to wiki/, rolls file changes up per calendar day, and writes a
reverse-chronological digest distinguishing pages CREATED (+) from UPDATED (~), with each
day's commit subjects as a one-line summary. Uncommitted working-tree changes are folded
into today's bucket so a mid-session run reflects in-progress work. Page titles/types come
from each file's YAML frontmatter. A third navigation surface alongside index.md (by topic)
and log.md (by operation) — see CLAUDE.md section 7.

Usage:
  python tools/build_timeline.py                       # repo = ., out = wiki/timeline.md
  python tools/build_timeline.py --repo . --out wiki/timeline.md

Generated file — do not edit by hand; rerun this script. Console output is forced to UTF-8
(this machine's console codepage is cp949); the .md is written UTF-8 and never ASCII-stripped.
"""
import re
import sys
import argparse
import subprocess
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKIP = {"timeline.md"}                       # never list the generated file itself
HOUSEKEEPING = {"index.md", "log.md"}        # shown as a per-day footnote, not as knowledge
FM_TYPE = re.compile(r"^type:\s*(.+)$", re.MULTILINE)
FM_TITLE = re.compile(r"^title:\s*(.+)$", re.MULTILINE)
_RANK = {"A": 3, "D": 2, "M": 1}             # within one day: created > removed > updated


def _git(repo: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or f"git {' '.join(args)} failed")
    return out.stdout


def _bump(files: dict, path: str, status: str) -> None:
    if path not in files or _RANK[status] > _RANK[files[path]]:
        files[path] = status


def _wanted(path: str) -> bool:
    return path.startswith("wiki/") and path.endswith(".md") and Path(path).name not in SKIP


def collect(repo: Path) -> dict:
    """{date: {"subjects": [...], "files": {path: A|M|D}}} from git history, scoped to wiki/."""
    days: dict = {}
    log = _git(
        repo, "log", "--no-merges", "--date=short",
        "--pretty=format:__C__\t%ad\t%s", "--name-status", "--", "wiki",
    )
    cur = None
    for line in log.splitlines():
        if line.startswith("__C__"):
            _, d, subj = line.split("\t", 2)
            cur = days.setdefault(d, {"subjects": [], "files": {}})
            if subj and subj not in cur["subjects"]:
                cur["subjects"].append(subj)
        elif line and cur is not None and line[0] in "AMDRC":
            parts = line.split("\t")
            code = parts[0][0]
            path, status = (parts[-1], "M") if code in ("R", "C") else (parts[1], code)
            if _wanted(path):
                _bump(cur["files"], path, status)
    return days


def merge_worktree(repo: Path, days: dict) -> None:
    """Fold uncommitted wiki/ changes into today's bucket so in-progress work shows."""
    today = date.today().isoformat()
    bucket = None
    for line in _git(repo, "status", "--porcelain", "--", "wiki").splitlines():
        if not line.strip():
            continue
        xy, path = line[:2], line[3:].strip()
        if " -> " in path:                       # rename: keep the new path
            path = path.split(" -> ", 1)[1]
        if not _wanted(path):
            continue
        status = "A" if ("?" in xy or "A" in xy) else "D" if "D" in xy else "M"
        if bucket is None:
            bucket = days.setdefault(today, {"subjects": [], "files": {}})
        _bump(bucket["files"], path, status)


def page_meta(repo: Path, path: str) -> tuple:
    """(title, type) from frontmatter; (stem, '') if unreadable/missing."""
    try:
        text = (repo / path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return Path(path).stem, ""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    block = m.group(1) if m else ""
    tm, ty = FM_TITLE.search(block), FM_TYPE.search(block)
    title = tm.group(1).strip().strip('"').strip("'") if tm else Path(path).stem
    return title, (ty.group(1).strip() if ty else "")


def _entry(mark: str, repo: Path, path: str) -> str:
    title, typ = page_meta(repo, path)
    rel = path[len("wiki/"):]                    # link relative to wiki/ (where timeline.md lives)
    label = f"[{title}]({rel})" if (repo / path).exists() else title
    return f"- **{mark}** {label}" + (f" · {typ}" if typ else "")


def render(repo: Path, days: dict) -> tuple:
    out = [
        "---",
        "type: timeline",
        "title: Timeline — Work by Day",
        "description: Auto-generated reverse-chronological digest of the knowledge added/changed each day.",
        f"timestamp: {date.today().isoformat()}T00:00:00Z",
        "---",
        "",
        "# Timeline — work by day",
        "",
        "> Auto-generated by `tools/build_timeline.py` from git history. **Do not edit by hand — rerun the",
        "> script.** `+` = page created · `~` = page updated. See also [by operation](log.md) and",
        "> [by topic](index.md).",
        "",
    ]
    entries = 0
    for d in sorted(days, reverse=True):
        files = days[d]["files"]
        created = sorted(p for p, s in files.items() if s == "A" and Path(p).name not in HOUSEKEEPING)
        updated = sorted(p for p, s in files.items() if s == "M" and Path(p).name not in HOUSEKEEPING)
        removed = sorted(p for p, s in files.items() if s == "D" and Path(p).name not in HOUSEKEEPING)
        names = {Path(p).name for p in files}
        hk = []
        if "index.md" in names:
            hk.append("indexes")
        if "log.md" in names:
            hk.append("log")
        counts = []
        if created:
            counts.append(f"+{len(created)} new")
        if updated:
            counts.append(f"~{len(updated)} updated")
        if removed:
            counts.append(f"-{len(removed)} removed")
        head = f"## {d}"
        if counts:
            head += "  ·  " + ", ".join(counts)
        elif hk:
            head += "  ·  housekeeping"
        out.append(head)
        if days[d]["subjects"]:
            out.append(f"_{'; '.join(days[d]['subjects'])}_")
        for p in created:
            out.append(_entry("+", repo, p))
            entries += 1
        for p in updated:
            out.append(_entry("~", repo, p))
            entries += 1
        for p in removed:
            out.append(f"- **✗** {Path(p).stem} (removed)")
        if hk:
            out.append(f"- _housekeeping: {', '.join(hk)}_")
        out.append("")
    return "\n".join(out).rstrip() + "\n", entries


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate wiki/timeline.md (the wiki by date) from git history.")
    ap.add_argument("--repo", default=".", help="repo root (default .)")
    ap.add_argument("--out", default="wiki/timeline.md", help="output path (default wiki/timeline.md)")
    a = ap.parse_args()
    repo = Path(a.repo)
    try:
        days = collect(repo)
        merge_worktree(repo, days)
    except (RuntimeError, FileNotFoundError) as e:
        print(f"error: {e}")
        sys.exit(1)
    text, entries = render(repo, days)
    (repo / a.out).write_text(text, encoding="utf-8")
    print(f"Wrote {a.out} — {len(days)} days, {entries} page entries")


if __name__ == "__main__":
    main()
