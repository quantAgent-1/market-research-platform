#!/usr/bin/env python3
"""Extract text / table-of-contents from a PDF for wiki ingestion.

Poppler (pdftoppm/pdftotext) is not required — this uses PyMuPDF (`fitz`).

Usage:
  python tools/pdf_extract.py <pdf> toc            # page count + embedded bookmarks
  python tools/pdf_extract.py <pdf> front          # text of the first 6 pages
  python tools/pdf_extract.py <pdf> text A B       # text of pages A..B (1-indexed, inclusive)
  python tools/pdf_extract.py <pdf> find "regex"   # pages whose text matches regex
"""
import re
import sys
import unicodedata

import fitz  # PyMuPDF

# Console here is cp949 (Korean code page); force lossless-ish ASCII so prints never crash.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_REPL = {
    "ﬁ": "fi", "ﬂ": "fl", "‘": "'", "’": "'",
    "“": '"', "”": '"', "–": "-", "—": "--",
    "…": "...", "\xa0": " ", "\xa9": "(c)", "−": "-",
}


def clean(s: str) -> str:
    for k, v in _REPL.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFKD", s)
    return s.encode("ascii", "ignore").decode("ascii")


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        return
    path, cmd = sys.argv[1], sys.argv[2]
    doc = fitz.open(path)
    n = doc.page_count

    if cmd == "toc":
        print(f"PAGES: {n}")
        toc = doc.get_toc()
        if not toc:
            print("(no embedded TOC/bookmarks)")
        for lvl, title, page in toc:
            print(f"{'  ' * (lvl - 1)}{page:>5}  {clean(title)}")

    elif cmd == "front":
        for i in range(min(6, n)):
            t = doc[i].get_text().strip()
            if t:
                print(f"--- p{i + 1} ---\n{clean(t)[:1800]}\n")

    elif cmd == "text":
        a = max(1, int(sys.argv[3]))
        b = min(n, int(sys.argv[4]))
        for i in range(a - 1, b):
            print(f"--- p{i + 1} ---\n{clean(doc[i].get_text().strip())}\n")

    elif cmd == "find":
        pat = re.compile(sys.argv[3], re.IGNORECASE)
        for i in range(n):
            if pat.search(doc[i].get_text()):
                print(f"p{i + 1}")

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
