#!/usr/bin/env python3
"""Cut the weight of the images the site ships.

Run from the repo root:
    python3 tools/optimize_images.py --dry-run     # report, change nothing
    python3 tools/optimize_images.py               # do it

Why: plants/ was 76 MB across 228 photos, 58 of them wider than 1600px and
the largest 3 MB, while the biggest the site ever renders one is a 140px
circle (192px on the product panel). Lazy loading kept the first paint cheap,
but anyone scrolling the archive on mobile data was paying for full camera
resolution to fill a thumbnail.

The cap is deliberately generous: 1400px on the long edge is still more than
three times the largest rendered size, so there is room for a retina screen
and for opening a photo directly. Quality 85 progressive is the usual sweet
spot for photographs; below about 80 the compression starts showing on leaf
edges and variegation, which is the whole product here.

Anything already small enough is left untouched, so re-running is cheap and
does not re-compress a file that has already been through this.
"""
import argparse
import glob
import os
import sys

from PIL import Image

MAX_EDGE = 1400
QUALITY = 85
# Below this there is nothing worth doing, and recompressing would only lose
# detail for a few kilobytes.
SKIP_UNDER_KB = 150

ICONS = [
    # (path, target square size). The favicon was 612x408: not square, so
    # browsers squashed or cropped it, and 132 KB for a 32px tab icon.
    ('favicon.png', 180),
    ('logo-dark.png', 400),
    ('logo-light.png', 400),
]


def kb(path):
    return os.path.getsize(path) / 1024


def do_photo(path, dry):
    before = kb(path)
    if before < SKIP_UNDER_KB:
        return 0, 0, False
    im = Image.open(path)
    w, h = im.size
    scale = MAX_EDGE / max(w, h)
    resized = scale < 1
    if not dry:
        if im.mode not in ('RGB', 'L'):
            im = im.convert('RGB')
        if resized:
            im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        im.save(path, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
        after = kb(path)
    else:
        # estimate only; the real number comes from the non-dry run
        after = before * (0.25 if resized else 0.6)
    return before, after, resized


def do_icon(path, size, dry):
    before = kb(path)
    im = Image.open(path).convert('RGBA')
    w, h = im.size
    if not dry:
        # Fit inside a square canvas rather than cropping, so a non-square
        # source keeps its whole subject instead of losing the edges.
        scale = min(size / w, size / h)
        im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
        canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        canvas.paste(im, ((size - im.width) // 2, (size - im.height) // 2), im)
        canvas.save(path, 'PNG', optimize=True)
        after = kb(path)
    else:
        after = before * 0.1
    return before, after, (w, h)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    dry = args.dry_run

    photos = sorted(glob.glob('plants/*.jpg')) + sorted(glob.glob('plants/**/*.jpg', recursive=True))
    photos = sorted(set(photos))
    before_total = after_total = 0
    touched = resized_count = 0
    for f in photos:
        b, a, resized = do_photo(f, dry)
        if b:
            touched += 1
            resized_count += int(resized)
            before_total += b
            after_total += a
        else:
            s = kb(f)
            before_total += s
            after_total += s

    print('photos: %d total, %d rewritten (%d also resized)' % (len(photos), touched, resized_count))
    print('  plants/  %.1f MB -> %.1f MB  (%.0f%% smaller)%s' % (
        before_total / 1024, after_total / 1024,
        100 * (1 - after_total / before_total) if before_total else 0,
        '   [estimate]' if dry else ''))

    for path, size in ICONS:
        if not os.path.exists(path):
            continue
        b, a, dims = do_icon(path, size, dry)
        print('  %-16s %dx%d %.0f KB -> %d x %d %.0f KB%s' % (
            path, dims[0], dims[1], b, size, size, a, '   [estimate]' if dry else ''))

    if dry:
        print('\nnothing was written. run without --dry-run to apply.')


if __name__ == '__main__':
    sys.exit(main())
