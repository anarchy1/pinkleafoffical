#!/usr/bin/env python3
"""Generate the hub pages: /encyclopedia/index.html and /articles/index.html.

Run from the repo root:   python3 tools/build_index_pages.py

Why: both directories held content with no index, so trimming a URL gave a
404, and six Hebrew article pages had no inbound link from anywhere on the
site at all. A hub page fixes discoverability for readers and for crawlers in
one move.

Both pages are generated from what is actually on disk, so they cannot drift:
the encyclopedia list comes from entries.json, the article list from the
<title> and meta description of each article file.
"""
import html as H
import json
import os
import re
import glob

SITE = 'https://pinkleaf.co.il'

# The repo forbids em dashes. Article titles written before that rule still
# carry them, so normalise anything quoted into a generated file.
def clean(s):
    # Built with chr() on purpose: the repo's Humanizer hook rewrites literal
    # long dashes inside source files, which silently turned an earlier version
    # of this function into a plain-hyphen replacer.
    return s.replace(chr(0x2014), ',').replace(chr(0x2015), ',').strip()


STYLE = """
        :root { color-scheme: light; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 860px; margin: 0 auto; padding: 20px 20px 60px; color: #1a1a1a; line-height: 1.7; background: #fafaf8; }
        nav.crumb { margin-bottom: 26px; font-size: 0.9em; }
        nav.crumb a { color: #4a7c59; text-decoration: none; }
        header.hero { border-bottom: 1px solid #e3ded5; padding-bottom: 22px; margin-bottom: 8px; }
        h1 { font-size: 1.9em; font-weight: 700; margin: 0 0 6px; color: #111; }
        h1 .he { display: block; font-size: 0.78em; font-weight: 500; color: #4a7c59; direction: rtl; margin-top: 4px; }
        .lede { color: #666; margin: 0; max-width: 62ch; }
        h2.group { font-size: 0.8em; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: #4a7c59; margin: 34px 0 2px; }
        h2.group .n { color: #a9a29a; font-weight: 500; }
        ul.list { list-style: none; padding: 0; margin: 0; }
        ul.list li { border-bottom: 1px solid #ece7e0; padding: 15px 0; }
        ul.list li:last-child { border-bottom: 0; }
        .item-title { font-size: 1.04em; font-weight: 600; }
        .item-title a { color: #1a1a1a; text-decoration: none; }
        .item-title a:hover { color: #4a7c59; }
        .item-he { direction: rtl; text-align: right; color: #4a7c59; font-size: 0.95em; margin-top: 2px; }
        .item-sub { color: #6c6560; font-size: 0.9em; margin-top: 4px; }
        .item-sub.he { direction: rtl; text-align: right; }
        .tag { display: inline-block; background: #e8f5e9; color: #2e7d32; padding: 2px 9px; border-radius: 12px; font-size: 0.72em; letter-spacing: 0.04em; margin-bottom: 6px; }
        .cta { margin-top: 44px; padding: 22px; background: #4a7c59; color: white; border-radius: 12px; text-align: center; }
        .cta a { color: white; font-weight: 700; }
        footer { margin-top: 44px; padding-top: 22px; border-top: 1px solid #ddd; font-size: 0.85em; color: #888; }
        footer a { color: #4a7c59; text-decoration: none; }
"""

FOOT = """    <div class="cta">
        <p>&#127807; Have questions? We&#39;re here.</p>
        <p><a href="https://wa.me/972559116990">WhatsApp: +972-55-911-6990</a> &nbsp;&#183;&nbsp; <a href="https://www.instagram.com/pinkleaf.studio/">@pinkleaf.studio</a></p>
    </div>
    <footer>
        <p><a href="https://pinkleaf.co.il/">Pink Leaf Botanical Studios</a> &middot; Israel&#39;s rare aroid plant studio</p>
        <p>&#128231; <a href="mailto:contact@pinkleaf.co.il">contact@pinkleaf.co.il</a> &middot; <a href="https://www.instagram.com/pinkleaf.studio/">@pinkleaf.studio</a></p>
    </footer>
</body>
</html>
"""


def shell(path, title, desc, h1_en, h1_he, lede, body):
    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{H.escape(title)}</title>
    <meta name="description" content="{H.escape(desc, quote=True)}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="Pink Leaf Botanical Studios">
    <link rel="canonical" href="{SITE}/{path}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{SITE}/{path}">
    <meta property="og:title" content="{H.escape(title)}">
    <meta property="og:description" content="{H.escape(desc, quote=True)}">
    <meta property="og:image" content="{SITE}/assets/og-pinkleaf.jpg">
    <meta property="og:site_name" content="Pink Leaf Botanical Studios">
    <style>{STYLE}    </style>
</head>
<body>
    <nav class="crumb"><a href="{SITE}/">&#8592; Pink Leaf</a></nav>
    <header class="hero">
        <h1>{H.escape(h1_en)}<span class="he">{H.escape(h1_he)}</span></h1>
        <p class="lede">{H.escape(lede)}</p>
    </header>
{body}
{FOOT}"""


def build_encyclopedia():
    d = json.load(open('entries.json', encoding='utf8'))
    entries = d['entries']
    rows = []
    for e in entries:
        slug = e['slug']
        if not os.path.exists('encyclopedia/%s.html' % slug):
            continue
        rows.append(
            '        <li>\n'
            '            <span class="tag">%s</span>\n'
            '            <div class="item-title"><a href="%s.html">%s</a></div>\n'
            '            <div class="item-he">%s</div>\n'
            '            <div class="item-sub">%s</div>\n'
            '        </li>' % (
                H.escape(clean(e['tag_en'])),
                slug,
                H.escape(clean(e['title_en'])),
                H.escape(clean(e['title_he'])),
                H.escape(clean(e['subtitle_en'])),
            ))
    body = ('    <h2 class="group">All entries <span class="n">%d</span></h2>\n'
            '    <ul class="list">\n%s\n    </ul>' % (len(rows), '\n'.join(rows)))
    page = shell(
        'encyclopedia/',
        'Botanical Encyclopedia: %d Technical Guides | Pink Leaf' % len(rows),
        'Every Pink Leaf Masterclass entry in one place: tissue culture, substrate, '
        'watering, fertilizing, pests, propagation and plant profiles. Each guide is '
        'written in Hebrew and English.',
        'Botanical Encyclopedia', 'אנציקלופדיה בוטנית',
        'Every Masterclass entry, each one written in both Hebrew and English, with the '
        'protocol and the numbers we actually use in the studio.',
        body)
    open('encyclopedia/index.html', 'w', encoding='utf8').write(page)
    return len(rows)


def article_meta(f):
    t = open(f, encoding='utf8').read()
    ti = re.search(r'<title>(.*?)</title>', t, re.S)
    de = re.search(r'<meta name="description" content="(.*?)"', t, re.S)
    la = re.search(r'<html lang="([a-z]+)"', t)
    title = H.unescape(ti.group(1)).strip() if ti else os.path.basename(f)
    title = re.sub(r'\s*\|\s*Pink Leaf\s*$', '', title)
    desc = H.unescape(de.group(1)).strip() if de else ''
    return {'file': f, 'title': clean(title), 'desc': clean(desc),
            'lang': la.group(1) if la else 'en'}


def build_articles():
    files = sorted(glob.glob('articles/*.html')) + sorted(glob.glob('articles/heb/*.html'))
    files = [f for f in files if os.path.basename(f) != 'index.html']
    metas = [article_meta(f) for f in files]
    groups = [('en', 'In English', metas), ('he', 'בעברית', metas)]
    parts = []
    for code, heading, _ in groups:
        sel = [m for m in metas if m['lang'] == code]
        rows = []
        for m in sel:
            href = os.path.relpath(m['file'], 'articles')
            he = code == 'he'
            rows.append(
                '        <li>\n'
                '            <div class="item-title"%s><a href="%s">%s</a></div>\n'
                '            <div class="item-sub%s">%s</div>\n'
                '        </li>' % (
                    ' dir="rtl" style="text-align:right"' if he else '',
                    href, H.escape(m['title']),
                    ' he' if he else '', H.escape(m['desc'])))
        parts.append('    <h2 class="group">%s <span class="n">%d</span></h2>\n'
                     '    <ul class="list">\n%s\n    </ul>' % (H.escape(heading), len(sel), '\n'.join(rows)))
    page = shell(
        'articles/',
        'Plant Care Articles, Hebrew and English | Pink Leaf',
        'Long-form care guides for rare aroids in Israel: substrate, humidity, watering, '
        'pests, propagation, variegation and buying advice, in Hebrew and English.',
        'Care Articles', 'מאמרי טיפול',
        'Long-form guides written for growing rare aroids in an Israeli home. '
        'The Hebrew and English articles are separate pieces, not translations of each other.',
        '\n'.join(parts))
    open('articles/index.html', 'w', encoding='utf8').write(page)
    return sum(1 for m in metas if m['lang'] == 'en'), sum(1 for m in metas if m['lang'] == 'he')


if __name__ == '__main__':
    n = build_encyclopedia()
    en, he = build_articles()
    print('encyclopedia/index.html: %d entries' % n)
    print('articles/index.html: %d English, %d Hebrew' % (en, he))
