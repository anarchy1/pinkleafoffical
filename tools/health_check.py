#!/usr/bin/env python3
"""The site health check, as one command. Run from the repo root:

    python3 tools/health_check.py

This is the eight point check described in CLAUDE.md. It existed as ad hoc
shell and python typed fresh each time, which drifted: it produced two false
alarms in four runs (flagging the word "deflasked" in public teaching
articles, and counting a comment as a config flag). A check that cries wolf
gets ignored, and then it is worse than no check.

Point 8 lives in tools/smoke_test.py because it needs a browser. This runs it
and folds in the result.

Exit code 0 means everything passed, 1 means something needs attention.
"""
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)

# Folders that are meant to be served. Everything else must be 404d.
# Do not add to this without opening the folder: src/ was waved through once
# on the strength of its name and turned out to be dead marketing drafts.
PUBLIC_DIRS = {"plants", "assets", "articles", "encyclopedia", "stickers"}

problems = []
passes = []


def ok(msg):
    passes.append(msg)


def bad(msg):
    problems.append(msg)


def strip_comments(text):
    """Config comments are not config. Counting them caused a false alarm."""
    return "\n".join(l for l in text.splitlines() if not l.strip().startswith("#"))


def sh(*args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def main():
    html = pathlib.Path("index.html").read_text(encoding="utf-8")

    # 1. Branch drift
    subprocess.run(["git", "fetch", "-q", "origin", "main"], capture_output=True)
    behind = len(sh("git", "log", "--oneline", "HEAD..origin/main").split("\n")) - 1
    ahead = len(sh("git", "log", "--oneline", "origin/main..HEAD").split("\n")) - 1
    (bad if behind else ok)(f"1 drift: {behind} behind main, {ahead} ahead")

    # 2. Schema against store
    pm = re.search(r"const ITEM_PRICES = \{(.*?)\n        \};", html, re.S)
    prices = dict(re.findall(r'"([^"]+)"\s*:\s*(\d+)', pm.group(1)))
    mismatch = checked = 0
    for blk in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S):
        for node in json.loads(blk).get("@graph", []):
            if "#product-" not in node.get("@id", ""):
                continue
            pid = node["@id"].split("#product-")[-1]
            offers = node.get("offers") or []
            if isinstance(offers, dict):
                offers = [offers]
            for o in offers:
                checked += 1
                name = o.get("name")
                key = f"{pid}_{name}" if name else None
                cands = [k for k in prices if k.startswith(pid + "_")]
                if key and key in prices:
                    expect = int(prices[key])
                elif len(cands) == 1:
                    expect = int(prices[cands[0]])
                else:
                    continue
                if int(o["price"]) != expect:
                    mismatch += 1
    (bad if mismatch else ok)(
        f"2 schema: {checked} offers, {mismatch} disagree with the store"
        + ("  run tools/build_product_schema.py" if mismatch else "")
    )

    # 3. Store data integrity
    m = re.search(r"const ALL_STORE_ITEMS = \[(.*?)\n        \];", html, re.S)
    items = []
    for line in m.group(1).splitlines():
        i = re.search(r'id:\s*"([^"]+)"', line)
        if not i:
            continue
        av = re.search(r"availability:\s*\[([^\]]*)\]", line)
        st = re.search(r'status:\s*"([^"]+)"', line)
        items.append((i.group(1),
                      re.findall(r'"([^"]+)"', av.group(1)) if av else [],
                      st.group(1) if st else ""))
    valid = {f"{i}_{o}" for i, a, _ in items for o in a}
    unpriced = [f"{i}_{o}" for i, a, st in items if st != "coming"
                for o in a if f"{i}_{o}" not in prices]
    orphans = [k for k in prices if k not in valid]
    dupes = [k for k, v in Counter(i for i, _, _ in items).items() if v > 1]
    trouble = unpriced or orphans or dupes
    (bad if trouble else ok)(
        f"3 store data: {len(items)} items, {len(unpriced)} unpriced, "
        f"{len(orphans)} orphan prices, {len(dupes)} duplicate ids"
    )

    # 4. Private data. Match the assignment shape, never a bare word: the word
    # deflasked is legitimate in an article teaching what deflasking is.
    leak = sh("grep", "-rnE", r'(acclimation|stage)\s*:\s*"|"in-transit"|"customs"',
              "--include=*.html", ".")
    (bad if leak.strip() else ok)(
        "4 private data: " + ("CLEAN" if not leak.strip() else leak.strip()[:200])
    )

    # 5. It still parses
    broken = 0
    for f in ["index.html", "stickers/index.html"]:
        t = pathlib.Path(f).read_text(encoding="utf-8")
        for b in re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", t, re.S):
            if "application/ld+json" in b[:80] or '"@context"' in b[:200]:
                try:
                    json.loads(b)
                except Exception:
                    broken += 1
                continue
            tf = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
            tf.write(b)
            tf.close()
            if subprocess.run(["node", "--check", tf.name], capture_output=True).returncode:
                broken += 1
            os.unlink(tf.name)
    (bad if broken else ok)(f"5 parses: {broken} broken script blocks")

    # 6. Switches wired but empty
    empties = [v for v in ("STOCK_SHEET_CSV", "INVOICE4U_PAY_URL")
               if re.search(v + r"\s*=\s*''", html)]
    ok(f"6 unbuilt switches: {', '.join(empties) if empties else 'none'}"
       + ("  (feature reads as done and does nothing)" if empties else ""))

    # 7. Internal folders blocked, with force
    toml_raw = pathlib.Path("netlify.toml").read_text(encoding="utf-8")
    toml = strip_comments(toml_raw)
    dirs = [p.name for p in pathlib.Path(".").iterdir() if p.is_dir() and p.name != ".git"]
    unblocked = [d for d in dirs if d not in PUBLIC_DIRS and f'/{d}/*' not in toml]
    rules = toml.count("status = 404")
    forced = toml.count("force = true")
    issue = unblocked or rules != forced
    (bad if issue else ok)(
        f"7 folders: {len(unblocked)} unblocked {unblocked or ''}, "
        f"{rules} rules / {forced} forced"
        + ("  force=true missing, Netlify will serve the file anyway" if rules != forced else "")
    )

    # 8. Behaviour
    r = subprocess.run([sys.executable, "tools/smoke_test.py"], capture_output=True, text=True)
    (bad if r.returncode else ok)(
        "8 store works: " + ("all smoke checks passed" if not r.returncode
                             else "SMOKE TEST FAILED\n" + r.stdout)
    )

    print("\n  ".join(["PASS"] + passes))
    if problems:
        print("\n  ".join(["\nNEEDS ATTENTION"] + problems))
        return 1
    print("\nall clear")
    return 0


if __name__ == "__main__":
    sys.exit(main())
