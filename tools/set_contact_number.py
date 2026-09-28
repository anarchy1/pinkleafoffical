#!/usr/bin/env python3
"""Repoint every customer contact on the site at a different phone number.

    python3 tools/set_contact_number.py --check
    python3 tools/set_contact_number.py 054-000-0000 --dry-run
    python3 tools/set_contact_number.py 054-000-0000

Why this exists: the studio's WhatsApp number is hard-coded in more than a
hundred places across index.html, every article, every encyclopedia page, the
404 page, the shared enhancements JS and the page builder. It is the target of
every "message us" link on the site and it is also the Bit payment phone. All
of it currently rings one handset. Moving the shop to a business line used to
mean 112 hand edits, which is how a few of them would get missed and a
customer would land on a dead link.

The current number is not stored here. It is read from index.html, so this
script cannot go stale, and running it twice in a row is a no-op.

Three written forms are kept in sync:

    wa.me/972559116990      the WhatsApp deep links
    +972-55-911-6990        schema.org telephone and visible text
    055-911-6990            the Bit payment phone

Nothing else changes. This does not deploy. After running it, the site still
has to go out from the Mac.
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUFFIXES = {".html", ".js", ".py"}
SKIP_DIRS = {".git", "node_modules", ".claude"}


def scan_dirs():
    for path in sorted(ROOT.rglob("*")):
        if path.suffix not in SUFFIXES or not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.resolve() == pathlib.Path(__file__).resolve():
            continue
        yield path


def current_number():
    """The number the site uses now, taken from the wa.me links in index.html."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    found = re.findall(r"wa\.me/(\d{11,15})", html)
    if not found:
        sys.exit("could not find a wa.me link in index.html")
    return max(set(found), key=found.count)


def normalise(raw):
    """Accept 0559116990, 055-911-6990, +972559116990 or 972559116990.

    Returns the international form with no punctuation.
    """
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("972"):
        digits = digits[3:]
    elif digits.startswith("0"):
        digits = digits[1:]
    if len(digits) != 9:
        sys.exit(
            f"'{raw}' is not an Israeli mobile number. "
            "Expected 9 digits after the leading 0, for example 054-792-0799."
        )
    return "972" + digits


def forms(intl):
    """The three written shapes of one number, in the order they are replaced."""
    rest = intl[3:]
    return {
        "intl_plain": intl,
        "intl_dashed": f"+972-{rest[0:2]}-{rest[2:5]}-{rest[5:9]}",
        "local_dashed": f"0{rest[0:2]}-{rest[2:5]}-{rest[5:9]}",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("number", nargs="?", help="the new number, in any common form")
    ap.add_argument("--check", action="store_true",
                    help="report where the current number appears and stop")
    ap.add_argument("--dry-run", action="store_true",
                    help="show what would change without writing")
    args = ap.parse_args()

    old = forms(current_number())

    if args.check or not args.number:
        total, files = 0, 0
        print(f"current number: {old['intl_dashed']}\n")
        for path in scan_dirs():
            text = path.read_text(encoding="utf-8", errors="ignore")
            n = sum(text.count(v) for v in old.values())
            if n:
                files += 1
                total += n
                print(f"  {n:>3}  {path.relative_to(ROOT)}")
        print(f"\n{total} references across {files} files")
        if not args.number:
            print("\nPass a new number to rewrite them all.")
        return 0

    new = forms(normalise(args.number))
    if new == old:
        print(f"already set to {new['intl_dashed']}, nothing to do")
        return 0

    changed, total = [], 0
    for path in scan_dirs():
        text = path.read_text(encoding="utf-8")
        updated = text
        for key in ("intl_plain", "intl_dashed", "local_dashed"):
            updated = updated.replace(old[key], new[key])
        if updated != text:
            n = sum(text.count(v) for v in old.values())
            total += n
            changed.append((path, n))
            if not args.dry_run:
                path.write_text(updated, encoding="utf-8")

    verb = "would change" if args.dry_run else "changed"
    print(f"{old['intl_dashed']}  ->  {new['intl_dashed']}\n")
    for path, n in changed:
        print(f"  {n:>3}  {path.relative_to(ROOT)}")
    print(f"\n{verb} {total} references across {len(changed)} files")
    if not args.dry_run:
        print("\nThis does not deploy. The site still has to go out from the Mac.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
