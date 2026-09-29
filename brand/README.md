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
| `brand/logo-round-online.jpg` | **The current online logo**, added 26 Sep 2026. Round, cream and rose, split green and pink monstera inside a gold ring, wordmark, then site, phone and Instagram. 1254 x 1254 | Profile pictures and anywhere the brand needs to appear as a single round badge with contact details |
| `brand/sticker-printed-kawaii-round.jpg` | **A sticker that was actually printed.** Round, holographic, kawaii split monstera with a face, "grown with love." and the handle. 1254 x 1254 | Reference for the sticker line. Not a logo, do not use it as one |
| `brand/sticker-concepts-sheet.jpg` | Eleven sticker **concepts** on one sheet, kawaii and pixel art, holographic. Not printed, not chosen | Picking the collectible set. Concepts only |

The light/dark naming refers to the mode the file is used in on the site, not
to the colour of the artwork. That is easy to get backwards, so check the
actual file before using it.

### Three different things, do not mix them up

This has already caused confusion, so it is written down.

1. **The round online logo** (`logo-round-online.jpg`) is what Kat shows as the
   logo online right now. She calls it temporary, so expect it to change.
2. **The website header pair** (`logo-light.png` / `logo-dark.png`) is still
   what the site itself loads. The round logo has NOT replaced it in the code.
3. **The stickers** are a separate product, not branding. They go to customers
   as a bonus and as collectibles.

**Two visual languages are in play on purpose.** The logo and the site are
premium: rose gold, cream, restraint. The stickers are kawaii: faces,
holographic, pixel art, hearts. That is a deliberate split, a serious front of
house and a playful thing in the box. Keep each one in its own lane. Never put
a kawaii face on the store or the cards, and never put the formal lockup on a
collectible sticker.

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

## Instagram card spec (current, set by Kat 29 September 2026)

Kat redrew the plant card and this is the layout to match. It replaces the
earlier 1080 x 1350 version. Where the two disagree, this one wins.

**Canvas: square, 1:1**, rendered at device scale 2. Not 4:5.

**Masthead.** Logo top left, noticeably smaller than before, roughly a tenth
of the canvas height. To its right a hairline rule that runs to the right
edge with **a small four-point diamond set into it**, off centre. The rule is
not plain. A matching rule with the same diamond closes the card at the
bottom.

**Title block, right column, RTL.**
1. Hebrew name, Frank Ruhl Libre, deep green, two lines, large.
2. **Latin name directly underneath in italic Cormorant Garamond, rose.**
   There is no Hebrew common-name line between them any more.
3. Description in Assistant, **two short paragraphs with a gap**, not one block.

**Divider.** Hairline with the same small diamond centred in it.

**Care block.** Heading איך מטפלים in Frank Ruhl Libre, green. Then six rows,
each with **three parts**: a line-art icon on the left, a **bold green label**
next to it, then the value text. The labels are fixed and carry the meaning,
so the icon is decoration rather than the only cue:

| Label | What goes in it |
| --- | --- |
| אור | light |
| לחות | humidity |
| מצע | substrate |
| השקיה | watering |
| רגישות | what it will not tolerate |
| קצב צמיחה | growth rate |

Icons are **outline drawings, not emoji**. The old cards used emoji and they
read as clip art next to this layout.

**Photo.** Arch on the left, taller than wide, with a **thin rose hairline
border**. Not the thick cream frame with a drop shadow that the old card used.

**Footer.** Text only, bottom right, **no panel or box behind it**. Three
lines, with "Pink Leaf" set inline in the third, then the handle in rose
underneath. The handle needs `dir="ltr"` or Hebrew RTL renders it as
`pinkleaf.studio@`.

**Ornament.** A faint leaf watermark sits in the bottom left, very low
contrast, behind the footer rule.

**Fonts.** Frank Ruhl Libre for Hebrew headings, Assistant for Hebrew body,
Cormorant Garamond italic for the Latin name.

**Never put a price, a supplier name, or acclimation state on a card.**

### When a card is the right format at all

Set with Kat 29 September 2026. A card competes with the photograph, so it
does not suit every plant.

- **A plant that sells on how it looks gets a photograph and a caption, not a
  card.** Wrapping a stunning leaf in eight lines of Hebrew works against it.
- **A card earns its place where the story sells the plant** (Tortum, a hybrid
  with an interesting parentage) **and on teaching content**, where there is no
  single photo worth leading with.

Render scripts live in the session scratchpad, which does not survive between
sessions. If the cards need rebuilding, the spec above is the record.
