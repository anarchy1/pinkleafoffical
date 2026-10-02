# Website health log

Running record of what the site audit found, what got fixed, and what is still
open. Read this before auditing so you do not re-report something known.

The check itself is defined in `CLAUDE.md` under "audit the site on your own
initiative". Add a dated section each time it runs.

---

## 26 September 2026

Ran after Kat asked for the Netlify deploy to be verified, then asked for the
audit to become a standing habit.

### Deploy

Green. Published 00:02 UTC, built in 14 seconds, no errors, 242 files, 4
redirect rules applied.

One thing to know about how it got there: the deploy record carries no commit
reference, `deploy_source` is `cli`, and its title names a commit that does not
exist in this repository. The live site was pushed from a folder on the Mac, not
from git. Git and production are therefore not guaranteed to match in either
direction. Do not treat `origin/main` as proof of what is live.

### Fixed this session

| What | Why it mattered |
| --- | --- |
| Branch was 22 commits behind `main` while holding 9 commits of unmerged store work | Kat's price corrections and the stock feed were not live and nobody knew |
| Acclimation gating still present on the branch | Ships supply chain state to a public file, which `CLAUDE.md` forbids. Resolved in favour of `main`, which had already removed it |
| CSS comment reading "imports in transit, customs, or hardening" | Live in `index.html` view-source on production today. Rewritten |
| Product schema advertised old prices for 79 of 80 products | Google would have been told prices the store does not charge. Regenerated with `tools/build_product_schema.py` |

### Checked and clean

- 80 store items, 65 available, 15 coming. Every purchasable option has a price.
- No price rows pointing at options that do not exist. No duplicate ids.
- 8 items without a photo, all of them the `X_` entries that already use the
  shared placeholder. Not a defect.
- All five inline scripts pass `node --check`. Both `ld+json` blocks parse.
- No surviving references to the gating helpers the merge removed.
- `tools/`, `content/`, `CLAUDE.md` and `RESET.md` are 404'd by redirect rules,
  so internal files in the published root are not served.
- `tools/plant-db.csv` carries id, name and family only. No cost data.
- Pricing calculator is gone from both branches.

### Open

1. **Nothing above is live.** It needs a merge to `main` and a deploy from the
   Mac. The customer visible change is the price table moving off round numbers,
   and sold out plants reading as sold out. Waiting on Kat.
2. **`STOCK_SHEET_CSV` is empty.** The Google Sheet stock feed is wired and
   guarded, so it fails quietly and changes nothing. Until Kat supplies the
   sheet URL, "sold out means sold out" is not actually working.
3. **No checkout.** Offer URLs route to WhatsApp. Meshulam through Invoice4U is
   the chosen provider and the payment link is generated per order by hand.
4. ~~Store direction not started.~~ **Wrong, corrected same day.** The clean
   product grid was already built on 23 September and is live in the code. That
   claim came from reading a stale `CLAUDE.md` before the merge brought the
   current one in. Lesson for the audit: read `CLAUDE.md` after merging main,
   not before, or you will report finished work as outstanding.
5. **Cannot see production from a cloud session.** `pinkleaf.co.il` and the
   Netlify preview URLs are blocked by the network egress policy, so audits are
   code-level only. Kat can open this in the cloud environment's network access
   settings.
6. **Seasonal theming: mechanism built, OFF, awaiting Kat's approval of a
   look.** `SEASON_THEMES` in index.html switches the same six palette tokens
   dark mode already uses, by date window, repeating yearly. Sukkot, winter and
   Tu BiShvat palettes are drafted. `enabled` is `false`, so the site looks
   exactly as it does today and nothing ships until she says yes. Seasons apply
   in light mode only so they never fight the Botanical Lab dark palette.
   Two things she has to do: approve a palette, and check the Sukkot and
   Tu BiShvat windows each year, since Hebrew dates move against the Gregorian
   calendar. Winter does not move.
7. ~~Sticker page requested.~~ **Built 26 September**, at `/stickers/`, and
   linked from the intro buttons and the crawlable index. Shows the one printed
   sticker; the other five are a single panel rather than five empty tiles,
   which had made the phone page 8000px of mostly nothing. Still open: Kat's
   shortlist of the final six, so the page can fill in.
8. **The round online logo is not in the site code.** Kat uses
   `brand/logo-round-online.jpg` as the logo online, but the site still loads
   the old `logo-light.png` / `logo-dark.png` pair. She calls the round one
   temporary, so this is on hold rather than a defect, but the two are out of
   step and someone will notice.

---

## 26 September 2026, hourly pass 1

Health check: branch drift 0 behind and 16 ahead, schema 83 offers 0 mismatches,
store data clean at 80 items, no private data, everything parses,
`STOCK_SHEET_CSV` still empty.

**Fixed: the stickers page was orphaned.** It shipped with nothing linking to
it, reachable only by typing the URL. Added a button on the intro beside
Instagram, and an entry in the crawlable index so search engines find it. A page
nobody can reach is the same as no page.

**Tightened health check 4.** It was matching bare words like "deflasked" and
flagging two public teaching articles every pass. The forbidden thing is a
per-plant field such as `acclimation: "deflasked"`, not the word in an article
explaining deflasking to customers. The check now looks for the assignment
shape, so real leaks are not buried in noise.

Nothing else was actionable. The remaining queue is blocked on Kat: the sticker
shortlist, the Google Sheet URL for the stock feed, a Meshulam account, and
approval on the seasonal palettes.

---

## 28 September 2026, full re-audit

Kat asked for a competitor study, a design comparison with the most modern
stores, and for the payment system to actually work. The full write-up is in
`docs/competitor-audit-2026-09-28.md`.

### Health check

- **Branch drift:** none. Branch and `main` were level before this work.
- **Production:** Netlify's current deploy is 26 Sep 10:17 UTC, after the
  last commit on `main`, with the six redirect rules `netlify.toml` defines,
  so production most likely matches `main`. Still a CLI upload with no commit
  ref.
- **Schema against store:** regenerating changed nothing. In sync.
- **Store data:** 80 items, no duplicate ids, 83 price rows, no orphans,
  every available plant's grades priced.
- **Private data:** no assignment-shaped supply chain fields, no supplier
  names, no cost fields in deployed files.
- **It still runs:** all inline scripts pass `node --check`, all `ld+json`
  parses. But see the first fix below: parsing is not the same as running.
- **Unbuilt switches:** `STOCK_SHEET_CSV` still empty. New one:
  `I4U_API_KEY` in Netlify switches card payment on (see the audit file).

### Fixed this session

| What | Why it mattered |
| --- | --- |
| `renderStore()` called an undefined `filteredItems` and threw on every render | Every `#/plant/` link, the kind shared on Instagram and WhatsApp, fell back to the plain store instead of opening the plant. `view_item` analytics never fired. `node --check` cannot catch this; only running the page does, so the health check now needs a browser pass too |
| Logo swap inverted in three places | After using dark mode, or the accessibility reset, the white wordmark sat on a white page |
| Organization schema logo was the white wordmark | Google would show a near invisible logo |
| Floating buttons over the bag drawer on mobile | Covered the drawer title and main button |
| Plants had no checkout; card option never appeared | Built: see the audit file, section 3 |

### Lesson for the health check

Add a **browser pass** to check 5: load the page in headless Chromium and
fail on any `pageerror`. Syntax checks passed for days while the store threw
on every render.

### Open, needs Kat

1. Deploy this branch. Customer visible: the new checkout with ₪37 shipping
   shown up front, the smaller logo on inner pages, the deeper rose buttons.
2. Add `I4U_API_KEY` in Netlify to switch card payment on, then place one
   small real order.
3. Confirm which phone number takes Bit (the site and the registry disagree).
4. Approve or change the checkout's refund line and write a cancellation
   policy.
5. Stale crawlable store text (one plant listed as available that is coming).

---

## 29 September 2026, second pass

- **Drift:** branch 3 ahead of `main`, 0 behind. Nothing deployed since
  26 Sep.
- **Found: work recorded but never committed.** Notion's inventory page says
  the Philodendron Radiatum was switched to available on 28 Sep. No branch
  had that change. Applied here and the schema regenerated. If a Mac session
  made it locally, expect a trivial merge.
- **Delivery:** the courier behind the 37 shekel rate stopped operating.
  `SHIPPING_FLAT_ILS` is now null: delivery orders pay for the plants only and
  the studio arranges delivery. Browser and function tests re-run clean.
- **Still open from yesterday:** Bit number, refund line, cancellation
  policy, stale crawlable store text, `STOCK_SHEET_CSV` empty.

---

## 30 September 2026, SEO pass on articles and encyclopedia

45 pages checked (27 encyclopedia, 18 articles). The basics are sound on every
page: canonical, one h1, Open Graph, structured data, sitemap entry, internal
links, no duplicate titles or descriptions.

What holds them back in search:

1. **38 of 45 titles are English only.** Israeli buyers search in Hebrew.
   Only 10 pages declare `lang="he"`; the encyclopedia pages carry Hebrew
   content under `lang="en" dir="ltr"`.
2. **23 titles are over 65 characters** and get cut off in Google results.
3. **30 meta descriptions are outside 70 to 170 characters** (some over 200,
   some under 50).
4. **26 pages have no `datePublished`**, so search engines cannot see them as
   fresh.
5. **Cadence:** Kat's plan was five new topics a week. The encyclopedia has 26
   entries in total. The gap is the pipeline, not the pages.

Fixing 1 to 3 is new customer-facing copy in Google results, so it waits for
Kat's approval.

### Fixed 1 Oct 2026 (Kat approved)

All 45 pages now have titles of 60 characters or fewer, descriptions of 115
to 160, Hebrew-first titles and descriptions on the 27 encyclopedia pages, and
datePublished / dateModified from git history. Seven garbled Hebrew
descriptions that Google was showing were rewritten. Source of truth:
`tools/seo_meta.json`, applied by `tools/apply_seo_meta.py`. Page language
attributes were left as they are: the encyclopedia pages carry both languages,
and flipping their direction would move the layout.

## 2 Oct 2026: store restyle (Pink Modern) and branch drift

Kat chose the pink direction from the mockups. The store grid is rebuilt:
square photos two across on phones (was one plant per screen), family chips
in the visitor's language, search first, one deep rose button per card, and
family plus "young plant" under every name so the grown photo is not taken
for what ships. Only exception badges show (sold out, coming soon, last one,
sale).

Found while doing it:

- **Branch drift.** `main` had two store commits this branch lacked (Hebrew
  store strings via `ST()`, filled ADD TO BAG). Merged in; the Hebrew labels
  are kept.
- **Button contrast.** That filled button was #b97a8e under white text,
  about 3.2:1, below the 4.5:1 for normal text. Now `--rose` #B04A6F, about
  5.2:1.
- **Stale delivery line.** The store still said "Nationwide shipping across
  Israel" after the courier stopped on 28 Sep. Now: pickup from the studio,
  delivery arranged per order.
- **Unescaped names in handlers.** Store cards passed plant names raw into
  `onclick`; a name with an apostrophe would break the button. Now `pdEsc`.

Health check: inline scripts pass `node --check`, JSON-LD parses, no
supply-chain fields, schema matches prices, browser pass with no `pageerror`,
add to bag and both checkout paths work. Not deployed: waits on Kat.
