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
import contextlib
import functools
import http.server
import pathlib
import re
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
import glob as _glob
# The sandbox Chromium build number changes between containers (1194, then
# 1243 on 26 Oct 2026). A hard-coded path made point 8 a false alarm each time.
_c = sorted(_glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))
CHROME = _c[-1] if _c else None


@contextlib.contextmanager
def serve(root):
    """Serve the repo over HTTP for the duration of the test.

    This used to load index.html over file://, where a root-relative path
    like /assets/pinkleaf-tailwind.css resolves to the filesystem root and
    404s. So every run was of a page with no Tailwind and no
    pinkleaf-enhancements.js, and a bug in either was invisible here. Over
    HTTP the page loads the way a visitor gets it.
    """
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    handler = functools.partial(Quiet, directory=str(root))
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as httpd:
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            yield f"http://127.0.0.1:{httpd.server_address[1]}"
        finally:
            httpd.shutdown()

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

    with serve(ROOT) as base, sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME) if CHROME else p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 1000})
        errors = []
        missing = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("requestfailed",
                lambda r: missing.append(r.url) if r.url.startswith(base) else None)
        # startswith(base), not "127.0.0.1" in url: Google Analytics beacons
        # carry the page URL as a query parameter, so a blocked GA call in the
        # sandbox used to read as a missing local asset (false alarm, 26 Oct).
        page.goto(f"{base}/index.html")
        page.wait_for_timeout(1200)

        # Get into the store.
        page.evaluate("showPage('store')")
        page.wait_for_timeout(1200)

        counts = page.evaluate("""() => {
            const txt = [...document.querySelectorAll('.add-to-cart-btn')].map(b => b.textContent.trim());
            return {
                cards: document.querySelectorAll('.portal').length,
                // Both labels, both languages. The store defaults to Hebrew,
                // so an English-only matcher reports zero buy buttons on a
                // perfectly working store. That happened on 30 September: the
                // waitlist check already matched both languages, the buy check
                // did not, and the merge that made the store speak Hebrew
                // looked exactly like the 26 September button inversion.
                // If a label changes in index.html, change it here too.
                addToBag: txt.filter(t => /ADD TO BAG|הוספה לסל/i.test(t)).length,
                waitlist: txt.filter(t => /NOTIFY ME|עדכנו אותי/i.test(t)).length,
                buttons: txt.length,
            };
        }""")

        check("page throws no JS errors", not errors, "; ".join(errors[:2]))
        check(
            "every local asset loads",
            not missing,
            ", ".join(u.split("/")[-1] for u in missing[:4]),
        )
        check(
            "the stylesheets actually applied",
            page.evaluate("""() => {
                const hrefs = [...document.styleSheets].map(s => s.href || '');
                return hrefs.some(h => h.includes('tailwind'))
                    && hrefs.some(h => h.includes('enhancements'));
            }"""),
            "tailwind and enhancements css",
        )
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
        # Compare each button count against the DATA, not against each other.
        # This used to assert addToBag > waitlist, which is not what "swapped"
        # means: it only held while most of the catalogue was in stock. On
        # 26 Oct 2026, after 42 plants went to the waitlist and 38 stayed
        # available, it failed on a perfectly correct page. The inversion it
        # exists to catch (26 Sep: every available plant showing NOTIFY ME)
        # still fails here, because then addToBag would be 0 against 38.
        check(
            "the two button types are not swapped",
            counts["addToBag"] == available and counts["waitlist"] == coming,
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
