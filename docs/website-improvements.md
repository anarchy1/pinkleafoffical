# Pink Leaf website improvement backlog

Written 2026-09-23. Grounded in a read of the actual repo at commit `d54c7fd`,
plus the Pink Leaf Operations Registry and the September 2026 security review in
Notion, plus `content/store-redesign-research-2026-06-09.md`.

This file deploys publicly. It names files and line numbers but never reproduces
private numbers, supplier names, customer records or internal formulas.

## Settled direction (not re-opened here)

From CLAUDE.md and the June 2026 store research. Treat as decided:

- Replace the card/carousel "game" layout with a clean product grid.
- Three store categories: Alocasia, Monstera, Philodendron.
- Payment provider is Meshulam (Grow), used as a hosted payment page or payment
  link, because the site is static and cannot process cards server-side. The
  registry records that the card link is generated through Invoice4U, and that
  Bit and PayBox are offered ahead of card.
- Bilingual Hebrew (RTL) and English (LTR), currency ILS.
- No minimum order. Shipping is quoted per order, not a fixed online fee.
- No fake scarcity. Honest "limited release" framing only.

## What the site actually is today

One file does almost everything: `index.html`, 5,191 lines, 258 KB, with all CSS
in a single `<style>` block and all logic in one inline `<script>`. There is no
build step and no backend.

- Six client-side "pages" swapped by `showPage()` (`index.html:3374`): intro,
  store, archive, encyclopedia, lab, care. Hash routing at `index.html:4939`
  onward gives deep links like `#/store` and `#/plant/PV19`.
- The store is **already a grid, not a carousel**. `ALL_STORE_ITEMS`
  (`index.html:3082`) holds 80 items, `ITEM_PRICES` (`index.html:4219`) holds 83
  priced variants, and `renderStore()` (`index.html:3534`) renders category tabs,
  search, a price filter and a sort into `.store-grid` (`index.html:992`). 65
  items are `status: "available"`, 15 are `status: "coming"`.
- The old carousel is dead code that still ships: `spin()` at `index.html:3816`,
  `.carousel-wheel` and `.store-card` CSS at `index.html:896`.
- The "game" is the Lab quiz: a Firebase Firestore leaderboard
  (`index.html:241`) reading `MASTER_DB`, 210 plants auto-generated from
  `tools/plant-db.csv` by `tools/build_plant_db.py`.
- Language: `index.html` keeps its own `lang` variable and `pl_lang` storage key,
  with a `HE/EN` button at `index.html:2504`. `assets/pinkleaf-enhancements.js`
  keeps a second, separate system with a `pinkleaf_lang` key and its own injected
  floating button. They do not know about each other.
- Checkout: bag drawer plus a WhatsApp handoff (`sendBagWhatsApp()`,
  `index.html:4656`). A card button exists but is hidden.

---

# P0: blocking revenue, or leaking data

## P0-1. An internal pricing tool is published on the live site

`tools/pricing-calculator.html` is in the repo, and `netlify.toml` publishes the
repo root with no build and no path exclusions, so it is reachable at
`/tools/pricing-calculator.html`. Its own header calls it internal and says it is
not linked from the public site, but "not linked" is not "not published". It
states an internal pricing method and carries default multiplier values.

The September 2026 security review in Notion records that this file was thought
to have been deleted on 19 Sep and that the netlify 404 blocks for these paths
were committed but probably never went live. The file is still here.

**Not fixed in this pass, per instruction.** Kat decides: delete the file, move
it out of the repo, or add a real deploy exclusion. Note that deleting it does
not remove it from git history, and the repo is public.

Why it matters: it is the clearest line in CLAUDE.md, no cost or margin math in a
deployed file. Size: small, minutes, but the decision is Kat's.
Files: `tools/pricing-calculator.html`, `netlify.toml`.

## P0-2. Internal research notes are published on the live site

`content/` deploys the same way. `content/store-redesign-research-2026-06-09.md`
line 32 restates the same internal pricing method, and line 18 lists the internal
supply-chain vocabulary that CLAUDE.md forbids in deployed files. The security
review names this file and `content/social-audit-2026-04-10.md` as public.

**Not fixed in this pass.** Same decision as P0-1: these are useful durable notes,
they just should not be served to the public web.

Size: small. Files: `content/store-redesign-research-2026-06-09.md`,
`content/social-audit-2026-04-10.md`, `content/seo-keyword-research-2026-04-10.md`,
`content/week-2026-04-10-social.md`.

## P0-3. The supply-chain vocabulary is still in the deployed page source

The store items themselves are clean: no item in `ALL_STORE_ITEMS` carries an
`acclimation` field any more, which commit `37847a9` fixed. But the machinery and
its vocabulary are still shipped in `index.html`:

- `index.html:1117`, a CSS comment naming the internal stages.
- `index.html:3505` to `3523`, the comment, `ACCLIMATION_LABELS`,
  `ACCLIMATION_HE` and `acclimationStage()`.

All four stage names are readable in `view-source:`. The labels all map to
"Coming Soon", so the code does nothing a customer sees, but the words are there.

**Not fixed in this pass.** The clean fix is to delete the gating machinery
entirely, since `status: "coming"` already does the job and the rule says that is
the only allowed signal.

Size: small, a clean deletion of roughly 25 lines plus the render branches that
depend on it at `index.html:3578`, `3588`, `3602`, `3648`.
Files: `index.html`.

## P0-4. There is no checkout. The card button is wired but switched off

`INVOICE4U_PAY_URL` is an empty string at `index.html:4459`. Because of that, the
pay button at `index.html:2631` stays `display:none` (`index.html:4587`), and
`payWithInvoice4u()` falls straight back to the WhatsApp handoff
(`index.html:4464`). Every sale is still a manual conversation.

**Already half-built**, and built well: `computeBagTotals()` (`index.html:4477`)
is a single source of truth for the money, the bag persists to localStorage, and
the shipping policy note is already written. The missing piece is one URL and a
test order.

What to do: create the hosted payment page, paste the URL, confirm whether it
accepts the amount as a URL parameter (the parameter name is configurable at
`index.html:4460`), then place one real order end to end before announcing it.
Keep WhatsApp as the fallback, as the research doc says.

Size: small in code, larger in setup and testing. Files: `index.html`.

## P0-5. Sold out never fires, so a sold plant stays buyable

`STOCK_SHEET_CSV` is an empty string at `index.html:4330`, so `loadLiveStock()`
returns immediately (`index.html:4358`) and `LIVE_STOCK` stays empty. Every
downstream check then returns "unknown, so do not block":
`variantQty()` returns null, `variantSoldOut()` is always false, `itemSoldOut()`
is always false, and `itemUnitsLeft()` is null.

The practical effect: the "Sold Out", "Last One" and disabled-variant paths in
`renderStore()` are unreachable, the add-to-bag backstop at `index.html:4524`
never triggers, and all 65 available plants look buyable whatever is on the shelf.

**Already half-built**, and thoughtfully: the CSV parser tolerates quoted fields,
a blank quantity keeps a plant purchasable, and the sheet can also move a plant
between available and coming (`syncStoreStatus()`, `index.html:4427`). The
comment at `index.html:4327` already warns that only public-safe columns belong
in that sheet, which matters because publishing it makes it readable by anyone
with the link. Keep it to id, variant, name, category, qty, price, status.

The registry points at the Sep 13 shelf count in Notion as the real stock truth,
so that count is the natural first fill of the sheet.

Size: small in code, real work in keeping the sheet honest.
Files: `index.html`.

## P0-6. It is not clear where a push to main actually goes

CLAUDE.md says GitHub Pages, push to `main`, live in about 60 seconds, and `CNAME`
contains `pinkleaf.co.il`. But `netlify.toml` is in the repo, and the Notion
security review records that on 26 Aug 2026 the domain nameservers were moved to
Netlify's, and that the live deploy at the time of the review was a manual upload
that had not refreshed since 9 Sep.

If that is still true, every item in this backlog is unshippable until it is
resolved, and worse, the fixes in P0-1 through P0-3 would not take effect either.

What to do, before anything else: confirm which host serves `pinkleaf.co.il`
today, confirm that host builds from `main` automatically, push one trivial
visible change, and watch it appear. Then correct the "Deploy / dev environment
notes" section of CLAUDE.md so the next session is not misled.

Size: small, mostly checking. Files: `netlify.toml`, `CNAME`, `CLAUDE.md`.

## P0-7. The shop is English-only for Hebrew visitors

The page defaults to Hebrew for Israeli visitors (`index.html:3179`), and Israel
is the entire shipping market. But the store interface is hardcoded English:

- Category tabs `ALL / ALOCASIA / MONSTERA / PHILODENDRON` (`index.html:2724`).
- Filters: `Any price`, `Under 300`, `Featured`, `Price: low to high`
  (`index.html:2731` to `2743`).
- Every badge: `Available`, `Coming Soon`, `Sold Out`, `Last One`,
  `Opening Sale`, `Limited Release` (`index.html:3582` to `3598`).
- Every button: `ADD TO BAG`, `NOTIFY ME`, `COMING SOON`, `Select Variant`,
  `Select Size`, `(Sold Out)`, `(Unavailable)`.
- The result count `"80 plants"` (`index.html:3568`) and the empty state
  (`index.html:3571`).
- The product detail overlay description and care lines (`index.html:3685` to
  `3700`), which are English prose generated at runtime.

`toggleLang()` (`index.html:4090`) re-renders the intro, the nav, the encyclopedia
and the care page, but it never calls `renderStore()`, so even the parts that
could switch do not.

What to do: add a small string table keyed by `he` and `en`, route every literal
above through it, and add `renderStore()` plus a product-overlay refresh to
`toggleLang()`. The rest of the site already proves the pattern works.

Size: medium, one focused pass through `renderStore()` and the product overlay.
Files: `index.html`.

## P0-8. The product schema Google sees is stale and contradicts the store

`index.html:42` to `220` carries the JSON-LD. Problems, in order of harm:

- Only 4 products are described, out of 80 in the store. Every other plant is
  invisible to rich results.
- `"paymentAccepted"` at `index.html:59` still says PayPlus. PayPlus was
  superseded by Meshulam in June 2026, and the registry lists Bit and PayBox as
  the first two methods offered. None of that is reflected.
- Alocasia Polly Pink is published at 199 and 350 (`index.html:140`, `150` to
  `170`), which does not match the current `ITEM_PRICES` entry for that plant.
  Publishing a price that differs from the page is the usual cause of Google
  dropping or flagging a merchant's rich results.
- Availability is hardcoded. Philodendron Jose Buono is `OutOfStock` at
  `index.html:213`, Alocasia Macrorrhiza Variegata is `InStock` at
  `index.html:200`, and both are `status: "coming"` in the store data.
- Every `offers.url` points at a WhatsApp inquiry rather than a checkout, which
  is honest today and should change with P0-4.

What to do: generate the Product graph from `ALL_STORE_ITEMS` and `ITEM_PRICES`
rather than hand-maintaining it, so a price can never be right in one place and
wrong in the other. Fix `paymentAccepted` in the same pass.

Size: medium. Files: `index.html`, and a small generator alongside
`tools/build_plant_db.py` if the graph is to be built rather than typed.

---

# P1: high value

## P1-1. Two language systems fight each other, and the visitor's choice is lost

There are two independent implementations:

- `index.html`: `lang` variable, `pl_lang` storage key, `HE/EN` button at
  `index.html:2504`, `toggleLang()` at `index.html:4090`.
- `assets/pinkleaf-enhancements.js`: `PinkLeaf.setLang()`, `pinkleaf_lang`
  storage key, and a floating toggle button that the script injects into the body
  if one is not already there.

Consequences, all reproducible:

1. Two language toggles appear on the page, and they read different keys, so they
   can disagree.
2. The injected toggle only flips `<html lang>` and `<html dir>`. It never
   touches the `lang` variable, so the layout direction flips while the nav,
   intro, store and bag text stay in the previous language.
3. The enhancement script initialises on `DOMContentLoaded`, and `index.html`
   sets direction again in `window.onload` (`index.html:4964`), which runs later.
   So a preference saved by the injected toggle is overwritten on every reload.

What to do: pick one. The `index.html` system is the one that actually translates
content, so keep it and delete section 3 of the enhancements script, or have the
enhancement delegate to `toggleLang()`.

Size: small. Files: `assets/pinkleaf-enhancements.js`, `index.html`.

## P1-2. The care and substrate line is both hidden and broken

`SUBSTRATE_DB` (`index.html:3073`) holds six real products with photos in
`plants/care/`, Hebrew descriptions and prices under keys `l5` and `l10`.

But `renderCareProducts()` (`index.html:3839`) only understands `l1`, `l2` and
`l10`. Line 3846 labels anything that is not `l10` or `l2` as "1 ליטר", so a 5
litre product is labelled 1 litre. Line 3847 then marks a row purchasable only
when the key is exactly `l1`, so **every single row renders as sold out** and
nothing in the care range can be added to the bag.

On top of that the page is unreachable: the nav link is `display:none`
(`index.html:2691`) and the page carries `data-temporarily-hidden="true"`
(`index.html:2871`).

So this is a whole product line, already photographed, described and priced, that
no customer can see or buy. Fix the size mapping, decide which sizes are really in
stock, then unhide the nav link.

Size: small. Files: `index.html`.

## P1-3. The homepage leads with the game, not the plants

`index.html:2697` to `2718`. The intro panel is followed by a large tappable Lab
teaser: "Can you name the plant?", "Earn XP", "Climb the leaderboard", "TAP TO
PLAY". The store gets one button among three.

The settled direction is to demote the game. Make the store the primary call to
action, put a small strip of real plants with prices on the homepage, and shrink
the Lab to a normal nav item. The Lab is genuinely good and worth keeping, it
just should not outrank the shop.

Size: small to medium. Files: `index.html`.

## P1-4. The image payload is very heavy, and the tooling for it is unused

`plants/` is 84 MB. 228 JPEGs average 342 KB, the largest is 3.0 MB, and several
others are over 1.5 MB. There are zero `.webp` and zero `.avif` files. A shopper
opening the store on mobile data pulls dozens of full-resolution photographs.

Meanwhile `assets/pinkleaf-enhancements.js` already implements blur-up lazy
loading and automatic `<picture>` wrapping with AVIF and WebP sources, keyed on
the classes `pl-lazy` and `pl-modern`. Those classes appear **zero times** in
`index.html`. The module is dead weight.

What to do: generate WebP (and optionally AVIF) derivatives, cap the longest edge
at roughly 1200 px for grid use, keep the originals out of the deploy or
downsample them, and either wire up `pl-modern` or delete the module. Native
`loading="lazy"` is already on the store and archive images, which helps but does
not reduce the bytes actually fetched.

Size: medium, mostly a one-off conversion script plus a small render change.
Files: `plants/`, `index.html`, `assets/pinkleaf-enhancements.js`.

## P1-5. Eight store items have no photo, and one of them is on sale now

These ids in `ALL_STORE_ITEMS` have no matching file in `plants/`:
`X_melo_aurea`, `X_venom_aurea`, `X_angela_aurea`, `X_black_cardinal`,
`X_radiatum`, `X_monstera_jungle_mint`, `X_brown_beauty`, `X_atabapoense_pink`.

Each falls back to `logo-dark.png` (`index.html:3661`), which is a 152 KB logo
used as a product photo. Seven are `status: "coming"`, which is survivable.
`X_melo_aurea` is `status: "available"`, added in the most recent commit, so
there is a plant for sale today with a logo where its picture should be.

Also worth a better fallback: a small neutral placeholder instead of the full
logo file, since the logo is larger than many of the real photos.

Size: small. Files: `plants/`, `index.html`.

## P1-6. Products have no crawlable URLs

A product opens as an overlay at `#/plant/PV19` (`index.html:4950`). Hash
fragments are never sent to the server and search engines do not index them as
separate pages. `sitemap.xml` has 39 URLs and not one is a product.

So the encyclopedia and the articles, which do have real URLs, carry all of the
search traffic, and the actual saleable inventory carries none. For a shop whose
differentiator is rarity, "Alocasia Venom Pink Israel" is exactly the query worth
owning.

Options, cheapest first: keep the overlay but generate a thin static page per
available plant (the `encyclopedia/` directory already shows this pattern works),
and add those to `sitemap.xml`. The generator can reuse `tools/build_plant_db.py`
conventions so the pages never drift from the store data.

Size: medium. Files: new per-product pages, `sitemap.xml`, `tools/`.

## P1-7. The no-JavaScript fallback advertises a store that no longer exists

`index.html:4998` onward. The `<noscript>` block lists exactly one plant, Alocasia
Macrorrhiza Variegata, with prices that do not match the current data, and its
care section lists a substrate range ("Pazo Mix" and friends) that was replaced by
the Botanique line in commit `05600a7`.

The article and encyclopedia lists in the same block are accurate and useful. Only
the store and care sections are stale. Either generate those two sections from the
real data or remove them, because a crawler reading that block currently learns
that Pink Leaf sells one plant.

Size: small. Files: `index.html`.

## P1-8. Analytics fire before the cookie banner is answered

Google Analytics is configured and sends at `index.html:232` to `238`, in the
`<head>`, unconditionally. The privacy and cookie banner that asks permission is
at the very bottom of the page, and `cookieConsent()` runs only when the visitor
clicks. So consent is requested after the data has already been sent, and a
visitor who clicks "דחייה" has already been counted.

The banner cites Israeli privacy law by name, so the gap between what it promises
and what the page does is worth closing. Standard fix: load the analytics tag only
after acceptance, or use consent mode defaults set to denied.

Size: small. Files: `index.html`.

## P1-9. The Lab leaderboard collects email addresses into an open collection

`registerUser()` (`index.html:3319`) writes `{ name, email, xp, joinedAt }` to the
Firestore collection `labRegistry` (`index.html:3352`). The Firebase config,
including the project id, is in the page source at `index.html:245`, which is
normal for Firebase and not itself the problem. The problem is what the security
rules allow: if `labRegistry` is readable, anyone can read every stored name and
email, because the client reads the whole collection to draw the scoreboard
(`index.html:276`).

Two questions for Kat, in order:

1. Does the game need an email address at all? The leaderboard only displays
   `name` and `xp`. Dropping the field removes the risk entirely.
2. If it stays, the Firestore rules need checking so that reads are limited to the
   fields the scoreboard actually shows.

This is the one place on the site where a member of the public types personal data
into a store Pink Leaf controls, so it deserves a look even though nothing is
known to have gone wrong.

Size: small in code, needs a console check. Files: `index.html`, Firebase rules.

## P1-10. Two plants cannot be reached from any category tab

`plFamily()` (`index.html:3487`) resolves a family from `MASTER_DB`, falling back
to parsing the genus out of the name. Two saleable items resolve to `Others`:
`PV13` Rhaphidophora Tetrasperma Mint, and `X_xanthosoma_mickey` Xanthosoma Mickey
Mouse. The store has only ALL, Alocasia, Monstera and Philodendron tabs
(`index.html:2723`), so those two appear under ALL and nowhere else.

The three-category rule is settled, so the answer is a decision rather than code:
either these two are folded into the nearest category, or they are dropped from the
store, or a small "More rare aroids" tab is added. Leaving them reachable only from
ALL is the one option that is just an accident.

Size: small. Files: `index.html`.

---

# P2: polish and cleanup

## P2-1. Delete the dead carousel

Left over from the layout being replaced: `spin()` (`index.html:3816`), the
`#wheel` element lookup and `window.sAng` / `window.sLen` globals it depends on
which no longer exist, `.carousel-wheel` and `.store-card` CSS (`index.html:896`
to `930`), `.store-grid-flat` and `.store-card-flat` (`index.html:2470` to
`2494`), and `filterStore()` (`index.html:3455`) which reads a
`store-filter-select` element that is not in the page. `addToCart()` still
defensively looks for `.store-card` and `.store-card-flat` ancestors
(`index.html:4499`).

Size: small. Files: `index.html`.

## P2-2. `entries.json` exists twice, and the copies have diverged

`entries.json` at the root and `src/data/entries.json` have different checksums.
The site fetches the root copy (`index.html:4718`). Either the `src/` copy is the
editing source and the root copy is the build output, in which case that should be
written down and a build step should produce it, or the `src/` copy is stale and
should go. Right now a future session can reasonably edit the wrong one.

Size: small. Files: `entries.json`, `src/data/entries.json`.

## P2-3. The repo breaks its own em dash rule 1,812 times

CLAUDE.md states the rule as absolute, and the Humanizer hook enforces it only on
files a session actually writes or edits. Files written before the hook existed
still carry the character: 1,812 occurrences across 43 deployed HTML, JSON and
Markdown files, mostly in `articles/`, `encyclopedia/` and `entries.json`.
`index.html` is clean.

A single sweep would settle it. Worth doing carefully, since some of those are
inside Hebrew prose where the replacement punctuation is not always a comma.

Size: small to medium, mechanical. Files: `articles/`, `encyclopedia/`,
`entries.json`.

## P2-4. Third party scripts on every page load

`index.html` loads Tailwind from a CDN at runtime (`index.html:372`), the confetti
library (`index.html:373`), the Firebase app and Firestore modules
(`index.html:242`), Google Fonts, and Google Analytics. Tailwind's CDN build
compiles classes in the browser on every visit, which is explicitly not intended
for production. Firebase and confetti are only needed on the Lab page.

Cheapest improvement without a build step: load Firebase and confetti lazily when
the Lab page opens, and replace the Tailwind CDN with a small static stylesheet
containing only the utilities actually used.

Size: medium. Files: `index.html`.

## P2-5. Invalid markup: a stray closing tag

`index.html:2757` closes `page-vault`, then `index.html:2759` closes a `<main>`
that was never opened. Browsers recover from it silently, which is exactly why it
has survived. `showPage()` hides pages with `document.querySelectorAll('main')`,
so malformed nesting here is worth not leaving to chance.

Size: trivial. Files: `index.html`.

## P2-6. Keyboard and screen reader gaps in the store

- Product photos open the detail overlay through `onclick` on a `div`
  (`index.html:3661`), with no `tabindex`, no `role` and no key handler, so the
  overlay cannot be opened from a keyboard.
- The category tabs are plain buttons with no `role="tablist"` and no
  `aria-selected`, so the active category is conveyed by colour alone.
- Availability badges are decorative spans, so "Sold Out" is not announced with
  the product name.

The site already advertises accessibility work: a skip link at `index.html:2499`
and an accessibility drawer citing IS 5568. The store is the part that has not
caught up.

Size: small. Files: `index.html`.

## P2-7. The share image is a plant photo declared as a share card

`og:image` is `plants/PV19.jpg` with `og:image:width` 1200 and
`og:image:height` 630 (`index.html:28` to `30`). The declared dimensions are the
standard share card size, not the dimensions of that photograph. Generate a real
1200 by 630 card with the logo and one plant, and point both Open Graph and
Twitter at it.

Size: small. Files: `index.html`, new asset.

## P2-8. Dated values that will quietly go stale

- `priceValidUntil: "2026-12-31"` appears on every offer in the JSON-LD. After
  that date Google may stop showing the price. Worth either rolling it forward
  with the schema generator in P0-8 or removing it.
- The "Opening Sale" badge (`index.html:3584`) and the `openingSale` flag need an
  end date, or the studio is permanently opening.
- The archive page renders all photos of a genus in one pass
  (`renderVault()`, `index.html:3829`). With 210 plants in `MASTER_DB` and the
  image weights in P1-4, the Alocasia tab alone is a heavy load. Pagination or a
  smaller thumbnail set would help.

Size: small each. Files: `index.html`.

---

## Suggested order

1. P0-6 first. Until a push to `main` is known to reach `pinkleaf.co.il`, nothing
   below it is real.
2. P0-1, P0-2, P0-3 together, as one privacy pass, with Kat deciding on each file.
3. P0-5 then P0-4: know what is in stock before taking money for it.
4. P0-7 and P0-8: make the shop speak Hebrew and stop publishing prices that
   disagree with the page.
5. P1 in the order listed. P1-2 is the cheapest revenue in the list, since the
   products already exist and only the size mapping is wrong.

## Things this pass deliberately did not do

No site file was changed. The privacy items in P0-1 to P0-3 were found, not fixed,
because the fix for each is a deletion decision that belongs to Kat, and because
deleting a file from a public repo does not remove it from history.
