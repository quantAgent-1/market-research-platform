#!/usr/bin/env python3
"""Lint relative markdown links across the wiki (OKF bundle integrity check).

Scans .md files under a root for [text](target) links, resolves relative targets
against each file's directory, and reports any whose target file does not exist.
External (http/https/mailto) and pure in-page (#anchor) links are ignored.

Usage:
  python tools/check_links.py [root]      # default root: current directory
"""
import re
import sys
from pathlib import Path

LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    broken: list[tuple[str, str]] = []
    total = 0
    for md in sorted(root.rglob("*.md")):
        if ".git" in md.parts:
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        # Ignore links inside fenced code blocks and inline code (doc examples/templates).
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        text = re.sub(r"`[^`]*`", "", text)
        for m in LINK.finditer(text):
            target = m.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = target.split("#", 1)[0]
            if not path:
                continue
            total += 1
            if not (md.parent / path).resolve().exists():
                broken.append((md.as_posix(), target))

    print(f"Checked {total} relative links under {root}/")
    if broken:
        print(f"BROKEN ({len(broken)}):")
        for src, tgt in broken:
            print(f"  {src} -> {tgt}")
        sys.exit(1)
    print("All relative links resolve. OK.")


if __name__ == "__main__":
    main()
