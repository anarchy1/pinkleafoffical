#!/usr/bin/env python3
"""Wire a batch of encyclopedia entries into entries.json, standalone pages, footer links and sitemap.

Usage, from the repo root:   python3 content/build-entries.py content/new-entries-YYYY-MM-DD.json

Idempotent: skips slugs that already exist, so it is safe to re-run after
editing the source JSON (delete the generated page first to regenerate it).
Each entry needs a "short" field: the label used for the footer link."""
import json, re, html, datetime, os, sys

if len(sys.argv) < 2:
    sys.exit('usage: python3 content/build-entries.py content/new-entries-YYYY-MM-DD.json')
new = json.load(open(sys.argv[1], encoding='utf8'))

# 1) entries.json
d = json.load(open('entries.json', encoding='utf8'))
slugs = {e['slug'] for e in d['entries']}
added = [e for e in new if e['slug'] not in slugs]
# 'short' is a build-time label for the footer link, not part of the entry schema
d['entries'] += [{k: v for k, v in e.items() if k != 'short'} for e in added]
json.dump(d, open('entries.json', 'w', encoding='utf8'), ensure_ascii=False, indent=2)
print('entries.json:', len(d['entries']), 'entries (+%d)' % len(added))

# 2) standalone HTML pages from the existing template
tpl = open('encyclopedia/engineered-substrates.html', encoding='utf8').read()
SUB_OLD = 'Potting soil is slow death. This is not an opinion — it is chemistry.'
HE_LABEL = '<div class="lang-label">&#1506;&#1489;&#1512;&#1497;&#1514;</div>'

def page(e):
    s = tpl
    s = s.replace('engineered-substrates.html', e['slug'] + '.html')
    s = s.replace('Engineered Substrate for Rare Aroids | Pink Leaf', html.escape(e['title_en']) + ' | Pink Leaf')
    s = s.replace('"headline": "Engineered Substrate for Rare Aroids"', '"headline": ' + json.dumps(e['title_en'], ensure_ascii=False))
    s = s.replace('<h1>Engineered Substrate for Rare Aroids</h1>', '<h1>' + html.escape(e['title_en']) + '</h1>')
    s = s.replace('content="' + SUB_OLD + '"', 'content="' + html.escape(e['meta_description_en'], quote=True) + '"')
    s = s.replace('"description": "' + SUB_OLD + '"', '"description": ' + json.dumps(e['meta_description_en'], ensure_ascii=False))
    s = s.replace('<p class="subtitle">' + SUB_OLD + '</p>', '<p class="subtitle">' + html.escape(e['subtitle_en']) + '</p>')
    s = s.replace('<span class="tag">Substrate Engineering</span>', '<span class="tag">' + html.escape(e['tag_en']) + '</span>')
    s = re.sub(r'(<div class="lang-label">English</div>\s*)<div class="content">.*?</div>',
               lambda m: m.group(1) + '<div class="content">' + html.escape(e['content_en']) + '</div>', s, count=1, flags=re.S)
    s = re.sub(r'(' + re.escape(HE_LABEL) + r'\s*)<div class="content">.*?</div>',
               lambda m: m.group(1) + '<div class="content">' + html.escape(e['content_he']) + '</div>', s, count=1, flags=re.S)
    un = html.unescape(s)
    assert e['content_en'][:40] in un and e['content_he'][:20] in un, e['slug']
    assert 'is slow death' not in s and 'Substrate Engineering' not in s and 'Orchiata Bark, 30%' not in s, 'template residue in ' + e['slug']
    open('encyclopedia/' + e['slug'] + '.html', 'w', encoding='utf8').write(s)
    return len(s)

for e in new:
    if not os.path.exists('encyclopedia/' + e['slug'] + '.html'):
        print('page', e['slug'], page(e), 'bytes')

# 3) footer links in index.html
idx = open('index.html', encoding='utf8').read()
anchor = '<a href="/encyclopedia/plant-health-indicators.html" style="color:inherit; text-decoration:none; opacity:0.7;">Plant Health Indicators</a>'
assert idx.count(anchor) == 1
short = {e['slug']: e.get('short', e['title_en'].split(':')[0].strip()) for e in new}
links = ''.join('\n                <a href="/encyclopedia/%s.html" style="color:inherit; text-decoration:none; opacity:0.7;">%s</a>'
                % (e['slug'], short[e['slug']]) for e in new if ('/encyclopedia/%s.html' % e['slug']) not in idx)
idx = idx.replace(anchor, anchor + links)
open('index.html', 'w', encoding='utf8').write(idx)
print('index.html: footer links added:', links.count('<a '))

# 4) sitemap
sm = open('sitemap.xml', encoding='utf8').read()
line = '  <url><loc>https://pinkleaf.co.il/encyclopedia/plant-health-indicators.html</loc>'
i = sm.find(line); j = sm.find('\n', i) + 1
today = datetime.date.today().isoformat()
add = ''.join('  <url><loc>https://pinkleaf.co.il/encyclopedia/%s.html</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
              % (e['slug'], today) for e in new if e['slug'] + '.html' not in sm)
sm = sm[:j] + add + sm[j:]
open('sitemap.xml', 'w', encoding='utf8').write(sm)
print('sitemap.xml: urls added:', add.count('<url>'))
