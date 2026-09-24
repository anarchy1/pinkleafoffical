#!/usr/bin/env python3
"""Remove em dashes from the content that predates the repo's writing rule.

Run from the repo root:
    python3 tools/strip_em_dashes.py --dry-run
    python3 tools/strip_em_dashes.py

CLAUDE.md forbids em dashes in every file in this repo, and the PostToolUse
hook enforces it going forward. Content written before that rule still carried
them: 755 across entries.json and the encyclopedia, 1057 across the articles.

Every one of them is the same shape, a space, the dash, a space, which is what
makes replacing them safely possible. Two rules:

  in a title      ->  a colon      "Reading Leaf Symptoms: What Your Plant..."
  in prose        ->  a comma      "This is not an opinion, it is chemistry."

A title means a <title> tag, an og:title, a JSON-LD headline, an <h1>, or a
title field in entries.json. Everywhere else reads as a clause break, and a
comma is what the rule itself recommends.

The characters are built with chr() because the Humanizer hook rewrites long
dashes inside source files, which would otherwise turn this script's own
patterns into something else.
"""
import argparse
import glob
import json
import re

EM = chr(0x2014)
BAR = chr(0x2015)
IN_TITLE = ': '
IN_PROSE = ', '

TITLE_FIELDS = ('title_he', 'title_en')


def fix_json_value(value, is_title):
    rep = IN_TITLE if is_title else IN_PROSE
    for ch in (EM, BAR):
        value = value.replace(' %s ' % ch, rep).replace(ch, ',')
    return value


def walk(node, is_title=False):
    if isinstance(node, dict):
        return {k: walk(v, k in TITLE_FIELDS) for k, v in node.items()}
    if isinstance(node, list):
        return [walk(v, is_title) for v in node]
    if isinstance(node, str):
        return fix_json_value(node, is_title)
    return node


def count(text):
    return text.count(EM) + text.count(BAR)


# Regions of an HTML file where a long dash is separating a title from its
# subtitle rather than breaking a sentence.
TITLE_REGIONS = [
    re.compile(r'<title>.*?</title>', re.S),
    re.compile(r'<meta property="og:title" content="[^"]*"'),
    re.compile(r'"headline":\s*"[^"]*"'),
    re.compile(r'<h1[^>]*>.*?</h1>', re.S),
]


def fix_html(text):
    def in_title(m):
        s = m.group(0)
        for ch in (EM, BAR):
            s = s.replace(' %s ' % ch, IN_TITLE).replace(ch, ',')
        return s

    for rx in TITLE_REGIONS:
        text = rx.sub(in_title, text)
    for ch in (EM, BAR):
        text = text.replace(' %s ' % ch, IN_PROSE).replace(ch, ',')
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    total_before = 0
    changed = []

    raw = open('entries.json', encoding='utf8').read()
    before = count(raw)
    total_before += before
    if before and not args.dry_run:
        data = json.load(open('entries.json', encoding='utf8'))
        json.dump(walk(data), open('entries.json', 'w', encoding='utf8'),
                  ensure_ascii=False, indent=2)
    if before:
        changed.append(('entries.json', before))

    files = sorted(glob.glob('encyclopedia/*.html')) + sorted(glob.glob('articles/**/*.html', recursive=True))
    for f in files:
        text = open(f, encoding='utf8').read()
        before = count(text)
        if not before:
            continue
        total_before += before
        changed.append((f, before))
        if not args.dry_run:
            open(f, 'w', encoding='utf8').write(fix_html(text))

    print('files carrying long dashes: %d' % len(changed))
    print('occurrences: %d' % total_before)
    for f, n in changed[:6]:
        print('   %-52s %4d' % (f, n))
    if len(changed) > 6:
        print('   ... and %d more files' % (len(changed) - 6))
    if args.dry_run:
        print('\ndry run, nothing written')
    else:
        left = count(open('entries.json', encoding='utf8').read()) + sum(
            count(open(f, encoding='utf8').read()) for f in files)
        print('\nremaining after the pass: %d' % left)


if __name__ == '__main__':
    main()
