# Pink Leaf brand assets

Read this before putting the logo on anything: a card, a post, a slide, a
label, a page. It exists so nobody has to ask Kat where the logo is, and so
nobody invents one again.

Cloud sessions can only see this repository. The design pack on the Mac does
not travel. If an asset is not in this folder, it does not exist as far as any
cloud session is concerned.

---

## The rule

**Never crop the logo. Never rebuild it in text. Never substitute an emoji.**

Use a file from this folder, whole, at the sizes below. If the asset you need
is not here, stop and ask Kat for it rather than improvising one. An
improvised logo is worse than no logo, because it ships looking almost right
and only she notices.

This rule exists because a session cropped the circular mark out of the
website header logo and used the crop on five Instagram cards. It looked wrong
at a glance and she had to catch it twice.

---

## What is actually here

| File | What it is | Use it for |
| --- | --- | --- |
| `brand/lockup-rose-trimmed.png` | The full lockup (circular monstera mark above PINK LEAF / Botanical Studios) in rose gold, transparent, trimmed to the artwork at 293 x 316 px | Anything on a light or cream background: Instagram cards, printed labels, documents |
| `logo-light.png` (repo root) | Same lockup, **white** wordmark, 500 x 500 with transparent padding | The website only, on dark backgrounds |
| `logo-dark.png` (repo root) | Same lockup, **rose gold** wordmark, 500 x 500 with transparent padding | The website only, on light backgrounds. `lockup-rose-trimmed.png` is this file trimmed |
| `favicon.png` (repo root) | A simple pink gradient leaf, 612 x 408. **Not the real mark.** A different drawing entirely | Browser tab icon only. Never use it as the logo |

The light/dark naming refers to the mode the file is used in on the site, not
to the colour of the artwork. That is easy to get backwards, so check the
actual file before using it.

---

## What is missing, and what to ask Kat for

The design pack on her Mac has these. The repository does not. Until they are
committed here, every design job is working from a 293 px raster, which is
marginal for anything printed or rendered at 2x.

1. **Vector master** of the full lockup (`.svg`, `.ai` or `.eps`). This is the
   single most useful thing to add.
2. **The mark on its own**, as a designed standalone asset: the circle and the
   monstera leaf with no wordmark, drawn to work at small sizes. A crop of the
   lockup is not this.
3. **High resolution raster** of the lockup, 2000 px on the long edge or more,
   transparent PNG, in both the rose gold and the white versions.
4. **A horizontal lockup** if one exists (mark to the left of the wordmark
   rather than above it). The vertical lockup is awkward in a wide header.
5. **The brand font**, if the wordmark is set in a real typeface rather than
   custom lettering, plus its licence terms.
6. **The official colour values.** The ones below were sampled from the
   artwork and from existing cards. They are good enough to work with and they
   are not authoritative.

Drop them into `brand/` and update the table above. Nothing in this folder is
private: the logo is on the public site already, so committing brand assets
does not conflict with the private data rules in `CLAUDE.md`.

---

## Colours currently in use

Sampled, not official. Replace if the design pack says otherwise.

| Token | Hex | Where |
| --- | --- | --- |
| Cream | `#EFE8DB` | Card background |
| Deep green | `#33503A` | Headings, Hebrew plant names |
| Rose | `#C4708A` | Latin names, the handle, accents |
| Body | `#4A4038` | Body text |
| Hairline | `#CFC6B5` | Rules and dividers |
| Photo frame | `#F6F2E9` | The border around photos |

---

## Instagram card spec

Two page carousel. Page 1 is the plant info card. Page 2 is the parentage card
for a hybrid, or the story card for everything else.

- Canvas 1080 x 1350, rendered at device scale 2.
- Logo: `lockup-rose-trimmed.png` at 118 px tall, top left, followed by a
  hairline rule across the rest of the width. Nothing else in the masthead.
- Footer: text only. Three lines plus the handle, right aligned, no logo.
- The handle needs `dir="ltr"` or Hebrew RTL renders it as `pinkleaf.studio@`.
- Fonts: Frank Ruhl Libre for Hebrew headings, Assistant for Hebrew body,
  Cormorant Garamond for Latin names.
- Never put a price, a supplier name, or acclimation state on a card.

Render scripts live in the session scratchpad, which does not survive between
sessions. If the cards need rebuilding, the spec above is the record.
