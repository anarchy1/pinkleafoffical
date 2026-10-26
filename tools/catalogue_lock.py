#!/usr/bin/env python3
"""The catalogue lock. Kat's plant names, photos and prices, frozen.

    python3 tools/catalogue_lock.py check            exit 1 if the store drifted
    python3 tools/catalogue_lock.py approve PV119    re-lock one card, with Kat's yes
    python3 tools/catalogue_lock.py approve all      re-lock everything, with Kat's yes

Why this exists: on 25 and 26 Oct 2026 the store carried card names a session
had invented and two of Kat's own photos swapped between ids, and nobody
noticed for months because nothing compared the store to what Kat actually
labelled. The lock file (docs/catalogue-lock.json) records, per store card,
the id, the name, the md5 of the photo file and the prices. `check` fails the
health check (and therefore tools/deploy.sh) whenever any of those differ.

A session is never allowed to run `approve` on its own. Only after Kat has
said, in her own words, that a specific card should change. Put her words in
the commit message.
"""
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCK = ROOT / "docs" / "catalogue-lock.json"
sys.path.insert(0, str(ROOT / "tools"))
from build_product_schema import parse_store  # noqa: E402


def md5(path):
    p = ROOT / path
    if not p.exists():
        return None
    return hashlib.md5(p.read_bytes()).hexdigest()[:10]


def current():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    items, prices = parse_store(html)
    out = {}
    for it in items:
        pid = it["id"]
        out[pid] = {
            "id": pid,
            "name": it["name"],
            "status": it["status"],
            "image": f"plants/{pid}.jpg",
            "md5": md5(f"plants/{pid}.jpg"),
            "prices": {g: prices[f"{pid}_{g}"] for g in it["grades"] if f"{pid}_{g}" in prices},
        }
    return out


def load_lock():
    if not LOCK.exists():
        return {}
    return {e["id"]: e for e in json.loads(LOCK.read_text(encoding="utf-8"))}


def save_lock(d):
    LOCK.write_text(json.dumps(sorted(d.values(), key=lambda e: e["name"]),
                               ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def check():
    lock, now = load_lock(), current()
    if not lock:
        print("no lock file; run: python3 tools/catalogue_lock.py approve all")
        return 1
    problems = []
    for pid, L in lock.items():
        N = now.get(pid)
        if N is None:
            problems.append(f"{pid} {L['name']}: card REMOVED from the store")
            continue
        if N["name"] != L["name"]:
            problems.append(f"{pid}: name changed  {L['name']!r} -> {N['name']!r}")
        if N["md5"] != L["md5"]:
            problems.append(f"{pid} {L['name']}: photo changed (plants/{pid}.jpg md5 {L['md5']} -> {N['md5']})")
        if N["prices"] != L["prices"]:
            problems.append(f"{pid} {L['name']}: prices changed  {L['prices']} -> {N['prices']}")
        if N["status"] != L["status"] and N["status"] in ("sold", "soldout", "sold_out"):
            problems.append(f"{pid} {L['name']}: marked {N['status']} (Kat confirms sales, nobody else)")
    for pid, N in now.items():
        if pid not in lock:
            problems.append(f"{pid} {N['name']!r}: NEW card not in the lock")
    if problems:
        print("CATALOGUE LOCK FAILED. The store no longer matches Kat's labels:")
        for p in problems:
            print("  " + p)
        print("\nIf Kat asked for this change in her own words: "
              "python3 tools/catalogue_lock.py approve <PVid>   (or: approve all)")
        return 1
    print(f"catalogue lock: {len(lock)} cards match Kat's names, photos and prices")
    return 0


def approve(what):
    lock, now = load_lock(), current()
    if what == "all":
        lock = now
    else:
        ids = [w.strip() for w in what.split(",")]
        for pid in ids:
            if pid in now:
                lock[pid] = now[pid]
            elif pid in lock:
                del lock[pid]
            else:
                print(f"{pid}: not in store or lock"); return 1
    save_lock(lock)
    print(f"locked {what} ({len(lock)} cards). Put Kat's words in the commit message.")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["check"]:
        sys.exit(check())
    if a[:1] == ["approve"] and len(a) == 2:
        sys.exit(approve(a[1]))
    print(__doc__); sys.exit(2)
