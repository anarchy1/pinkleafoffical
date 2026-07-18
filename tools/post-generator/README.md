# Pink Leaf post generator

The durable version of the Instagram post design system. Regenerates the branded
posts (arch photo, big logo, Hebrew story, care list) as 1080x1553 PNGs, so we
never have to rebuild the template from scratch again.

## What's here
- `generate_posts.py` - the generator (template + renderer)
- `posts_data.json` - the content for each post (name, story, care set, photo, crop)
- `photos/` - the plant photo used for each post
- Output goes to `../../social-posts/` (images) alongside `captions.md`

## Run it
```
pip install pillow pillow-heif
python3 generate_posts.py
```
Needs a Chromium binary. It auto-detects `/opt/pw-browsers/chromium-*` or one on
PATH; otherwise set `CHROME=/path/to/chrome`.

## Add or change a post
1. Drop the plant photo in `photos/` (jpg/png/webp/heic all fine).
2. Add an entry to `posts_data.json`:
   - `h1a`,`h1b`: headline, two lines (Hebrew)
   - `subhe`,`suben`: Hebrew subtitle + English name
   - `story`: the Hebrew story paragraph
   - `care`: `"ALO"` (Alocasia care set) or `"MON"` (Monstera care set)
   - `photo`: filename in `photos/`
   - `bgpos`: CSS background-position to frame the leaf, e.g. `"center 30%"`
3. Re-run. To tune the crop so the leaf is centered, adjust `bgpos`
   (lower percentage pulls the view toward the top of the photo).

## Rules
- Product/in-stock posts must use a real photo of the actual plant.
- Captions live in `../../social-posts/captions.md`.
