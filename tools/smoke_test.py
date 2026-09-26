#!/usr/bin/env python3
"""Behavioural smoke test for the store. Run from the repo root:

    python3 tools/smoke_test.py

Why this exists: on 26 September a merge resolution left the buy button on
the wrong branch of an if, so every available plant showed NOTIFY ME and
nothing on the site could be bought. The store was unbuyable in production.

Every check in place at the time passed. The scripts parsed, the schema
matched the store, no variable was undefined, no private data shipped. A
logic inversion in a conditional is invisible to all of that, because the
code is perfectly valid. It is just wrong.

So this loads the real page in a real browser and asserts on what a
customer would actually see. It is the only check here that can fail on
behaviour rather than on shape.

Exit code 0 means pass, 1 means fail.
"""
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

failures = []
notes = []


def check(name, ok, detail=""):
    (notes if ok else failures).append(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))


def main():
    index = ROOT / "index.html"
    html = index.read_text(encoding="utf-8")

    # How many plants should be buyable, straight from the store data.
    m = re.search(r"const ALL_STORE_ITEMS = \[(.*?)\n        \];", html, re.S)
    if not m:
        print("FAIL  could not find ALL_STORE_ITEMS")
        return 1
    available = sum(
        1 for line in m.group(1).splitlines()
        if re.search(r'id:\s*"', line) and 'status: "available"' in line
    )
    coming = sum(
        1 for line in m.group(1).splitlines()
        if re.search(r'id:\s*"', line) and 'status: "coming"' in line
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME)
        page = browser.new_page(viewport={"width": 1280, "height": 1000})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(index.as_uri())
        page.wait_for_timeout(1200)

        # Get into the store.
        page.evaluate("showPage('store')")
        page.wait_for_timeout(1200)

        counts = page.evaluate("""() => {
            const txt = [...document.querySelectorAll('.add-to-cart-btn')].map(b => b.textContent.trim());
            return {
                cards: document.querySelectorAll('.portal').length,
                addToBag: txt.filter(t => /ADD TO BAG/i.test(t)).length,
                waitlist: txt.filter(t => /NOTIFY ME|עדכנו אותי/.test(t)).length,
                buttons: txt.length,
            };
        }""")

        check("page throws no JS errors", not errors, "; ".join(errors[:2]))
        check("store renders plant cards", counts["cards"] > 0, f"{counts['cards']} cards")
        check("buy buttons exist at all", counts["buttons"] > 0, f"{counts['buttons']} buttons")

        # THE ONE THAT MATTERS. If this fails, nothing can be bought.
        check(
            "available plants offer ADD TO BAG",
            counts["addToBag"] > 0,
            f"{counts['addToBag']} of {available} available plants",
        )
        check(
            "ADD TO BAG is not wildly off the available count",
            counts["addToBag"] >= max(1, available // 2),
            f"{counts['addToBag']} shown vs {available} available in the data",
        )
        check(
            "coming-soon plants offer the waitlist",
            counts["waitlist"] > 0 if coming else True,
            f"{counts['waitlist']} waitlist buttons, {coming} coming",
        )
        check(
            "the two button types are not swapped",
            counts["addToBag"] > counts["waitlist"],
            f"{counts['addToBag']} buy vs {counts['waitlist']} waitlist; "
            f"data says {available} available vs {coming} coming",
        )

        browser.close()

    for line in notes + failures:
        print(" ", line)
    if failures:
        print(f"\n{len(failures)} FAILED")
        return 1
    print(f"\nall {len(notes)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
