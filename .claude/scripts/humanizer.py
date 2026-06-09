#!/usr/bin/env python3
"""Humanizer: strip em dashes from text files.

Enforces the project's "never use em dashes" rule by rewriting any em dash
(U+2014) or horizontal bar (U+2015) to a plain hyphen. Spacing around the
character is preserved, so " — " becomes " - " and "word—word" becomes
"word-word".

Usage:
    humanizer.py <file> [<file> ...]

Safe by design:
- Skips paths that are not regular files.
- Skips binary files (anything containing a NUL byte, e.g. PNG/favicon).
- Only rewrites a file when its content actually changes.
- Exits 0 even on a skipped file so it never blocks a tool call.
"""

import sys
from pathlib import Path

# Characters that count as an em dash for our purposes.
EM_DASHES = {
    "—": "-",  # — em dash
    "―": "-",  # ― horizontal bar
}


def humanize(text: str) -> str:
    for bad, good in EM_DASHES.items():
        text = text.replace(bad, good)
    return text


def process(path: Path) -> bool:
    """Rewrite the file in place if it contains em dashes. Returns True if changed."""
    if not path.is_file():
        return False
    try:
        raw = path.read_bytes()
    except OSError:
        return False
    if b"\x00" in raw:  # binary file, leave it alone
        return False
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    cleaned = humanize(text)
    if cleaned == text:
        return False
    path.write_text(cleaned, encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    changed = 0
    for arg in argv:
        if process(Path(arg)):
            changed += 1
    if changed:
        print(f"humanizer: stripped em dashes from {changed} file(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
