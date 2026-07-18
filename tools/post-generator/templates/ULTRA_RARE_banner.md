# ULTRA RARE banner - placement reference

Approved 2026-07-06. Reference image: `ULTRA_RARE_banner_reference.png`
(the Ocean Mint post).

## It is now automatic (do not hand-place it)
The banner is baked into `generate_posts.py`. To put the ULTRA RARE banner on a
post, add `"ultra": true` to that plant's entry in `posts_data.json`. The
generator draws it for you at the locked position. Leave the flag off for
everyday plants. To render one post: `python3 generate_posts.py 14-venom-pink`.

Locked geometry (in `add_banner` / `_ribbon` / `_arch_mask`): a "\" ribbon at
angle -45, pink fill (201,141,160) with a cream inset border and cream text
"✦ ULTRA RARE ✦" in FreeSerifBold, centered at (895, 250), then CLIPPED to the
arch shape so the ends sit flush to the arch edge. If the arch photo rect ever
changes in the CSS, update AL/AT/AW/AH at the top of the banner section to match.

## The rule (this is the approved look)
- The banner is a diagonal ribbon across the **TOP-RIGHT corner of the arch
  photo**, not the corner of the whole post.
- It runs at roughly -45 degrees (top-right to lower-left), tucked so both ends
  sit just past the arch edge, spanning corner to corner of the photo.
- Colors: pink fill (approx c98da0 / rgb 201,141,160), cream inset border,
  cream text.
- Text: `ULTRA RARE` in FreeSerifBold, small star glyph on each side.
- The PINK LEAF wordmark (top-left of the post) stays fully clear. The banner
  never touches it. This is why the banner lives on the photo, not the post
  corner.

## When to use it
Only on ultra-rare varieties (the premium tier). Pair with "ultra rare" and
"coming soon" language in the caption. Keep it OFF everyday varieties so it
stays meaningful.

## Not this
- Not a circular sticker (rejected).
- Not on the top-left post corner (collides with the PINK LEAF wordmark).
- Not chroma-keyed onto the image (green key ate the pink fill). Draw the ribbon
  directly with PIL, then paste using the ribbon's own alpha as the mask.
