#!/usr/bin/env python3
"""Rebuild the storefront from a single CSV.

tools/store-catalog.csv is the one place Kat edits the store. One row is one
plant variant: its name, category, whether it is selling now or coming soon,
and its price. This script reads that file and regenerates two blocks inside
index.html (ALL_STORE_ITEMS and ITEM_PRICES), so names, prices, categories,
and now/soon status can never drift apart again.

Usage:
    python3 tools/build_store.py            # rebuild index.html from the CSV
    python3 tools/build_store.py --check    # verify index.html matches the CSV

The store grid renders available plants first, then "coming soon", so CSV row
order only needs to be a sensible grouping; it does not have to be sorted.
"""

import csv
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CSV_PATH = os.path.join(HERE, "store-catalog.csv")
HTML_PATH = os.path.join(ROOT, "index.html")

# status word in the CSV -> status value the store JS expects
STATUS_MAP = {"now": "available", "soon": "coming"}
VALID_ACCLIMATION = {"in-transit", "customs", "deflasked", "hardening"}

ITEMS_BEGIN = "// >>> BEGIN GENERATED: store items"
ITEMS_END = "// >>> END GENERATED: store items <<<"
PRICES_BEGIN = "// >>> BEGIN GENERATED: item prices"
PRICES_END = "// >>> END GENERATED: item prices <<<"


def load_catalog():
    """Read the CSV into an ordered list of plants, each with its variants."""
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    order = []          # plant ids in first-seen order
    plants = {}         # id -> plant dict
    errors = []

    for n, row in enumerate(rows, start=2):  # line 1 is the header
        pid = (row.get("id") or "").strip()
        name = (row.get("name") or "").strip()
        category = (row.get("category") or "").strip()
        status_word = (row.get("status") or "").strip().lower()
        acclimation = (row.get("acclimation") or "").strip()
        light = (row.get("light") or "").strip()
        humidity = (row.get("humidity") or "").strip()
        variant = (row.get("variant") or "").strip()
        price_raw = (row.get("price") or "").strip()

        if not pid:
            errors.append(f"line {n}: missing id")
            continue
        if not name:
            errors.append(f"line {n} ({pid}): missing name")
        if status_word not in STATUS_MAP:
            errors.append(f"line {n} ({pid}): status must be 'now' or 'soon', got '{status_word}'")
        if acclimation and acclimation not in VALID_ACCLIMATION:
            errors.append(
                f"line {n} ({pid}): acclimation '{acclimation}' is not one of "
                + ", ".join(sorted(VALID_ACCLIMATION))
            )
        if not variant:
            errors.append(f"line {n} ({pid}): missing variant")
        price = None
        if price_raw:
            try:
                price = int(price_raw)
            except ValueError:
                errors.append(f"line {n} ({pid}): price '{price_raw}' is not a whole number")

        if pid not in plants:
            order.append(pid)
            plants[pid] = {
                "id": pid,
                "name": name,
                "family": category,
                "status": STATUS_MAP.get(status_word, "available"),
                "acclimation": acclimation,
                "light": light,
                "humidity": humidity,
                "variants": [],  # list of (variant, price)
            }
        plants[pid]["variants"].append((variant, price))

    if errors:
        raise ValueError("Catalog problems found:\n  - " + "\n  - ".join(errors))

    return [plants[pid] for pid in order]


def js_string(value):
    """Escape a value for a double-quoted JS string."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def render_items(plants):
    lines = ["        const ALL_STORE_ITEMS = ["]
    for p in plants:
        variants = ", ".join(f'"{js_string(v)}"' for v, _ in p["variants"])
        parts = [
            f'id: "{js_string(p["id"])}"',
            f'name: "{js_string(p["name"])}"',
            f'family: "{js_string(p["family"])}"',
            f'availability: [{variants}]',
            f'light: "{js_string(p["light"])}"',
            f'humidity: "{js_string(p["humidity"])}"',
            f'status: "{p["status"]}"',
        ]
        if p["acclimation"]:
            parts.append(f'acclimation: "{p["acclimation"]}"')
        lines.append("            { " + ", ".join(parts) + " },")
    lines.append("        ];")
    return "\n".join(lines)


def render_prices(plants):
    lines = ["        const ITEM_PRICES = {"]
    for p in plants:
        for variant, price in p["variants"]:
            if price is None:
                continue
            key = js_string(f'{p["id"]}_{variant}')
            lines.append(f'            "{key}": {price},')
    lines.append("        };")
    return "\n".join(lines)


def replace_block(html, begin_marker, end_marker, new_body):
    """Replace everything between (but not including) the marker lines."""
    pattern = re.compile(
        r"(" + re.escape(begin_marker) + r".*?\n)"   # begin marker line(s)
        r".*?"                                        # old body
        r"(\n[ \t]*" + re.escape(end_marker) + r")",  # end marker line
        re.DOTALL,
    )
    if not pattern.search(html):
        raise ValueError(f"Could not find markers: {begin_marker} ... {end_marker}")
    # Keep the comment lines that follow the begin marker up to the const.
    def _sub(m):
        head = m.group(1)
        # Preserve any extra comment lines between begin marker and the const.
        head_lines = []
        for line in head.splitlines(keepends=True):
            if line.lstrip().startswith("// Do not hand-edit"):
                head_lines.append(line)
        head_block = m.group(1)
        return head_block + new_body + m.group(2)
    return pattern.sub(_sub, html, count=1)


def validate_js(items_js, prices_js):
    """Run the generated JS through node so a typo can never reach the site."""
    snippet = items_js + "\n" + prices_js + "\n"
    snippet += "if (!Array.isArray(ALL_STORE_ITEMS)) throw new Error('items not an array');\n"
    snippet += "if (typeof ITEM_PRICES !== 'object') throw new Error('prices not an object');\n"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tf:
        tf.write(snippet)
        tmp = tf.name
    try:
        subprocess.run(["node", "--check", tmp], check=True,
                       capture_output=True, text=True)
        subprocess.run(["node", tmp], check=True, capture_output=True, text=True)
    except FileNotFoundError:
        print("  (node not found: skipped JS syntax validation)")
    except subprocess.CalledProcessError as e:
        raise ValueError("Generated JS failed validation:\n" + (e.stderr or e.stdout))
    finally:
        os.unlink(tmp)


def main():
    check_only = "--check" in sys.argv
    plants = load_catalog()
    items_js = render_items(plants)
    prices_js = render_prices(plants)
    validate_js(items_js, prices_js)

    with open(HTML_PATH, encoding="utf-8") as f:
        html = f.read()

    new_html = replace_block(html, ITEMS_BEGIN, ITEMS_END, items_js)
    new_html = replace_block(new_html, PRICES_BEGIN, PRICES_END, prices_js)

    n_now = sum(1 for p in plants if p["status"] == "available")
    n_soon = len(plants) - n_now
    n_prices = sum(1 for p in plants for _, pr in p["variants"] if pr is not None)

    if check_only:
        if new_html != html:
            print("OUT OF SYNC: index.html does not match tools/store-catalog.csv.")
            print("Run: python3 tools/build_store.py")
            sys.exit(1)
        print(f"In sync: {len(plants)} plants ({n_now} now, {n_soon} soon), {n_prices} prices.")
        return

    if new_html == html:
        print(f"No change. {len(plants)} plants ({n_now} now, {n_soon} soon), {n_prices} prices.")
        return

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Rebuilt store: {len(plants)} plants ({n_now} now, {n_soon} soon), {n_prices} prices.")


if __name__ == "__main__":
    main()
