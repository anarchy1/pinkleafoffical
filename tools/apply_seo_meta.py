#!/usr/bin/env python3
"""Apply tools/seo_meta.json to the article and encyclopedia pages.

For each page listed there it sets the <title>, the meta description and the
matching og: and twitter: tags. A description of null keeps the page's own.
It also adds datePublished and dateModified to the page's Article
structured data when they are missing, taken from git: the commit that
first added the file, and the last commit that touched it. Needs a full
(not shallow) clone for the first date to be right.

Idempotent. Run from the repo root:  python3 tools/apply_seo_meta.py
Prints every title and description length so overlong ones are visible.
"""
import html
import json
import re
import subprocess
import sys

META = json.load(open('tools/seo_meta.json', encoding='utf-8'))


def git_date(path, first):
    args = ['git', 'log', '--format=%ad', '--date=short']
    if first:
        args += ['--diff-filter=A', '--follow']
    args += ['--', path]
    out = subprocess.run(args, capture_output=True, text=True).stdout.split()
    if not out:
        return None
    return out[-1] if first else out[0]


def set_meta(h, attr, key, value):
    pat = re.compile(r'(<meta\s+' + attr + r'="' + re.escape(key) + r'"\s+content=")[^"]*(")')
    return pat.sub(lambda m: m.group(1) + value + m.group(2), h)


def main():
    shallow = subprocess.run(['git', 'rev-parse', '--is-shallow-repository'],
                             capture_output=True, text=True).stdout.strip()
    if shallow == 'true':
        sys.exit('Shallow clone: run "git fetch --unshallow" first, or the publish dates will be wrong.')
    bad = 0
    for path, m in META.items():
        if path.startswith('_'):
            continue
        h = open(path, encoding='utf-8').read()
        title = m['title']
        t_esc = html.escape(title, quote=False)
        h = re.sub(r'<title>.*?</title>', lambda _: '<title>' + t_esc + '</title>', h, count=1, flags=re.S)
        h = set_meta(h, 'property', 'og:title', html.escape(title, quote=True))
        h = set_meta(h, 'name', 'twitter:title', html.escape(title, quote=True))
        desc = m.get('description')
        if desc:
            d_esc = html.escape(desc, quote=True)
            h = set_meta(h, 'name', 'description', d_esc)
            h = set_meta(h, 'property', 'og:description', d_esc)
            h = set_meta(h, 'name', 'twitter:description', d_esc)
        else:
            found = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', h)
            desc = html.unescape(found.group(1)) if found else ''

        # Publish dates in the Article structured data.
        if '"datePublished"' not in h:
            pub, mod = git_date(path, True), git_date(path, False)
            if pub and mod:
                h, n = re.subn(r'("@type"\s*:\s*"(?:Article|BlogPosting)"\s*,)',
                               lambda mm: mm.group(1) + ' "datePublished": "' + pub + '", "dateModified": "' + mod + '",',
                               h, count=1)
                if not n:
                    print('  no Article block to date:', path)
        open(path, 'w', encoding='utf-8').write(h)

        flag = ''
        if len(title) > 60:
            flag += ' TITLE>60'
        if not (100 <= len(desc) <= 160):
            flag += ' DESC %d' % len(desc)
        if flag:
            bad += 1
        print('%3d %3d %s%s' % (len(title), len(desc), path, flag))
    print('pages with a length outside the target:', bad)


if __name__ == '__main__':
    main()
